import requests

class sellgate:
    def __init__(self):
        self.base_url = "https://api.sellgate.io/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            response_data = response.json()
            if response_data.get('success'):
                return response_data
            else:
                error_message = response_data.get('message', 'Unknown error')
                raise Exception(f"API request failed: {error_message}")
        except requests.exceptions.HTTPError as e:
            response = e.response
            error_message = response.json().get('message', 'Unknown error')
            raise Exception(f"API request failed: {error_message}")
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def create_checkout(self, checkout_request):
        if isinstance(checkout_request, dict):
            return self._make_request("POST", "checkout", data=checkout_request)
        else:
            raise ValueError("checkout_request must be a dictionary")

    def create_address(self, address_request):
        if isinstance(address_request, dict):
            return self._make_request("POST", "address", data=address_request)
        else:
            raise ValueError("address_request must be a dictionary")