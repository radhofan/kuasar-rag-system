import pytest

# Define the pytest_addoption function
def pytest_addoption(parser):
    """Add custom command-line options to pytest."""
    parser.addoption("--file", action="store", default=None, help="Path to the document file")
    parser.addoption("--question", action="store", default="", help="Question to ask")

# Define the fixture
@pytest.fixture
def test_params(request):
    """Fixture to get file path and question from command line."""
    return {
        "file_path": request.config.getoption("--file"),
        "question": request.config.getoption("--question"),
    }
