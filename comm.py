import requests
import urllib

import os

DOMAIN = os.environ.get('DOMAIN', 'flasher.degconnect.com')

DEFAULT_USER = os.environ.get('DEFAULT_USER')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')


def get_modded(card):
    """
    d = {'vram_size': 4, 'memory': 'SK Hynix', 'rom_size': 4, 'bios_version': '113-1E366FU-S4J', 'model_1': 'RX 580'}
    http://panels.degconnect.com/api/v1/core/rom-moddeds/?vram_size=4&memory=SK%20Hynix&rom_size=4&bios_version=113-1E366FU-S4J&model_1=RX%20580
    :return:
    """

    url = 'http://{}/api/v1/core/rom-moddeds/'.format(DOMAIN)
    params = {'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
              'bios_version': card['bios-version'], 'model_1': card['model_1']}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            download_url = data[0]['download_url']
            url = 'http://{}/{}'.format(DOMAIN, download_url)
            lst = url.split('/')
            if lst:
                name = 'modded-{}'.format(lst[-1])
                urllib.urlretrieve (url, name)
                return name


def save_backup(filename, card):
    url = 'http://{}/api/v1/core/user-backups/'.format(DOMAIN)
    data = {'ssid': card['ssid'], 'generic_model': card['model'],
            'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
            'bios_version': card['bios-version'], 'model_1': card['model-1'], 'flash_type': card['flash-type'],
           }
    files = {'content': open(filename, 'rb')}
    resp = requests.post(url, data=data, files=files, auth=(DEFAULT_USER, DEFAULT_PASSWORD), )
    if resp.status_code == 200:
        data = resp.json()
        print data
    elif resp.status_code == 500:
        f = open('error.html', 'w')
        f.write(resp.content)
        f.close()
    elif resp.status_code == 201:
        print "Backup saved to Deconnect.com servers"
