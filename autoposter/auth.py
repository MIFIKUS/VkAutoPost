import vk_api
import json

class Login:
    def __init__(self):
        self._token = self._get_token()
        self._session = vk_api.VkApi(token=self._token, scope='offline')
        self.vk = self._session.get_api()

    def _get_token(self):
        with open('service_files/vk.json') as vk_cnf:
            return json.load(vk_cnf).get('TOKEN')

    def get_vk(self):
        return self.vk

    def get_session(self):
        return self._session