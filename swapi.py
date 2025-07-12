import requests
from urllib.parse import urljoin
from pathlib import Path


def save_sw_data():
    path = Path("data")
    path.mkdir(exist_ok=True)
    sw_requester_instance = SWRequester('https://swapi.py4e.com/api')
    # sw_requester_instance = SWRequester('https://swapi.dev/api')
    categories = list(sw_requester_instance.get_sw_categories())
    for category in categories:
        file = f'{category}.txt'
        response = sw_requester_instance.get_sw_info(category)
        print(response)
        with open(f"{path}/{file}", "w") as file:
            file.write(f'{response} \n')


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint=''):
        full_url = urljoin(self.base_url.rstrip('/') + '/',
                           endpoint.lstrip('/'))
        try:
            response = requests.get(full_url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            print('Возникла ошибка при выполнении запроса')


class SWRequester(APIRequester):

    def __init__(self, base_url='https://swapi.py4e.com/'):
        super().__init__(base_url)

    def get_sw_categories(self, endpoint=''):
        return self.get(endpoint).json().keys()

    def get_sw_info(self, sw_type):
        return self.get(f'{sw_type}/').text


if __name__ == "__main__":
    save_sw_data()
    # sw_requester = SWRequester('https://swapi.py4e.com/')
    # categories = list(sw_requester.get_sw_categories('/api/'))
    # print(categories[1])
    # category_response = sw_requester.get_sw_info('/api/' + categories[1])
    # print(category_response)
