from bsor.Bsor import make_bsor, make_info
from bsor.Scoring import calc_stats
import logging

import faulthandler

if __name__ == '__main__':
    import os

    #faulthandler.enable()
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Started')

    # example, read basic info from bsor file
    filename = 'D:/_TMP/easy.bsor'
    print(f'File name :    {os.path.basename(filename)}')

    from bsor.BsorUtil import *

    with open(filename, "rb") as f:
        print("make")
        m = make_bsor(f)

        m.info.playerId = '76561198026425351'
        m.info.playerName = 'Schippi'
        print("write to file")
        with open('D:/_TMP/easy_Schippi.bsor', 'wb') as fo:
            m.write(fo)

        stats = calc_stats(m)
        print(f'BSOR Version:  {m.file_version}')
        print(f'BSOR notes: {len(m.notes)}')
        print(f'BSOR stats: {stats}')
        with open('D:/_TMP/replay.json', 'w') as fi:
            fi.write(str(m))

    exit(9)
    #my_playlist = clan_playlist('GER', count=60, stars_from=4, stars_to=10, include_to_hold=False, unplayed_player=76561198026425351)
    my_playlist = unplayed_list(unplayed_player=76561198026425351, count=1200, stars_from=4, stars_to=10)
    with open('D:/_TMP/76561198026425351.bplist', 'w') as f:
        f.write(json.dumps(my_playlist, indent=2))
    #print(my_playlist)
