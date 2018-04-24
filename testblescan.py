# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import bluetooth._bluetooth as bluez
import time
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

#initialize music player
pygame.mixer.init()

#iBeacon minor parameter used to identify beacons
id_left = '5'
id_right = '20'
id_center = '2'

#initialize rssi values
rssi_left = -1000
rssi_right = -1000
rssi_center = -1000

#initialize average rssi values
rssi_left_ave = -1000
rssi_right_ave = -1000
rssi_center_ave = -1000

#counter of values read
right_count = 0
left_count = 0
center_count = 0

#booleans to determine if certain sound is playing
#can change this to int with range 0-3
playing_left = False
playing_right = False
playing_center = False
playing_outside = False

#number of samples to average
list_size = 5

#create lists to store last 5 rssi values
rssi_center_list = [0]*list_size
rssi_left_list = [0]*list_size
rssi_right_list = [0]*list_size


while True:
        #scan for bluetooth beacons
        returnedList = blescan.parse_events(sock, 10)
        print("----------")
        for beacon in returnedList:
            if beacon[0:8].lower() == "20:CD:39".lower():
        
                    
                id = beacon.split(',')[3] #read id from beacon data
                rssi = beacon.split(',')[-1] #read rssi from beacon data
                print(beacon)
                print("id", id)
                print("rssi", rssi)
                
                #wait until at least list_size samples are read from right or left before playing sounds
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
                        
                #determine which sound to play after at least list_size samples have been collected
                else:
                    if id == id_center:
                        rssi_center = int(rssi)
                    elif id == id_right:
                        rssi_right = int(rssi)
                        #rssi_right_list uses % to overwrite the oldest value in the list
                        rssi_right_list[right_count%list_size] = rssi_right
                        right_count += 1
                        print("rssi_right_list", rssi_right_list)
                        rssi_right_ave = sum(rssi_right_list)/list_size
                    else:
                        rssi_left = int(rssi)
                        #rssi_left_list uses % to overwrite the oldest value in the list
                        rssi_left_list[left_count%list_size] = rssi_left
                        left_count += 1
                        print("rssi_left_list", rssi_left_list)
                        rssi_left_ave = sum(rssi_left_list)/list_size
                    
                    print("rssi_left", rssi_left_ave)
                    print("rssi_right", rssi_right_ave)
                    print("rssi_center", rssi_center)
                        
                    #don't play sounds if the user is too far away from painting    
                    if rssi_center < -70:
                        print("too far")
                        playing_left = False
                        playing_right = False
                        playing_center = False
                        playing_outside = False
                        pygame.mixer.music.pause()
                        break
                   
                    #play outside sound if user is within range of -70:-64.
                    elif rssi_center < -63:
                        print("outside sound")
                        
                        #only load and play song from beginning if outside sound is not already playing
                        if playing_outside == False:
                            pygame.mixer.music.load("/home/pi/bluetooth-beacon-art/outer.wav")
                            pygame.mixer.music.play()
                      
                        playing_outside = True
                        playing_left = False
                        playing_right = False
                        playing_center = False
                  
                    #play left or right sound if there is a difference greater than 2 between their respective rssi values
                    elif abs(rssi_left_ave - rssi_right_ave) > 2: 
                        
                        #play left sound
                        if rssi_left_ave > rssi_right_ave:
                            print("left playing")
                            if playing_left == False:
                                pygame.mixer.music.load("/home/pi/bluetooth-beacon-art/left.wav")
                                pygame.mixer.music.play()
                            playing_left = True
                            playing_outside = False
                            playing_right = False
                            playing_center = False
                        
                        #play right sound
                        else:
                            print("right playing")
                            if playing_right == False:
                                pygame.mixer.music.load("/home/pi/bluetooth-beacon-art/right.wav")
                                pygame.mixer.music.play()
                            playing_left = False
                            playing_outside = False
                            playing_right = True
                            playing_center = False
                                
                    #play center sound if there is not a significant difference between left and right rssi values
                    #this helps prevent jumping between left and right sounds if user is near the middle of the painting
                    else:
                            print("center playing")
                            if playing_center == False:
                                pygame.mixer.music.load("/home/pi/bluetooth-beacon-art/middle.wav")
                                pygame.mixer.music.play()

                            playing_left = False
                            playing_outside = False
                            playing_right = False
                            playing_center = True
                     
                    sleep(0.5)
       # sleep(1)
