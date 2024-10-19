import pytest

def pytest_collection_modifyitems(items):
    for item in items:
        print("printq", item.name)
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "structure" in item.name:
            item.add_marker(pytest.mark.model_structure)