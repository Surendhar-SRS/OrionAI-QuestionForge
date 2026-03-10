import os
import sys
import importlib

# Ensure backend directory is in the path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

def test_secret_key_randomness():
    # Make sure we don't have the environment variable set
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]

    # Importing the config
    from app.core import config
    importlib.reload(config)

    key1 = config.settings.SECRET_KEY
    print(f"Key 1: {key1}")

    # The old hardcoded value
    OLD_SECRET_KEY = "super-secret-key-change-it-in-prod"
    assert key1 != OLD_SECRET_KEY, "SECRET_KEY is still the insecure hardcoded default!"
    assert len(key1) >= 32, "SECRET_KEY should be at least 32 characters long."

    # Reload to check if it's re-read (it will be different if reloaded because of the class definition logic)
    importlib.reload(config)
    key2 = config.settings.SECRET_KEY
    print(f"Key 2: {key2}")

    assert key1 != key2, "SECRET_KEY should be re-generated for each reload of the config module if no ENV var is set"

def test_secret_key_from_env():
    # Test that it respects the environment variable
    TEST_KEY = "my-test-secret-key-that-is-longer-than-32-chars-long"
    os.environ["SECRET_KEY"] = TEST_KEY

    from app.core import config
    importlib.reload(config)

    assert config.settings.SECRET_KEY == TEST_KEY, "SECRET_KEY should be read from the environment variable"
    print(f"Key from ENV: {config.settings.SECRET_KEY}")

if __name__ == "__main__":
    try:
        test_secret_key_randomness()
        test_secret_key_from_env()
        print("All security configuration tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
