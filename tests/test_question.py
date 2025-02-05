from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_question(test_params):
    """Test API with file and question based on command-line parameters."""
    file_path = test_params.get("file_path")  
    question = test_params.get("question")

    files = {}
    file = None  

    if file_path:
        file = open(file_path, "rb")  
        files = {"file": file}

    response = client.post(
        "/question/",
        files=files,
        data={"question": question}
    )

    if file:  
        file.close()

    json_response = response.json()
    print("Response:", json_response)

    if question and file_path:
        assert "answer" in json_response
    elif question:
        assert "answer" in json_response
    elif file_path:
        assert "document_id" in json_response
    else:
        assert response.status_code == 400  
