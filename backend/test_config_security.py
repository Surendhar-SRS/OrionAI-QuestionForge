import os
import sys
import importlib

# Ensure backend directory is in the path
sys.path.append(os.path.join(os.getcwd(), "backend"))


def test_secret_key_missing():
    # Make sure we don't have the environment variable set
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    try:
        from app.core import config

        importlib.reload(config)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "SECRET_KEY environment variable must be set" in str(e)


def test_secret_key_from_env():
    # Test that it respects the environment variable
    TEST_KEY = "my-test-secret-key-that-is-longer-than-32-chars-long"
    os.environ["SECRET_KEY"] = TEST_KEY

    from app.core import config

    importlib.reload(config)

    assert config.settings.SECRET_KEY == TEST_KEY, (
        "SECRET_KEY should be read from the environment variable"
    )
    print(f"Key from ENV: {config.settings.SECRET_KEY}")


if __name__ == "__main__":
    try:
        test_secret_key_missing()
        test_secret_key_from_env()
        print("All security configuration tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
