from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app, chatbot_response

client = TestClient(app)


def test_read_item_no_query():
    response = client.get("/rag/")
    assert response.status_code == 200
    assert response.json() == {"result": "No query provided", "sources": []}


@patch("app.global_rag")
def test_read_item_product_query(mock_global_rag):
    mock_rag_instance = MagicMock()
    mock_global_rag.return_value = mock_rag_instance
    mock_rag_instance.hybrid_search.return_value = [{"name": "Product 1"}, {"name": "Product 2"}]
    mock_rag_instance.create_prompt.return_value = "Prompt for product query"
    mock_rag_instance.answer_query.return_value = "Response for product query"

    response = client.get("/rag/?q=tìm sản phẩm giày")
    assert response.status_code == 200
    assert response.json() == {
        "result": "Response for product query",
        "sources": [{"name": "Product 1"}, {"name": "Product 2"}],
    }

    mock_rag_instance.hybrid_search.assert_called_once_with(query="tìm sản phẩm giày", k=10)
    mock_rag_instance.create_prompt.assert_called_once()
    mock_rag_instance.answer_query.assert_called_once()


@patch("app.check_route")
@patch("app.check_keywords")
def test_chatbot_response_chitchat(mock_check_keywords, mock_check_route):
    # Arrange
    mock_check_route.return_value = "chitchat"
    mock_check_keywords.return_value = False
    mock_rag = MagicMock()
    query = "How are you doing today?"

    # Act
    response, search_result = chatbot_response(query, mock_rag)

    # Assert
    assert response == "Xin lỗi, tôi chỉ trả lời các câu hỏi liên quan đến shop BAN."
    assert search_result == []
    mock_check_route.assert_called_once_with(query)
    mock_check_keywords.assert_called_once_with(query, ["tìm", "gợi ý", "tư vấn"])
    mock_rag.get_history.assert_called_once()
    mock_rag.hybrid_search.assert_not_called()
    mock_rag.create_prompt.assert_not_called()
    mock_rag.update_history.assert_not_called()
    mock_rag.answer_query.assert_not_called()
    mock_rag.remove_message.assert_not_called()
