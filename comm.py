import requests


def get_modded(card):
    '''
    d = {'vram_size': 4, 'memory': 'SK Hynix', 'rom_size': 4, 'bios_version': '113-1E366FU-S4J', 'model_1': 'RX 580'}
    http://localhost:8000/api/v1/core/rom-moddeds/?vram_size=4&memory=SK%20Hynix&rom_size=4&bios_version=113-1E366FU-S4J&model_1=RX%20580
    :return:
    '''
    domain = 'localhost:8000'
    url = 'http://{}/api/v1/core/rom-moddeds/'.format(domain)
    params = {'vram_size': card['vram-size'], 'memory': card['memory'], 'rom_size': card['rom-size'],
              'bios_version': card['bios-version'], 'model_1': card['model_1']}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        print "data:", data
        if data:
            # "download_url": "downloads/modded/2017/07/12/x.rom"
            download_url = data[0]['download_url']
            url = 'http://{}/{}'.format(domain, download_url)
            print url
