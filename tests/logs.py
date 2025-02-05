
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_logs():
    try:
        response = client.get("/logs/")

        if response.status_code == 200:
            log_content = response.json()
            print(f"Response Body: {log_content}")
        
        else:
            print(f"Error: Failed to retrieve logs with status code {response.status_code}")
            print(f"Error Details: {response.text}")
        
        return response.json()

    except Exception as e:
        print(f"An exception occurred: {e}")
        return {"error": str(e)}

