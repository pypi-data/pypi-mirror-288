import unittest
from auraflow_client.api import get_data


class TestAPI(unittest.TestCase):
    def test_get_data(self):
        dummy_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmRlcl9pZCI6IkdYWVdKUkRSWkgiLCJhcGlfc2VjcmV0IjoiMWZhZGM3OWQtM2NiYy00NzI2LTkyYzgtYzExYTRhZGNjZDA1In0.IaoRNmblu-F3PtL6xge4H0Z3t_DOi1BVP1uwEmJD5C4'
        body = {
            'ticker_list': ['^GSPC'],
            "start": '2020-01-01',
            "end": '2023-01-01',
            "source": 'yahoo',
            "data_format": 'json'
        }

        response = get_data(dummy_api_key, body)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
