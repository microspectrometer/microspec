import pytest

@pytest.fixture(scope="class")
def class_results(request):
  request.cls.results = [["Command", "Time(ms)"]]

