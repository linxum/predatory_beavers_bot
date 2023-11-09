import requests
import urllib as u

token = 'ccd39cf5ccd39cf5ccd39cf53ecfc5a0d8cccd3ccd39cf5a9984d97bd8f92cf358bbd91'
ver = 5.126
count = 1
offset = 0


def get_post(domain):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': ver,
                                'domain': domain,
                                'offset': offset,
                                'count': count
                            }
                            )
    return response.json()['response']['items'][0]


def get_post_text(domain):
    return get_post(domain)['text']

def get_post_photos(domain):
    urls = []
    post = get_post(domain)['attachments']
    for attachment in post:
        if attachment['type'] == 'photo':
            urls.append(attachment['photo']['sizes'][-1]['url'])
    return urls


def get_post_video(domain):
    urls = []
    post = get_post(domain)['attachments']
    for attachment in post:
        if attachment['type'] == 'video':
            urls.append("https://vk.com/video?z=video" + str(attachment['video']['owner_id']) + '_' + str(attachment['video']['id']))
    return urls


def url_to_png(urls):
    names = []
    count_url = 1
    for url in urls:
        name = str(count_url) + ".png"
        f = open(name, 'w+b')
        f.write(u.request.urlopen(url).read())
        f.close
        names.append(name)
        count_url += 1
    return names

