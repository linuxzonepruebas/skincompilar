# Embedded file name: /usr/lib/enigma2/python/Components/Converter/MaggyEmuName.py
from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll
import os

class MaggyEmuName(Poll, Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 2000
        self.poll_enabled = True

    @cached
    def getText(self):
        info = ''
        info2 = ''
        camdname = None
        cardname = None
        if fileExists('/tmp/.emu.info'):
            try:
                camdname = open('/tmp/.emu.info', 'r')
            except:
                camdname = None

        elif fileExists('/etc/startcam.sh'):
            try:
                for line in open('/etc/startcam.sh'):
                    if line.find('script') > -1:
                        camdname = '%s' % line.split('/')[-1].split()[0][:-3]

            except:
                camdname = None

        elif fileExists('/etc/CurrentBhCamName'):
            try:
                camdname = open('/etc/CurrentBhCamName', 'r')
            except:
                camdname = None

        elif fileExists('/etc/active_emu.list'):
            try:
                camdname = open('/etc/active_emu.list', 'r')
            except:
                camdname = None

        elif fileExists('/tmp/cam.info'):
            try:
                camdname = open('/tmp/cam.info', 'r')
            except:
                camdname = None

        elif fileExists('/etc/clist.list'):
            try:
                camdname = open('/etc/clist.list', 'r')
            except:
                camdname = None

        elif fileExists('/etc/init.d/softcam') or fileExists('/etc/init.d/cardserver'):
            try:
                camdname = os.popen('/etc/init.d/softcam info')
            except:
                camdname = None

            try:
                cardname = os.popen('/etc/init.d/cardserver info')
            except:
                camdname = None

        if cardname is not None:
            for line in cardname:
                if line.lower().find('oscam') > -1:
                    info2 = 'oscam'
                elif line.lower().find('newcs') > -1:
                    info2 = 'newcs'
                elif line.lower().find('wicard') > -1:
                    info2 = 'wicardd'
                elif line.lower().find('cccam') > -1:
                    info2 = 'cccam'
                else:
                    info2 = ''

            cardname.close()
        if camdname is not None:
            for line in camdname:
                if line.lower().find('mgcamd') > -1 and line.lower().find('oscam') > -1:
                    info = 'oscammgcamd'
                    break
                if line.lower().find('cccam') > -1 and line.lower().find('oscam') > -1:
                    info = 'oscamcccam'
                    break
                elif line.lower().find('mgcamd') > -1:
                    info = 'mgcamd'
                elif line.lower().find('oscam') > -1:
                    info = 'oscam'
                elif line.lower().find('wicard') > -1:
                    info = 'wicardd'
                elif line.lower().find('cccam') > -1:
                    info = 'cccam'
                elif line.lower().find('camd3') > -1:
                    info = 'camd3'
                elif line.lower().find('evocamd') > -1:
                    info = 'evocamd'
                elif line.lower().find('newcs') > -1:
                    info = 'newcs'
                elif line.lower().find('rqcamd') > -1:
                    info = 'rqcamd'
                elif line.lower().find('gbox') > -1:
                    info = 'gbox'
                elif line.lower().find('mpcs') > -1:
                    info = 'mpcs'
                elif line.lower().find('sbox') > -1:
                    info = 'sbox'
                elif line.lower().find('scam') > -1:
                    info = 'scam'

            camdname.close()
        else:
            return 'unknow'
        return info2 + info

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, (self.CHANGED_POLL,))