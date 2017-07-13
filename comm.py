import requests
import urllib


def get_modded(card):
    """
    d = {'vram_size': 4, 'memory': 'SK Hynix', 'rom_size': 4, 'bios_version': '113-1E366FU-S4J', 'model_1': 'RX 580'}
    http://panels.degconnect.com/api/v1/core/rom-moddeds/?vram_size=4&memory=SK%20Hynix&rom_size=4&bios_version=113-1E366FU-S4J&model_1=RX%20580
    :return:
    """
    domain = 'flasher.degconnect.com'
    url = 'http://{}/api/v1/core/rom-moddeds/'.format(domain)
    params = {'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
              'bios_version': card['bios-version'], 'model_1': card['model_1']}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            download_url = data[0]['download_url']
            url = 'http://{}/{}'.format(domain, download_url)
            lst = url.split('/')
            if lst:
                name = 'modded-{}'.format(lst[-1])
                urllib.urlretrieve (url, name)
                return name
