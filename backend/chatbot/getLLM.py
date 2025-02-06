
from groq import Groq

class GetLLM:
    def __init__(self,
                 llm_name:str ,
                 api_key: str = None):
        """
        Initialize the RAG class.

        Args:
        api_key (str, optional): API key for the language model.
        """
        self.Groqclient=Groq(api_key=api_key)
        self.llm_name=llm_name

    def generate_content(self, prompt_structure):
        """
        Generate content using the generative AI model.

        Returns:
        str: The generated response.
        """
        # Prepare the data payload for the API request
        data = {
            "model": self.llm_name,
            "messages": prompt_structure,
        }

        # Generate the response using the generative AI model
        chat_completion = self.Groqclient.chat.completions.create(**data)
        response = chat_completion.choices[0].message.content
        if(not response):
            response = "Xin lỗi, tôi không hiểu câu hỏi của bạn. Vui lòng thử lại."
        return response
    



if __name__ == "__main__":
    # Load environment variables from .env file
    env = dotenv.dotenv_values(".env")
    api_key = env.get("GEMINI_KEY")
    llm= GetLLM(llm_name='llama-3.1-8b-instant',api_key = api_key)
    prompt_structure = [
        {
            "role": "system",
            "content": "You are a helpful assistant! Your name is Bob."
        },
        {
            "role": "user",
            "content": "What is your name?"
        }
    ]
    print(llm.generate_content(prompt_structure))
    


