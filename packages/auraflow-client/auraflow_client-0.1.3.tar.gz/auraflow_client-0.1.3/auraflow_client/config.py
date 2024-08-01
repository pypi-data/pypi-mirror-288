import os
from dotenv import load_dotenv


def get_api_key():
    """Retrieve API Key from environment variables."""
    load_dotenv(verbose=True)
    key = os.getenv('AURAFLOW_API_KEY')

    if key is None:
        raise EnvironmentError("AURAFLOW_API_KEY not found. Please set the AURAFLOW_API_KEY environment variable.")

    return key
