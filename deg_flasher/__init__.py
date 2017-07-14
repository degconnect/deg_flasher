from .amddetect import can_be_flash, get_cards, backup, flash


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
    for card in flash_list:
        backup(card)
        flash(card)

    print "Done!!!"

if __name__ == "__main__":
    amd_flash()
