import os

import requests


class OrangoException(Exception):
    def __init__(self, result, stderr):
        self.result = result
        self.stderr = stderr
        super().__init__(self.stderr)

class Sandbox:
    def __init__(self, base_url: str, api_key: str, template_id: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.template_id = template_id
        self.session_id = None

    @classmethod
    def create(cls, api_key: str = None, template_id: str = None, base_url: str = None):
        api_key = api_key or os.getenv('ORANGO_APIKEY')
        if not api_key:
            raise ValueError("API key must be provided either as an argument or through the ORANGO_APIKEY environment variable.")

        base_url = base_url or os.getenv('ORANGO_BASE_URL') or 'https://orango.ai/api/v1'
        return cls(base_url, api_key, template_id)

    def exec(self, code: str):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        payload = {
            'code': code,
            'language': 'python',
            'env': {},
            'sessionId': self.session_id,
            # 'templateId': self.template_id,
        }
        response = requests.post(f'{self.base_url}/execute', json=payload, headers=headers)
        response_data = response.json()

        self.session_id = response_data.get('sessionId')

        if response_data.get('stderr'):
            raise OrangoException(response_data, response_data.get('stderr'))

        return response_data

    def close(self):
        # Optionally, close the sandbox or clean up resources
        pass
