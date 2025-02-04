from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_question_text_only():
    response = client.post(
        "/question/",
        data={"question": "What is Fast API?"}  
    )

    
    json_response = response.json()
    print("Answer:", json_response.get("answer", "No answer found"))

    assert "answer" in json_response
