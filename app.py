import os
import json
from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from flask_cors import CORS
from flask_cors import cross_origin
import ast 
import re, requests

app = Flask(__name__)

# Global dictionary to store the two prompt components.
system_prompt = {
            "manual": """
        You're an AI assistant that reviews customer feedback for restaurants,hotels etc.

        Your task is to:
        1. Identify the overall sentiment in the review (positive, negative, or mixed).
        2. Detect or use the provided language for the review..
        3. Extract specific problems or complaints (if any).
        4. Suggest actionable, practical solutions to those problems.
        5. Generate a short, polite company response appropriate to the sentiment, **in the specified language**.

        
        Your output should strictly follow this JSON format:
        {
        "sentiment": "...",
        "language": "...",
        "problems": ["..."],
        "solutions": ["..."],
        "company_response": "..."
        }
        """,
}
API_KEY = "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"
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/get_prompt', methods=['GET'])
@cross_origin()
def get_prompt():
    global system_prompt
    if system_prompt["manual"] is None :
        return jsonify({"error": "No system prompt has been set yet."}), 404

    combined_prompt = ""
    if system_prompt["manual"]:
        combined_prompt += system_prompt["manual"]
    return jsonify({"system_prompt": combined_prompt}), 200

@app.route('/api/chat', methods=['POST'])
@cross_origin()
def chat():
    data = request.get_json()
    if not data or "human_message" not in data:
        return jsonify({"error": "Please provide a 'human_message' field in the request body."}), 400

    #to get user feedback and language
    user_language = data.get("language", "").strip()

    #create dynamic prompt based on user input
    combined_prompt = system_prompt["manual"]
    # if user_language:
        # final_prompt += f"\nThe feedback must be analyzed and company response written in {user_language}."
    combined_prompt = "\n".join(filter(None, [system_prompt.get("manual")]))

        # Build full input message
    full_user_input = f"Customer Review: {data['human_message']}\n"

    if "form_data" in data and isinstance(data["form_data"], dict):
        full_user_input += "\nStructured Feedback (Form Data):\n"
        full_user_input += json.dumps(data["form_data"], indent=2)

    messages = []
    if combined_prompt:
        messages.append(("system", combined_prompt))
    # messages.append(("human", data["human_message"]))
    messages.append(("human", full_user_input))

    #initailize LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=API_KEY,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    try:
        ai_response = llm.invoke(messages)

        # Try to extract JSON object from string
        content = ai_response.content

        # Extract JSON block using regex (matches everything inside outermost `{}`)
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            AI_MSG = json.loads(match.group())
        else:
            AI_MSG = {"error": "Could not extract valid JSON from model response."}
    except Exception as e:
        return jsonify({"error": f"Failed to parse LLM response: {e}"}), 500


        
    return jsonify({"response": AI_MSG}), 200

#text to image generation code 
API_KEYY='FPSXa78a40fab6404ffb9c4359a9066eb74f'
@app.route('/api/image_generater', methods=['POST'])
def image_generater():
    try:
        # Get the prompt from the request
        prompt = request.json.get("prompt","")
        print("Using API key:", API_KEYY)

        # Make the API request
        response = requests.post(
            'https://api.freepik.com/v1/ai/mystic',  # Verify this endpoint
            data={'prompt': prompt},  # Use JSON payload
            headers={'Authorization': f'Bearer {API_KEYY}', # Include API_KEY,
                    'Content-Type': 'application/json'}
        )
    

        # Parse the API response
        try:
            print("Raw Response Text:", response.text)
            result = response.json()
        except ValueError:
            return jsonify({"error": "Invalid response from the API"}), 500

        # Debugging: Log the API response
        print("API-response:", result)

        # Check if the response contains the expected field
        if 'output_url' in result:
            return jsonify({"image_url": result['output_url']}), 200
        else:
            return jsonify({"error": "Failed to generate image."}), 500

    except Exception as e:
        # Log the error and return a response
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
