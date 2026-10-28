import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL")
API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_PROMPT = (
    "You are an experienced programming instructor. "
    "Explain concepts simply, using examples, in English"
)


class CodeAnalysis(BaseModel):
    category: str = Field(description="Category or topic of the code query")
    confidence: float = Field(description="Confidence level from 0.0 to 1.0")
    explanation: str = Field(description="Brief explanation or summary")


class ChatSession:

    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.messages = []

    def ask(
        self,
        user_prompt: str,
        temperature: float = 0.5,
    ) -> str:
        self.messages.append(
            {
                "role": "user",
                "parts": [{"text": user_prompt}],
            }
        )

        response = self.client.models.generate_content(
            model=MODEL,
            contents=self.messages,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": temperature,
            },
        )

        answer = response.text
        self.messages.append(
            {
                "role": "model",
                "parts": [{"text": answer}],
            }
        )

        return answer

    def ask_structured(self, user_prompt: str, temperature: float = 0.2) -> str:
        response = self.client.models.generate_content(
            model=MODEL,
            contents=user_prompt,
            config={
                "system_instruction": SYSTEM_PROMPT + " Analyze the request and respond in JSON format.",
                "temperature": temperature,
                "response_mime_type": "application/json",
                "response_schema": CodeAnalysis,
            },
        )
        return response.text
