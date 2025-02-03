from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_question():
    # Prepare test file (use a small sample PDF or markdown)
    test_file_path = "samples/md/FASTAPI_README.md"

    # Open the test file and send request
    with open(test_file_path, "rb") as file:
        response = client.post(
            "/question/",
            files={"file": file},
            data={"question": "What is FastAPI?"}
        )

    # Print response content
    # print("Response Status Code:", response.status_code)
    # print("Response Text:", response.text)

    # # Check response status
    # assert response.status_code == 200, response.text

    # Parse JSON response
    json_response = response.json()
    print("Answer:", json_response.get("answer", "No answer found"))
    print("Document ID:", json_response.get("document_id", "No document ID found"))

    # Check if response has expected fields
    assert "answer" in json_response
    assert "document_id" in json_response

