
def get_id_by_link(vk, link):

    link = link.replace(' ', '')
    link = link.replace('https://', '')
    link = link.replace('vk.com/', '')
    link = link.replace('/', '')
    link = link.replace('set_receivers', '')
    print(link)

    if len(link) == 0:
        return ''
    group_info = vk.method('utils.resolveScreenName', {'screen_name': link})

    if group_info['type'] == 'group':
        group_info['object_id'] *= -1
    print(group_info)
    return group_info['object_id']

