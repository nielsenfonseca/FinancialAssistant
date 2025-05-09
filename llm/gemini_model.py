import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class GeminiModel:
    def __init__(self, model_name="gemini-2.0-flash", temperature=0.2):
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def __call__(self, messages):
        return self.llm.invoke(messages)