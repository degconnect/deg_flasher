#!/usr/bin/env python

import subprocess
import os
import getpass

from deg_flasher.comm import get_modded, save_backup, get_credits


DEFAULT_USER = os.environ.get('DEFAULT_USER')
DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')


def get_vrams():
    proc = subprocess.Popen(['vram'], stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if not err:
        ret = out[:-1] if out[-1] == '\n' else out
        return ret.split(' ')
    return ""


def get_from_atiflash():
    proc = subprocess.Popen(['sudo', 'atiflash', '-i'], stdout=subprocess.PIPE)
    out, err = proc.communicate()

    lst = out.splitlines()
    ret = []
    for s in lst[3:]:
        row = [l for l in s.split(' ') if l]
        rom_size = int(row[6])/10000
        ret.append({
            'ssid': row[3],
            'model': row[4],
            'flash-type': row[5],
            'rom-size': rom_size,
            'bios-version': row[8],
        })
    return ret


def stripped(s):
    bad = ['[', ']']
    for ch in bad:
        s = s.replace(ch, '')
    return s.strip()


def get_gpu_list():
    proc = subprocess.Popen(['gpu-info'], stdout=subprocess.PIPE)
    out, err = proc.communicate()

    proc1 = subprocess.Popen(['sudo', 'amdmeminfo', '-o', '-s', '-q'], stdout=subprocess.PIPE)
    out1, err1 = proc1.communicate()

    lst1 = out.splitlines()
    lst2 = out1.splitlines()
    ret = []
    for l, m in zip(lst1, lst2):
        lst = l.split(' ')
        model = ' '.join(lst[2:4])
        memory = m.split(':')[4]
        memory = memory.split('-')[0].split(' ')[:-1]
        memory = ' '.join(memory)
        ret.append(
            (lst[0], lst[1], stripped(model), memory)
        )
    return ret


def get_cards():
    vrams = get_vrams()
    cards = get_from_atiflash()
    gpus = get_gpu_list()
    ret = []
    for card, vram, gpu in zip(cards, vrams, gpus):
        card['vram-size'] = vram
        card['id'] = gpu[0]
        card['model-1'] = gpu[2]
        card['memory'] = gpu[3]
        ret.append(card)
    return ret


def can_be_flash(card):
    return card['model'] == 'Ellesmere'


def gen_rom_filename(card):
    mem_size = card['vram-size']
    rom_size = card['rom-size']
    bios_version = card['bios-version']
    bios_version = bios_version.replace('.', '-')
    ret = "{}-{}GB-{}-{}GB-ROM-{}.rom".format(card['model-1'], mem_size, card['memory'], rom_size, bios_version)
    ret = ret.replace(' ', '-')
    return ret


def backup(card, auth):
    """
    :param card:
    :param auth  tuple with email and password
    :return:
    backup ROM using ATIFLASH and send the backup to our servers
    todo: send backup to server attached to the machine that generated it
    """
    filename = gen_rom_filename(card)
    print "Backup card: {0}: {1} to file: {2}".format(card['ix'], card['model-1'], filename)
    proc = subprocess.Popen(['sudo', 'atiflash', '-s', str(card['ix']), filename], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print out
    if err:
        print "err:", err
    else:
        save_backup(filename, card, auth)


def real_flash(filename, card_index):
    proc = subprocess.Popen(['sudo', 'atiflash', '-p', str(card_index), filename], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print out
    if err:
        print "err:", err


def flash(card, auth):
    """
    :param card:
    :return:
    get the modded ROM from our servers and flash into the card using atiflash
    """
    msg = "Press any key for flashing card: {0} -> {1}. Press S<ENTER> for skip this card.".format(card['ix'], card['model-1'])
    ret = raw_input(msg)
    print
    print "="*40
    print
    if ret not in ['s', 'S']:
        filename = get_modded(card, auth)
        if filename:
            print "Flashing!!!!"
            real_flash(filename, card['ix'])
        elif filename == 403:
            msg = "In order to buy more credit you can go to http://flasher.degconnect.com/buy.\nThanks."
            print msg
            exit()
        else:
            print "The modded ROM is not ready just yet."
            print "We will modify this ROM as soon as possible and notify you when it is ready so you can re-run it."
            print "Please, allow 1 business day before contacting us."
    print


def get_username_password():
    email = raw_input("Type your email followed by ENTER key ")
    password = getpass.getpass('Enter your password followed by ENTER key ')
    return email, password


def amd_flash():
    print "DEG Flasher only works for Ellesmere RX 470/480/570/580"
    print "Please, remember to put all the cards in OC Mode. Check that and stop this if not in OC Mode."
    print "Stop mining or using your cards in any way before using this software!!!"
    ret = raw_input("Press Q to Quit and other key to continue: ")
    ret = ret.lower().strip()
    if ret in ['q', 'quit']:
        print "Bye"
        return
    print "Detecting all cards"

    cards = get_cards()
    flash_list, unknown = [], []
    ix = 0
    print "#\tModel\tFlash Type\tROM Size\tMemory Type\tVRAM Size\tBios Version"
    for card in cards:
        card['ix'] = ix
        ix += 1
        if can_be_flash(card):
            flash_list.append(card)
        else:
            unknown.append(card)
        print "{}\t{}\t{}\t{}\t\t{}\t\t{}\t{}".format(card['ix'], card['model-1'], card['flash-type'],
                                                      card['rom-size'], card['memory'], card['vram-size'],
                                                      card['bios-version'])
    if len(flash_list) == len(cards):
        print "Good News!!!\nAll your cards can be modded!!!!"
    elif flash_list:
        print "Not all your cards can be modded!\nWe only can flash AMD RX 470/480/570/580."
    else:
        print "Bad news.\nSorry, no card can be modded.\nWe only can flash AMD RX 470/480/570/580."
        return
    print
    if DEFAULT_USER:
        auth = (DEFAULT_USER, DEFAULT_PASSWORD)
    else:
        auth = get_username_password()
    card_credits = get_credits(auth)
    if card_credits is not None:
        for card in flash_list:
            backup(card, auth)
            flash(card, auth)

    print "Done!!!"


def main():
    amd_flash()

if __name__ == "__main__":
    main()
