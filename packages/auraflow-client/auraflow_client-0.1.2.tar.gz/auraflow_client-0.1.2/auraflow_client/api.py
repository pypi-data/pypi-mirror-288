from auraflow_client import get_api_key
import requests
import ast


def construct_data(dict_string):
    data_ = {}
    try:
        data_obj = ast.literal_eval(dict_string)
        if not isinstance(data_obj, dict):
            raise ValueError("The input is not a valid dictionary.")

        desired_keys = ['API_KEY', 'data']

        for key, value in data_obj.items():
            if key in desired_keys:
                data_[key] = value

    except (SyntaxError, ValueError) as ex:
        raise ValueError(f'Invalid data: {ex}')

    return data_


def fetch_data():
    data_string = input('Enter data: ')
    data_dict = construct_data(data_string)

    api_key = data_dict.get('API_KEY')
    data = data_dict.get('data')

    return api_key, data


def get_data(api_key=None, data=None):
    if api_key is None and data is None:
        api_key, data = fetch_data()

    if api_key is None:
        raise ValueError('API_KEY not found. Please set the API_KEY environment variable or Enter API_KEY as input data')

    """Fetch data from AuraFlow API."""
    url = 'https://auraflow.unbiased-alpha.com/api/open_api/get_data'
    headers = {'Authorization': f'Bearer {api_key}'}

    response = requests.post(url, headers=headers, data=data)

    return response.json(), response.status_code
