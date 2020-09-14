# uncompyle6 version 3.7.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Apr 20 2020, 20:30:41) 
# [GCC 9.3.0]
# Embedded file name: knocking.py
# Compiled at: 2020-08-03 17:26:57
import os, vlc
from datetime import datetime
import atexit, base64, time
dat = [
 [
  61, 'Z'], [61, '4'], [61, 'm'], [68, 'x'], [68, 'b'], [68, 'h'], [75, 'Z'], [75, 'a'], [76, 'y'], [82, 'B'], [82, 'd'], [83, 'P'], [148, 'T'], [148, '8'], [149, 'k'], [155, 'F'], [156, 'c'], [156, '7'], [162, 'S'], [163, '9'], [163, '2'], [170, '4'], [170, '2'], [170, 'w'], [234, 'K'], [235, '0'], [235, 'G'], [241, 't'], [242, '7'], [242, 'p'], [249, 'b'], [249, '5'], [250, 'l'], [256, '9'], [256, 'b'], [257, 'J'], [263, 'b'], [264, '4'], [264, 'n'], [271, 'R'], [271, 'd'], [271, 'S'], [278, 'M'], [278, 'f'], [278, 'F'], [285, '9'], [285, 'e'], [286, 'I'], [292, 'Z'], [292, '7'], [293, 'T'], [299, 'R'], [300, '0'], [300, '2'], [306, 'Z'], [307, 'a'], [307, 'U'], [314, '5'], [314, '2'], [314, '9']]

def exit_handler():
    f = open('.KnockinOnHeavensDoor.mp3', 'w')
    f.write('')
    f.close()


def decode(music, outfile):
    f = open(music, 'rb')
    bs64 = f.read()
    f.close()
    out = base64.b64decode(bs64)
    f = open(outfile, 'w')
    for i in out:
        f.write(i)

    f.close()


def knock(initial, tr):
    #k = raw_input()
    b = datetime.now()
    delta = b - initial
    delta = 1 #abs(delta.seconds - tr[0])
    if delta < 2:
        return tr[1]
    return False


def chrKnock(initial, tn):
    s = ''
    a = knock(initial, dat[tn])
    if a == False:
        return False
    b = knock(initial, dat[(tn + 1)])
    if b == False:
        return False
    c = knock(initial, dat[(tn + 2)])
    if c == False:
        return False
    if a != False:
        s = s + a
        if b != False:
            s = s + b
            if c != False:
                s = a + c
                return s
    return False


print 'Hello rock fan!!! Here is a game you will like'
print 'Give me a minute to generate and load the chords...'
try:
    decode('.music', '.KnockinOnHeavensDoor.mp3')
except:
    print 'some files are missing, please be sure to decompress all the game files in the same folder and play the game!'
    exit()

atexit.register(exit_handler)
print 'Ok, im ready. Hit Intro to start playing the music and dont lose the pitch:'
#raw_input()
player = vlc.MediaPlayer('.KnockinOnHeavensDoor.mp3')
player.play()
ini = datetime.now()
f = ''
for i in range(20):
    out = chrKnock(ini, i * 3)
    if out != False:
        f = f + out
    else:
        print '\nYou Failed! You are not listening to the music... Practice some more and try again!'
        print ''
        exit()

#time.sleep(7)
print '\nCongratulations, you Rock!!! Here you have your reward:'
print str(base64.b64decode(f))
# okay decompiling knocking.pyc
