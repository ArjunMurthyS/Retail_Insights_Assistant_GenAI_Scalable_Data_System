import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMClient:
    def __init__(self, model_name=None):
        self.llm = None
        
        # 1. Check for OpenAI Key (Priority)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            if not model_name:
                model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
            try:
                self.llm = ChatOpenAI(
                    model_name=model_name,
                    openai_api_key=openai_key,
                    temperature=0
                )
                print(f"LLM Initialized: OpenAI ({model_name})")
            except Exception as e:
                print(f"Error initializing OpenAI: {e}")
            return # Exit if OpenAI attempted (success or fail)

        # 2. Fallback to Google Key
        google_key = os.getenv("GOOGLE_API_KEY")
        if google_key:
            if not model_name:
                model_name = os.getenv("GOOGLE_MODEL_NAME", "gemini-1.5-flash")
            try:
                self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=google_key,
                    temperature=0,
                    convert_system_message_to_human=True
                )
                print(f"LLM Initialized: Google Gemini ({model_name})")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
        else:
            print("WARNING: No valid API Key found (OPENAI_API_KEY or GOOGLE_API_KEY). LLM features disabled.")

    def generate_response(self, prompt, retries=3):
        """
        Generate a response from the LLM.
        """
        if not self.llm:
            return "Error: LLM not initialized (Missing API Key)."
            
        for attempt in range(retries):
            try:
                response = self.llm.invoke(prompt)
                return response.content
            except Exception as e:
                error_str = str(e)
                # Handle Rate Limits for both providers
                if "429" in error_str or "ResourceExhausted" in error_str or "RateLimitError" in error_str:
                    if attempt < retries - 1:
                        time.sleep(2 * (attempt + 1)) # Exponential backoff
                        continue
                    return f"Error: Quota exceeded. Please try again later. Details: {error_str}"
                return f"Error calling LLM: {error_str}"
