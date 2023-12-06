import os
import urllib as u
import re
import requests

import tokens

ver = 5.126
count = 2
offset = 0


def get_post(domain):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': tokens.vk_token(),
                                'v': ver,
                                'domain': domain,
                                'offset': offset,
                                'count': count
                            }
                            )
    if not 'is_pinned' in response.json()['response']['items'][0]:
        return response.json()['response']['items'][0]
    else:
        return response.json()['response']['items'][1]


def get_post_text(domain):
    text = get_post(domain)['text']
    ids = re.finditer(r'\[id\d+\|([^\]]+)\]', text)
    for id in ids:
        text = text.replace(id.group(), id.group(1))
    clubs = re.finditer(r'\[club\d+\|([^\]]+)\]', text)
    for club in clubs:
        text = text.replace(club.group(), club.group(1))
    return text


def get_post_photos(domain):
    urls = []
    post = get_post(domain)['attachments']
    for attachment in post:
        if attachment['type'] == 'photo':
            urls.append(attachment['photo']['sizes'][-1]['url'])
    pngs = url_to_png(urls)
    return pngs


def get_post_video(domain):
    urls = []
    post = get_post(domain)['attachments']
    for attachment in post:
        if attachment['type'] == 'video':
            urls.append("https://vk.com/video?z=video" + str(attachment['video']['owner_id']) + '_' + str(attachment['video']['id']))
    return urls


def url_to_png(urls):
    names = []
    for url in urls:
        name = "img/" + str(urls.index(url)) + ".png"
        f = open(name, 'w+b')
        f.write(u.request.urlopen(url).read())
        f.close
        names.append(name)
    return names


def delete_files(pngs):
    for png in pngs:
        os.remove(png)
