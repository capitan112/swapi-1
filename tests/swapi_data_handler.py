import requests
import os


class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self):
        try:
            response = requests.get(self.base_url, verify=False)
            response.raise_for_status()
            return response
        except requests.RequestException:
            return 'ошибка запроса'
        except requests.ConnectionError:
            return 'сетевая ошибка'


class SWRequester(APIRequester):

    def __init__(self, base_url='https://swapi.py4e.com/api/'):
        super().__init__(base_url)

    def get_sw_categories(self):
        self.categories = list(self.get().json().keys())
        return self.categories

    def get_sw_info(self, category):
        if category in self.categories:
            category_url = self.base_url + f'/{category}/'
            response = requests.get(category_url, verify=False)
            return response.text

    def save_sw_data(self):
        sw_requester_instance = SWRequester()
        path = "data"
        os.makedirs(path, exist_ok=True)
        categories = sw_requester_instance.get_sw_categories()

        for category in categories:
            file = f'{category}.txt'
            response = sw_requester_instance.get_sw_info(category)
            file_path = path + '/' + file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f'{response} \n')


if __name__ == "__main__":
    sw_requester = SWRequester('https://swapi.dev/api/')
    categories = sw_requester.get_sw_categories()
    print(categories)
    category_response = sw_requester.get_sw_info(categories[1])
    print(category_response)
    sw_requester.save_sw_data()
