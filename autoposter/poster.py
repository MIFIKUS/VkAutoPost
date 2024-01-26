import vk_api

class MakePost:
    def __init__(self, vk, session):
        self._vk = vk
        self._session = session

    def make_post(self, id, text):
        upload = vk_api.upload.VkUpload(self._session)

        photo = ['tg_bot/post/post_photo.jpg']

        photo_list = upload.photo_wall(photo)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
        self._vk.wall.post(owner_id=id, message=text, attachments=attachment)


class Subscribe:
    def __init__(self, vk, session):
        self._vk = vk
        self._session = session

    def subscribe(self, id):
        self._vk.groups.join(group_id=abs(id))
