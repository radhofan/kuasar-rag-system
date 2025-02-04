from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_question():
    test_file_path = "samples/md/FASTAPI_README.md"

    with open(test_file_path, "rb") as file:
        response = client.post(
            "/question/",
            files={"file": file},
            data={"question": "What is FastAPI?"}
        )

    json_response = response.json()
    print("Answer:", json_response.get("answer", "No answer found"))
    print("Document ID:", json_response.get("document_id", "No document ID found"))

    assert "answer" in json_response
    assert "document_id" in json_response

