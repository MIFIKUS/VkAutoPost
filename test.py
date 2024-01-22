from autoposter.auth import Login
from autoposter.poster import MakePost
from autoposter.get_id import get_id_by_link
from logger.logs import Logs

import vk_api

login = Login()

vk = login.get_vk()
sesion = login.get_session()
v

get_id_by_link(sesion, 'https://vk.com/animescale')
