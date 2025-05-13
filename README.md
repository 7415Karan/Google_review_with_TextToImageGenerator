**AI-Powered Customer Feedback Analyzer & Image Generator**

This project is a Flask-based API that leverages LLMs (Large Language Models) to intelligently analyze customer feedback (from restaurants, hotels, etc.) and generate image content based on user prompts. It supports multilingual output and offers actionable insights for businesses based on sentiment analysis

Features-
Sentiment Analysis: Detects whether customer feedback is positive, negative, or mixed.
Language Detection: Automatically identifies or uses the specified language for analysis and response.
Problem Extraction: Identifies customer-reported problems or complaints from the review.
Practical Solutions: Suggests actionable steps for improvement.
Auto-Generated Company Response: Creates polite, context-aware responses in the review's language.
AI Image Generation: Converts text prompts into AI-generated images via Freepik API.

Technologies Used
Flask: Lightweight Python web framework for building RESTful APIs.
LangChain + Groq API: For integrating and invoking LLMs like LLaMA 3.1 via ChatGroq.
CORS (Cross-Origin Resource Sharing): Enables frontend-backend communication.
Regex & JSON: For parsing and handling structured data from LLM responses.
Freepik AI Image API: Converts text prompts into relevant visuals using an external API.
