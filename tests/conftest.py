import pytest

# Custom Parameters for Pytest
def pytest_addoption(parser):
    parser.addoption("--file", action="store", default=None, help="Path to the document file")
    parser.addoption("--question", action="store", default="", help="Question to ask")

@pytest.fixture
def test_params(request):
    return {
        "file_path": request.config.getoption("--file"),
        "question": request.config.getoption("--question"),
    }

