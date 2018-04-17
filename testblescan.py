# test BLE Scanning software
# jcs 6/8/2014
#!/usr/bin/env python3

import blescan
import sys
import bluetooth._bluetooth as bluez
import time
#from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import pygame

dev_id = 0
try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")

except:
        print("error accessing bluetooth device...")
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
pygame.mixer.init()
id_left = '5'
id_right = '20'
id_center = '2'
rssi_left = -1000
rssi_right = -1000
rssi_center = -1000
rssi_left_ave = -1000
rssi_right_ave = -1000
rssi_center_ave = -1000
right_count = 0
left_count = 0
center_count = 0
playing_left = False
playing_right = False
playing_center = False
playing_outside = False
list_size = 5
rssi_center_list = [0]*list_size
rssi_left_list = [0]*list_size
rssi_right_list = [0]*list_size
while True:
        returnedList = blescan.parse_events(sock, 10)
        print("----------")
        for beacon in returnedList:
            if beacon[0:8].lower() == "20:CD:39".lower():# or beacon[0:8] == "20:cd:39":
               # while (count  < 10):
                #    if id ==
                    
                id = beacon.split(',')[3]
                rssi = beacon.split(',')[-1]
                print(beacon)
                print("id", id)
                print("id test", beacon.split(',')[3])
                print("rssi", rssi)
                if (left_count < list_size and right_count < list_size):
                    if id == id_center:
                        rssi_center = int(rssi)
                        rssi_center_list[center_count%list_size] = rssi_center
                        print("rssi_center_list", rssi_center_list)
                        center_count += 1
                        rssi_center_ave = sum(rssi_center_list)/list_size
                    
                    elif id == id_right:
                        rssi_right = int(rssi)
                        rssi_right_list[right_count%list_size] = rssi_right
                        print("rssi_right_list", rssi_right_list)
                        right_count += 1
                        rssi_right_ave = sum(rssi_right_list)/list_size
                    else:
                        rssi_left = int(rssi)
                        rssi_left_list[left_count%list_size] = rssi_left
                        print("rssi_left_list", rssi_left_list)
                        left_count += 1
                        rssi_left_ave = sum(rssi_left_list)/list_size
                else:
                    if id == id_center:
                        rssi_center = int(rssi)
                    elif id == id_right:
                        rssi_right = int(rssi)
                        rssi_right_list[right_count%list_size] = rssi_right
                        right_count += 1
                        print("rssi_right_list", rssi_right_list)
                        rssi_right_ave = sum(rssi_right_list)/list_size
                    else:
                        rssi_left = int(rssi)
                        rssi_left_list[left_count%list_size] = rssi_left
                        left_count += 1
                        print("rssi_left_list", rssi_left_list)
                        rssi_left_ave = sum(rssi_left_list)/list_size
                    
                    print("rssi_left", rssi_left_ave)
                    print("rssi_right", rssi_right_ave)
                    print("rssi_center", rssi_center)
                    if rssi_center < -70:
                        print("too far")
                        playing_left = False
                        playing_right = False
                        playing_center = False
                        playing_outside = False
                        pygame.mixer.music.pause()
                        break
                    elif rssi_center < -63:
                        print("outside sound")
                        if playing_outside == False:
                            pygame.mixer.music.load("/home/pi/iBeacon-Scanner-/outer.wav")
                            pygame.mixer.music.play()
                        #sleep(5)
                        playing_outside = True
                        playing_left = False
                        playing_right = False
                        playing_center = False
                        #pygame.mixer.music.pause()
                    elif abs(rssi_left_ave - rssi_right_ave) > 2:     
                        if rssi_left_ave > rssi_right_ave:
                            print("left playing")
                            if playing_left == False:
                                pygame.mixer.music.load("/home/pi/iBeacon-Scanner-/left.wav")
                                pygame.mixer.music.play()
                            playing_left = True
                            playing_outside = False
                            playing_right = False
                            playing_center = False
                            #sleep(3)
                            #pygame.mixer.music.pause()
                        else:
                            print("right playing")
                            if playing_right == False:
                                pygame.mixer.music.load("/home/pi/iBeacon-Scanner-/right.wav")
                                pygame.mixer.music.play()
                            #sleep(3)
                            playing_left = False
                            playing_outside = False
                            playing_right = True
                            playing_center = False
                            #pygame.mixer.music.pause()
                    else:
                            print("center playing")
                            if playing_center == False:
                                pygame.mixer.music.load("/home/pi/iBeacon-Scanner-/middle.wav")
                                pygame.mixer.music.play()

                            playing_left = False
                            playing_outside = False
                            playing_right = False
                            playing_center = True
                            #sleep(3)
                            #pygame.mixer.music.pause()

                    #player = OMXPlayer("Chariot.wav")
                   # pygame.mixer.music.play()
                   # while pygame.mixer.music.get_busy() == True:
                    #    continue
                    sleep(0.5)
       # sleep(1)
