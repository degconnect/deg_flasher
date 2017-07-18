import requests
import urllib

import os

DOMAIN = os.environ.get('DOMAIN', 'flasher.degconnect.com')


def get_modded(card, auth):
    """
    d = {'vram_size': 4, 'memory': 'SK Hynix', 'rom_size': 4, 'bios_version': '113-1E366FU-S4J', 'model_1': 'RX 580'}
    http://flasher.degconnect.com/api/v1/core/rom-moddeds/?vram_size=4&memory=SK%20Hynix&rom_size=4&bios_version=113-1E366FU-S4J&model_1=RX%20580
    :return:
    """

    url = 'http://{}/api/v1/core/rom-moddeds/'.format(DOMAIN)
    params = {'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
              'bios_version': card['bios-version'], 'model_1': card['model-1']}
    headers = {'accept': 'application/json'}
    resp = requests.get(url, params=params, auth=auth, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            download_url = data[0]['download_url']
            url = 'http://{}{}'.format(DOMAIN, download_url)
            lst = url.split('/')
            if lst:
                name = 'modded-{}'.format(lst[-1])
                urllib.urlretrieve (url, name)
                return name
    elif resp.status_code == 403:
        data = resp.json()
        if data["detail"] == "You don't have enough credits to get a MODDED ROM.":
            print data["detail"]

    else:
        print "It went wrong trying to get the modded ROM from our servers"
        print "Status Code:", resp.status_code
        print "Response:", resp.content


def save_backup(filename, card, auth):
    url = 'http://{}/api/v1/core/user-backups/'.format(DOMAIN)
    data = {'ssid': card['ssid'], 'generic_model': card['model'],
            'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
            'bios_version': card['bios-version'], 'model_1': card['model-1'], 'flash_type': card['flash-type'],
           }
    files = {'content': open(filename, 'rb')}
    resp = requests.post(url, data=data, files=files, auth=auth)
    if resp.status_code == 200:
        data = resp.json()
        print data
    elif resp.status_code == 500:
        f = open('error.html', 'w')
        f.write(resp.content)
        f.close()
    elif resp.status_code == 201:
        print "Backup saved to Degconnect.com servers"
    else:
        print "It went wrong trying to backup your ROM to our servers"
        print "Status Code:", resp.status_code
        print "Response:", resp.content


def get_credits(auth):
    url = 'http://{}/api/v1/core/credits'.format(DOMAIN)
    headers = {'accept': 'application/json'}
    resp = requests.get(url, auth=auth, headers=headers)
    if resp.status_code == 200:
        r = resp.json()
        return r['credits']
    else:
        print "Your credentials are wrong!!!"
