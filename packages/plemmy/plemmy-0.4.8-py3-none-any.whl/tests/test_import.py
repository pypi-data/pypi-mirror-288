import pytest


def test_import():

    try:
        import plemmy
    except ModuleNotFoundError as ex:
        pytest.fail(f"{ex}")
