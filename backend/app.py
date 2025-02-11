from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from chatbot import RAG, LLMClient, MongoDBClient
from semantic_router import Route
from samples import product, chitchat
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.routers import SemanticRouter
import re
import dotenv
import os

# Ensure the script can find the .env file anywhere
dotenv.load_dotenv(dotenv.find_dotenv())
# Global variable to hold the RAG instance
global_rag = None

# Intialize the api key
mongodb_uri = os.getnv("MONGODB_URI")
api_key = os.getenv("GROQ_KEY")


def initialize_rag(api_key, mongodb_uri):
    llm = LLMClient(
        llm_name="llama-3.1-8b-instant",
        api_key=api_key,
    )
    db_name = "product"
    collection_name = "sendo"
    client = MongoDBClient(mongodb_uri, db_name, collection_name)
    collection = client.get_collection()
    rag_instance = RAG(collection=collection, llm_model=llm)
    rag_instance.remove_history()
    return rag_instance


def check_keywords(text: str, keywords: list) -> bool:
    # Convert text to lowercase for case-insensitive matching
    text = text.lower()

    # Create regex pattern from keywords
    pattern = "|".join(map(re.escape, keywords))

    # Return True if any keyword matches
    return bool(re.search(pattern, text))


def check_route(query):
    product_route = Route(name="product", utterances=product)
    chitchat_route = Route(name="chitchat", utterances=chitchat)
    routes = [product_route, chitchat_route]
    encoder = HuggingFaceEncoder()
    sr = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")
    result = sr(query)
    return result.name


def chatbot_response(query, rag):
    chat_history = rag.get_history()
    click_count = len(chat_history) // 2
    product_keywords = ["tìm", "gợi ý", "tư vấn"]
    search_result = []  # Initialize to avoid potential UnboundLocalError
    prompt = ""

    # Determine the route
    route = check_route(query)
    if (route == "chitchat" or route is None) and not check_keywords(query, product_keywords):
        return "Xin lỗi, tôi chỉ trả lời các câu hỏi liên quan đến shop BAN.", []

    if check_keywords(query, product_keywords) or click_count == 0:
        search_result = rag.hybrid_search(query=query, k=10)
        prompt = rag.create_prompt(search_results=search_result, query=query)
    else:
        prompt = query
    rag.update_history(role="user", content=prompt)
    response = rag.answer_query()
    print(len(rag.get_history()))
    if click_count >= 3:
        for _ in range(2):
            rag.remove_message()
    print(len(rag.get_history()))
    return response, search_result


# FastAPI application setup
origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    global global_rag
    global_rag = initialize_rag(api_key=api_key, mongodb_uri=mongodb_uri)


@app.get("/")
def read_root():
    return {"message": "Shop BAN"}


@app.get("/rag/")
async def read_item(q: str | None = None):
    global global_rag
    try:
        if not q:
            return {"result": "No query provided", "sources": []}

        # Process query and get response
        result, search_result = chatbot_response(
            rag=global_rag,
            query=q,
        )
        # for result in search_result:
        #     print(result['name'])
        # print(search_result)
        return {"result": result, "sources": search_result}

    except Exception as e:
        return {"error": str(e), "details": "An error occurred while processing the request."}
