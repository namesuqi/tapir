# coding=utf-8
"""
create peer_id_file
"""

import os


PEER_ID_FILE = "/peer_id1.txt"


class Creator(object):
    @staticmethod
    def create_peer_ids(peer_id_nums=100000, peer_id_file=PEER_ID_FILE):
        file1 = open(os.path.abspath(os.path.dirname(__file__)) + peer_id_file, "w")
        m = 1000000
        file1.write('[')
        for i in range(int(peer_id_nums)):
            file1.write('"1234567801ABCDEABCDEABCDE{0}",\n'.format(m))
            # file1.flush()
            m += 1
        file1.write('"0"]')
        file1.close()


if __name__ == '__main__':
    Creator.create_peer_ids()
    pass

