import os
import dotenv
from groq import Groq

# Ensure the script can find the .env file anywhere
dotenv.load_dotenv(dotenv.find_dotenv())


class LLMClient:
    """Class to interact with the Groq LLM API."""

    def __init__(self, llm_name: str, api_key: str = None):
        """
        Initialize the LLMClient class.

        Args:
            llm_name (str): The name of the language model.
            api_key (str, optional): API key for the language model.
        """
        self.groq_client = Groq(api_key=api_key)
        self.llm_name = llm_name

    def generate_content(self, prompt_structure):
        """
        Generate content using the generative AI model.

        Args:
            prompt_structure (list): The chat history as a list of dictionaries.

        Returns:
            str: The generated response.
        """
        try:
            chat_completion = self.groq_client.chat.completions.create(
                model=self.llm_name,
                messages=prompt_structure,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {e}"


if __name__ == "__main__":
    api_key = os.getenv("GROQ_KEY")

    llm = LLMClient(llm_name="llama-3.1-8b-instant", api_key=api_key)
    prompt_structure = [
        {"role": "system", "content": "You are a helpful assistant! Your name is Bob."},
        {"role": "user", "content": "What is your name?"},
    ]

    print(llm.generate_content(prompt_structure))
