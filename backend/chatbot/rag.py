from IPython.display import Markdown
import textwrap
from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize
# from getCollection import GetCollection
# from getLLM import GetLLM

class RAG:
    def __init__(self,
                 llm_model,
                 collection,
                 embeddingName: str = 'dangvantuan/vietnamese-embedding',
                 history: list = None):
        """
        Initialize the RAG class.

        Args:
        mongodbUri (str): MongoDB URI for connecting to the database.
        dbName (str): Name of the database.
        dbCollection (str): Name of the collection within the database.
        llm_name (str, optional): Name of the language model to use.
        embeddingName (str, optional): Name of the embedding model to use.
        api_key (str, optional): API key for the language model.
        """
        self.llm = llm_model
        self.collection = collection
        self.embedding_model = SentenceTransformer(embeddingName)
        self.tokenize = tokenize
        self.chat_history = history or [
    {
        "role": "system",
        "content": (
            "Bạn tên Lan, là một người tư vấn sản phẩm cho sàn thương mại điện tử BAN. "
            "Dựa vào thông tin được cung cấp từ hệ thống và câu hỏi của khách hàng, bạn sẽ đưa ra câu trả lời tốt nhất, đầy đủ nhất."
            "Hãy nhớ rằng bạn cần thể hiện sự chuyên nghiệp và tận tâm. "
            "đừng lặp lại sản phẩm đã tư vấn "
            "Trả lời bằng tiếng Việt."
            "Xưng hô là 'em' và khách là anh."
        )
    }
]
    def get_embedding(self, text):
        """
        Generate an embedding for the given text.

        Args:
        text (str): The text to generate an embedding for.

        Returns:
        list: The generated embedding as a list.
        """
        if not text.strip():
            return []
        tokenized_text = self.tokenize(text)
        embedding = self.embedding_model.encode(tokenized_text)
        return embedding.tolist()

    def vector_search(self, query):
        """
        Perform vector search in the MongoDB collection.

        Args:
        query (str): The query text.

        Returns:
        list: A list of search results from the collection.
        """
        embeddings = self.get_embedding(query)
        pipeline = [
            {
                "$vectorSearch": {
                "index": "vector_index",
                "queryVector": embeddings,
                "path": "embedding",
                "numCandidates": 1000,  # Number of candidate matches to consider
                "limit": 10  # Return top 'limit' matches
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'name': 1,
                    'price': 1,
                    'final_price': 1,
                    'shop_free_shipping': 1,
                    'attribute': 1,
                    'description': 1
                }
            }
        ]

        # Execute the aggregation pipeline
        results = list(self.collection.aggregate(pipeline))
        return results
    def full_text_search(self, query):
        """
        Perform full-text search in the MongoDB collection.
        """
        pipeline=[{
            '$search': {
                'index': 'default', 
                'text': {
                    'query': query, 
                    'path': ['name','description'],  
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'name': 1,
                'price': 1,
                'final_price': 1,
                'shop_free_shipping': 1,
                'attribute': 1,
                'description': 1            
            }
        },
        {
            '$limit': 5
        }]
        results = list(self.collection.aggregate(pipeline))
        return results
    
    def hybrid_search(self, query,k):
        """
        Perform a hybrid search combining vector search and full-text search using Reciprocal Rank Fusion (RRF).

        Args:
        query (str): The query text.

        Returns:
        list: A combined list of search results from vector and full-text search.
        """
        # Perform vector search
        vector_results = self.vector_search(query)

        # Perform full-text search
        text_results = self.full_text_search(query)

        # Combine results using Reciprocal Rank Fusion (RRF)
        def rrf(results, k=60):
            rank_dict = {}
            for rank, result in enumerate(results):
                name = result['name']
                if name not in rank_dict:
                    rank_dict[name] = 0
                rank_dict[name] += 1 / (k + rank + 1)
            return rank_dict

        vector_rank = rrf(vector_results)
        text_rank = rrf(text_results)

        combined_rank = {}
        for name in set(vector_rank.keys()).union(text_rank.keys()):
            combined_rank[name] = vector_rank.get(name, 0) + text_rank.get(name, 0)

        # Sort results by combined rank
        combined_results = sorted(combined_rank.items(), key=lambda x: x[1], reverse=True)

        # Convert sorted results back to original format
        final_results = []
        for name, _ in combined_results:
            for result in vector_results + text_results:
                if result['name'] == name:
                    final_results.append(result)
                    break

        return final_results[:k]
    def create_prompt(self,search_results,query):
        """
        Create a prompt from search results.

        Args:
        search_results (list): The search results.

        Returns:
        str: The generated prompt.
        """
        # Map each document using the projection fields
        info = []
        if not search_results:
            return f"Không tìm thấy kết quả nào cho '{query}'. Hãy dùng các thông tin bên trên."
        for item in search_results:
            # Safely extract fields with fallback values
            mapped_item = {
                'name': item.get('name', 'Không có tên sản phẩm'),
                'price': item.get('price', 'Không có thông tin giá'),
                'final_price': item.get('final_price', 'Không có thông tin giá cuối'),
                'shop_free_shipping': 'Có' if item.get('shop_free_shipping', 0) else 'Không',
                'attribute': item.get('attribute', 'Không có thông tin thuộc tính'),
                'description': item.get('description', 'Không có mô tả'),
            }
            info.append(mapped_item)

        # Build the prompt text
        product_details = "\n".join(
            [f"- Tên sản phẩm: {prod['name']}, Giá: {prod['price']}, Giá sau giảm: {prod['final_price']}, "
             f"Miễn phí giao hàng: {prod['shop_free_shipping']}, Thuộc tính: {prod['attribute']}, "
             f"Mô tả: {prod['description']}" for prod in info]
        )

        # Generate the final prompt
        prompt = f""" Hãy dựa vào thông tin bạn nhận được để trả lời câu hỏi của khách hàng. Trả lời đầy đủ thông tin cần thiết : tên sản phẩm , giá tiền, mô tả ngắn gọn.
        Thông tin bạn nhận được:
        {product_details}
        Khách hàng: 
        {query}
        Answer:
        """
        return prompt
    def update_history(self, role, content):
        """
        Update the conversation history.

        Args:
        role (str): The role of the participant ('user' or 'assistant').
        content (str): The message content.

        Returns:
        list: The updated history.
        """
        self.chat_history.append({"role": role, "content": content})

    def remove_message(self, role=None, content=None):
        """
        Remove the first message from the conversation history.

        Args:
        role (str, optional): The role of the participant ('user' or 'assistant'). If provided, only messages with this role will be considered.
        content (str, optional): The message content. If provided, only messages with this content will be considered.

        Returns:
        list: The updated history.
        """
        if role is None and content is None:
            # Remove the second message if no role or content is specified
            if self.chat_history:
                self.chat_history.pop(1)
        else:
            # Remove the first message that matches the role and/or content
            for i, msg in enumerate(self.chat_history):
                if (role is None or msg["role"] == role) and (content is None or msg["content"] == content):
                    self.chat_history.pop(i)
                    break
    def remove_history(self):
        """
        Remove all messages from the conversation history.

        Returns:
        list: An empty history.
        """
        self.chat_history = [
    {
        "role": "system",
        "content": (
            "Bạn tên Lan, là một người tư vấn sản phẩm cho sàn thương mại điện tử BAN. "
            "Dựa vào thông tin được cung cấp từ hệ thống và câu hỏi của khách hàng, bạn sẽ đưa ra câu trả lời tốt nhất, đầy đủ nhất. "
            "Hãy nhớ rằng bạn cần thể hiện sự chuyên nghiệp và tận tâm. "
            "đừng lặp lại sản phẩm đã tư vấn "
            "Xưng hô là 'em' và khách là anh."
        )
    }
]
    def answer_query(self):
        """
        Generate content using the generative AI model.

        Returns:
        str: The generated response.
        """
        prompt_structure = self.chat_history
        response = self.llm.generate_content(prompt_structure)
        self.update_history("assistant", response)
        return response
    def get_history(self):
        """
        Get the conversation history.

        Returns:
        list: The conversation history.
        """
        return self.chat_history
    @staticmethod
    def _to_markdown(text):
        """
        Convert text to Markdown format.

        Args:
        text (str): The text to convert.

        Returns:
        Markdown: The converted Markdown text.
        """
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
if __name__ == '__main__':
    # Load environment variables from .env file
    env = dotenv.dotenv_values(".env")
    mongodb_uri= env.get("MONGODB_URI")
    api_key = env.get("GEMINI_KEY")
    llm= GetLLM(llm_name='llama-3.1-8b-instant',api_key = api_key)
    db_name = "product"
    collection_name = "sendo"
    client = GetCollection(mongodb_uri, db_name, collection_name)
    collection=client.get_collection()
    rag=RAG(collection=collection,llm_model=llm)
    query='đầm đen'
    #print(query)
    search_result=rag.vector_search(query=query)
    # for item in search_result:
    #     print(item)
    prompt=rag.create_prompt(search_results=search_result,query=query)
    # #print(prompt)
    rag.update_history(role='user',content=prompt)
    respone=rag.answer_query()
    # with open('response_file.txt', 'w', encoding='utf-8') as file:
    #     file.write(respone)

    print(respone)
    #print(rag.remove_message())
    #print(respone)
    # query = 'trong những sản phẩm trên, có sản phẩm nào giảm giá không'
    # #print(query)
    # rag.update_history(role='user',content=query)
    # respone=rag.answer_query()
    
    #print(respone)
    