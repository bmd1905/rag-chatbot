from IPython.display import Markdown
import textwrap
from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize
import dotenv
from getCollection import MongoDBClient
from getLLM import LLMClient
import os

# Ensure the script can find the .env file anywhere
dotenv.load_dotenv(dotenv.find_dotenv())


class RAG:
    def __init__(
        self, llm_model, collection, embedding_name: str = "dangvantuan/vietnamese-embedding", history: list = None
    ):
        self.llm = llm_model
        self.collection = collection
        self.embedding_model = SentenceTransformer(embedding_name)
        self.tokenize = tokenize
        self.chat_history = history or [
            {
                "role": "system",
                "content": (
                    "Bạn tên Lan, là một người tư vấn sản phẩm cho sàn thương mại điện tử BAN. "
                    "Dựa vào thông tin được cung cấp từ hệ thống và câu hỏi của khách hàng, bạn sẽ đưa ra câu trả lời tốt nhất, đầy đủ nhất. "
                    "Hãy nhớ rằng bạn cần thể hiện sự chuyên nghiệp và tận tâm. "
                    "Đừng lặp lại sản phẩm đã tư vấn. "
                    "Trả lời bằng tiếng Việt. "
                    "Xưng hô là 'em' và khách là anh."
                ),
            }
        ]

    def get_embedding(self, text):
        if not text.strip():
            return []
        tokenized_text = self.tokenize(text)
        embedding = self.embedding_model.encode(tokenized_text)
        return embedding.tolist()

    def vector_search(self, query):
        embeddings = self.get_embedding(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": embeddings,
                    "path": "embedding",
                    "numCandidates": 1000,
                    "limit": 10,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "price": 1,
                    "final_price": 1,
                    "shop_free_shipping": 1,
                    "attribute": 1,
                    "description": 1,
                }
            },
        ]
        return list(self.collection.aggregate(pipeline))

    def full_text_search(self, query):
        pipeline = [
            {"$search": {"index": "default", "text": {"query": query, "path": ["name", "description"]}}},
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "price": 1,
                    "final_price": 1,
                    "shop_free_shipping": 1,
                    "attribute": 1,
                    "description": 1,
                }
            },
            {"$limit": 10},
        ]
        return list(self.collection.aggregate(pipeline))

    def create_prompt(self, search_results, query):
        if not search_results:
            return f"Không tìm thấy kết quả nào cho '{query}'. Hãy dùng các thông tin bên trên."
        info = []
        for item in search_results:
            mapped_item = {
                "name": item.get("name", "Không có tên sản phẩm"),
                "price": item.get("price", "Không có thông tin giá"),
                "final_price": item.get("final_price", "Không có thông tin giá cuối"),
                "shop_free_shipping": "Có" if item.get("shop_free_shipping", 0) else "Không",
                "attribute": item.get("attribute", "Không có thông tin thuộc tính"),
                "description": item.get("description", "Không có mô tả"),
            }
            info.append(mapped_item)
        product_details = "\n".join(
            [
                f"- Tên sản phẩm: {prod['name']}, Giá: {prod['price']}, Giá sau giảm: {prod['final_price']}, "
                f"Miễn phí giao hàng: {prod['shop_free_shipping']}, Thuộc tính: {prod['attribute']}, "
                f"Mô tả: {prod['description']}"
                for prod in info
            ]
        )
        return f"""
        Hãy dựa vào thông tin bạn nhận được để trả lời câu hỏi của khách hàng.
        Trả lời đầy đủ thông tin cần thiết: tên sản phẩm, giá tiền, mô tả ngắn gọn.
        Thông tin bạn nhận được:
        {product_details}
        Khách hàng:
        {query}
        Answer:
        """

    def answer_query(self):
        prompt_structure = self.chat_history
        response = self.llm.generate_content(prompt_structure)
        self.update_history("assistant", response)
        return response

    def update_history(self, role, content):
        self.chat_history.append({"role": role, "content": content})

    def remove_history(self):
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "Bạn tên Lan, là một người tư vấn sản phẩm cho sàn thương mại điện tử BAN. "
                    "Dựa vào thông tin được cung cấp từ hệ thống và câu hỏi của khách hàng, bạn sẽ đưa ra câu trả lời tốt nhất, đầy đủ nhất. "
                    "Hãy nhớ rằng bạn cần thể hiện sự chuyên nghiệp và tận tâm. "
                    "Đừng lặp lại sản phẩm đã tư vấn. "
                    "Xưng hô là 'em' và khách là anh."
                ),
            }
        ]

    def get_history(self):
        return self.chat_history

    @staticmethod
    def _to_markdown(text):
        text = text.replace("•", "  *")
        return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


if __name__ == "__main__":
    mongodb_uri = os.getenv("MONGODB_URI")
    api_key = os.getenv("GROQ_KEY")
    llm = LLMClient(llm_name="llama-3.1-8b-instant", api_key=api_key)
    client = MongoDBClient(mongodb_uri, "product", "sendo")
    collection = client.get_collection()
    rag = RAG(collection=collection, llm_model=llm)
    query = "đầm đen"
    search_result = rag.vector_search(query=query)
    prompt = rag.create_prompt(search_results=search_result, query=query)
    rag.update_history(role="user", content=prompt)
    response = rag.answer_query()
    print(response)
