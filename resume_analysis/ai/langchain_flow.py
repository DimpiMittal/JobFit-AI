from langchain_huggingface import HuggingFaceEndpoint
import os

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # ensure token is read

def generate_feedback(resume_text):
    try:
        llm = HuggingFaceEndpoint(
            endpoint_url="https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6",
            huggingfacehub_api_token=HF_TOKEN
        )

        prompt = f"""
        You are an AI resume reviewer. Analyze the following resume text and give:
        1. Strengths
        2. Weaknesses
        3. Suggestions for improvement
        Resume Text: {resume_text}
        """

        response = llm(prompt)
        return response

    except Exception as e:
        return f"Error generating feedback: {str(e)}"

