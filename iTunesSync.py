#!/usr/bin

import eyed3
import os
import sys
from pyItunes import *
import subprocess

SONG_RATING = 0 

def start_adb(lib) :

    print 'starting adb server ... '

    state = ' '
    music_dir = '/sdcard/Music'

    subprocess.call('adb start-server' , shell=True)
    state = subprocess.check_output('adb get-state' , shell=True)

    print 'state is : ' + state
    if not state.startswith('device') :
        print "no device connected , exiting ... "
        return
    
    for id, song in lib.songs.items():
        if song.rating > SONG_RATING:

            name = normalize_string(song.name)
            print name

            c = subprocess.check_output('adb shell ls /sdcard/Music/' + name + '.mp3' , shell=True)

            if not (c.endswith('.mp3')) :

                print "copying track \"" + song.name + "\" to device ...  "
                d = os.path.normpath(song.location)
                d = normalize_string(d)

                os.system('adb push /' + d + ' ' + music_dir)

    print "Finished syncing ."


def normalize_string(s) :

    s = s.replace('(' , '\(')
    s = s.replace(')' , '\)')
    s = s.replace(' ' , '\ ')
    s = s.replace('[' , '\[')
    s = s.replace(']' , '\]')
    s = s.replace('&' , '\&')
    s = s.replace('\'' , '\\\'')

    return s

if __name__ == '__main__' :

    s = raw_input("Enter Minimum Rating for songs to be synced (out of 100) : ")
    SONG_RATING = int(s)

    userName = subprocess.check_output('whoami' , shell=False)
    userName = userName.rstrip() 

    name = "/Users/" + userName + "/Music/iTunes/iTunes Music Library.xml"
    name = os.path.normpath(name)
    lib = Library(name)
    start_adb(lib)
    raw_input("Press any ket to exit ... ")
    os.system('adb kill-server')
    exit()