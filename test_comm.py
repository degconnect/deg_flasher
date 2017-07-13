#!/usr/bin/env python

from comm import get_modded, save_backup


def test_get_modded():

    d = {'vram-size': 4, 'memory': 'SK Hynix', 'rom-size': 4, 'bios-version': '113-1E366FU-S4J', 'model_1': 'RX 580'}

    #             "model_1": "RX 580",
    #             "memory": "SK Hynix",
    #             "vram_size": 4,
    #             "rom_size": 4,
    #             "flash_type": "M25P20/c",
    #             "bios_version": "113-1E366FU-S4J"

    ret = get_modded(d)

    print ret


def test_backup():
    card = {'vram-size': 4, 'memory': 'SK Hynix', 'rom-size': 8, 'bios-version': '113-1E366FU-S4J', 'model_1': 'RX 580',
            'ssid': '6361', 'generic_model': 'Ellesmere', 'flash-type': 'M25P20/c'}
    save_backup('RX-580-4GB-SK-Hynix-4GB-ROM-113-1E366FU-S4J.rom', card)


def main():
    test_backup()


if __name__ == "__main__":
    main()

