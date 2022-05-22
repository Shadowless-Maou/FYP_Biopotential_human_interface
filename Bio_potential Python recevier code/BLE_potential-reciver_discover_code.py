
import asyncio
import os
from bleak import BleakClient # BLE GATT CLient library for Windows, Mac, Linux
import pyautogui # computer  control library
address = "DE:54:EE:5E:25:B9" # static set the Machine address of the EMG sensor 
BLE_UUID = "00000001-0002-0003-0004-000000000001" # UUID of the BLE device service of read function

async def main(address):
    i = 0
    x = 0
    mode_counter = 0
    counter = 0
    loop_counter = 0
    idle = False # idle mode
    function = False # function mode
    movement_mouse = False # movement mode
    Mouse_click = False # mouse click mode
    client = BleakClient(address)
    ScreenWidth, ScreenHeight = pyautogui.size() # get the screen size
    try:
        await client.connect() # wait for a connection to the device, if no connection is made, skip the following code
        while True:
            pyautogui.moveTo(ScreenWidth/2,ScreenHeight/2) #set the mouse to the middle of the screen
            #---------------------------Mircobit EMG Signal BLE input plus Decoding and mouse control selection -----------------#
            EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) 
            # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
            EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) 
            # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
            EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    
            # invert the HEX string IE from 0701 to 1070 
            EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     
            # remove the last zero to from the hex code to ensure that it is the correct hex code
            EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  
            # convert the HEx string into intergor value 
            print(EMG_BLE_VALUE)
            EMG_BLE_VALUE_1 = str(EMG_BLE_VALUE)
            # convert the integer value into a string to be used in the exporting to file code
            if os.path.exists("EMG_BLE_VALUE.txt"):
                file1 = open("BLE_EMG_VALUE.txt", "a") 
            else:
                file1 = open("BLE_EMG_VALUE.txt","a")
            # open the txt file and sit it to append mode which the next value at the end of the file.
            file1.write(EMG_BLE_VALUE_1 + "\n")
            file1.close()
            EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
            # shift all of in comming values to the down by 1023 to ensure that the values are now referenced to 0 instead of the Vref of the EMG sensor
            EMG_BLE_VALUE_2 = str(EMG_BLE_VALUE)
            if os.path.exists("BLE_EMG_VALUE_lowered.txt"):
                file1 = open("BLE_EMG_VALUE_lowered.txt", "a") 
            else:
                file1 = open("BLE_EMG_VALUE_lowered.txt") 
            # open the txt file and sit it to append mode which the next value at the end of the file.
            file1.write(EMG_BLE_VALUE_2 + "\n")
            file1.close()
            if EMG_BLE_VALUE < 0:
                EMG_BLE_VALUE = 0
                # remove the negative values of the EMG signal
            if EMG_BLE_VALUE < 1300:
                EMG_BLE_VALUE = 0
                 # remove the values that are too low to be considered as a muscle movement
            if EMG_BLE_VALUE > 1800:
                for i in range(0,100):
                    # run the code 50 times to ensure that the code is run at a steady 50Hz rate and to look out for intentional activity of muscle movement
                    EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) 
                    # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                    EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE)
                    # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                    EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]   
                    # invert the HEX string IE from 0701 to 1070 
                    EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     
                    # remove the last zero to from the hex code to ensure that it is the correct hex code
                    EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  
                    # convert the Hex string into intergor value 
                    print(EMG_BLE_VALUE)
                    # display the value on the screen
                    EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                    if EMG_BLE_VALUE < 0:
                        EMG_BLE_VALUE = 0
                        # remove the negative values of the EMG signal
                    if EMG_BLE_VALUE < 1300:
                        EMG_BLE_VALUE = 0
                        # remove the values that are too low to be considered as a muscle movement
                    if EMG_BLE_VALUE > 1800:
                        # if the value is greater than 1800 then the muscle movement has been detected
                            x += 1 
                            if x >= 5: # if the muscle movement has been detected for 5 times then the muscle movement has been detected and not a false detection.
                                counter += 1
                                # increase the counter by 1 to keep track of which feature is being selected to be used
                                function = True
                                # set the function to true to activate the function
                    EMG_BLE_VALUE_old = EMG_BLE_VALUE
                    # set the old value to the current value to be used in the next iteration
                    if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                        # if the current value is greater than the old value then the muscle movement has been detected
                        detection = True
                        # set the detection to true to state that the muscle movement has been detected
                        idle = False
                        # set the idle to false to state that the idle mode has been deactivated
                    if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                        # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                        detection = False
                        # set the detection to false to state that the muscle movement has not been detected
                    if detection == False:
                        x = 0
                        loop_counter += 1
                        if loop_counter > 40:
                            function = False
                            # reset the function state to false as the idle state has been reached and the user is no longer using the system 
            #---------------------------Mircobit EMG Signal BLE input plus Decoding and mouse mode selection -----------------# 
            #----------------------------------------Function selection and execution---------------------------------------#                       
            while function == True:
                if counter == 1: # if the counter is 1 mosuse movement control are actived
                #---------------------------Mouse movement control---------------------------------------#
                    while idle == False:
                        EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                        EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                        EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                        EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                        EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                        print(EMG_BLE_VALUE)
                        EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                        if EMG_BLE_VALUE < 0:
                            EMG_BLE_VALUE = 0
                        if EMG_BLE_VALUE < 1300:
                            EMG_BLE_VALUE = 0
                        if EMG_BLE_VALUE > 1800:
                           for i in range(0,50):
                                EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                print(EMG_BLE_VALUE)
                                EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                if EMG_BLE_VALUE < 0:
                                    EMG_BLE_VALUE = 0
                                if EMG_BLE_VALUE < 1300:
                                    EMG_BLE_VALUE = 0
                                if EMG_BLE_VALUE > 1800:
                                        x += 1 
                                        if x >= 5:
                                            mode += 1
                                            movement_mouse = True
                                EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                # set the old value to the current value to be used in the next iteration
                                if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                    # if the current value is greater than the old value then the muscle movement has been detected
                                    detection = True
                                    # set the detection to true to state that the muscle movement has been detected
                                    idle = False
                                    # set the idle to false to state that the idle mode has been deactivated
                                if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                    # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                    detection = False
                                    # set the detection to false to state that the muscle movement has not been detected
                                if detection == False:
                                    x = 0
                                    # reset the counter to 0 to to ignore the false detection of the muscle movement
                                if detection == False:
                                    loop_counter += 1
                                    if loop_counter > 20:
                                        idle = True
                                        counter = 0
                                        # if the code has been running for 10 iteration with no activity then the idle state has been reached
                                        function = False
                                        # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                        if mode == 1: # horizontal movement
                            while movement_mouse == True:
                                for i in range(0,50):
                                    EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                    EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                    EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                    EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                    EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                    print(EMG_BLE_VALUE)
                                    EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                    if EMG_BLE_VALUE < 0:
                                        EMG_BLE_VALUE = 0
                                    if EMG_BLE_VALUE < 1300:
                                        EMG_BLE_VALUE = 0
                                    if EMG_BLE_VALUE > 1800:
                                        x += 1
                                        if x >= 5:
                                            mode_counter += 1
                                    EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                    # set the old value to the current value to be used in the next iteration
                                    if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                        # if the current value is greater than the old value then the muscle movement has been detected
                                        detection = True
                                        # set the detection to true to state that the muscle movement has been detected
                                        idle = False
                                        # set the idle to false to state that the idle mode has been deactivated
                                    if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                        # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                        detection = False
                                        # set the detection to false to state that the muscle movement has not been detected
                                    if detection == False:
                                        x = 0
                                        # reset the counter to 0 to to ignore the false detection of the muscle movement
                                    if detection == False:
                                        loop_counter += 1
                                        if loop_counter > 20:
                                            movement_mouse = False
                                            # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                if mode_counter == 1:
                                    while movement_mouse == True:
                                        EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                        EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                        EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                        print(EMG_BLE_VALUE)
                                        EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                        if EMG_BLE_VALUE < 0:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE < 1300:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE > 1800:
                                            i += 1 
                                            if i >= 5:
                                                pyautogui.moveTo(100,None,2) #move the mouse right 100 pixcels of the monitor over to 2 seconds 
                                                i = 0
                                        EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                        # set the old value to the current value to be used in the next iteration
                                        if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                            # if the current value is greater than the old value then the muscle movement has been detected
                                            detection = True
                                            # set the detection to true to state that the muscle movement has been detected
                                            idle = False
                                            # set the idle to false to state that the idle mode has been deactivated
                                        if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                            # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                            detection = False
                                            # set the detection to false to state that the muscle movement has not been detected
                                        if detection == False:
                                            # reset the counter to 0 to to ignore the false detection of the muscle movement
                                            loop_counter += 1
                                            if loop_counter > 20:
                                                movement_mouse = False
                                                # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                if mode_counter >= 2:
                                        while movement_mouse == True:
                                            EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                            EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                            EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                            EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                            EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                            print(EMG_BLE_VALUE)
                                            EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                            if EMG_BLE_VALUE < 0:
                                                EMG_BLE_VALUE = 0
                                            if EMG_BLE_VALUE < 1300:
                                                EMG_BLE_VALUE = 0
                                            if EMG_BLE_VALUE > 1800:
                                                i += 1 
                                                if i >= 5:
                                                    pyautogui.moveTo(-100,None,2) #move the mouse left 100 pixcels of the monitor over to 2 seconds 
                                                    i = 0
                                            EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                            # set the old value to the current value to be used in the next iteration
                                            if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                                # if the current value is greater than the old value then the muscle movement has been detected
                                                detection = True
                                                # set the detection to true to state that the muscle movement has been detected
                                                idle = False
                                                # set the idle to false to state that the idle mode has been deactivated
                                            if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                                # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                                detection = False
                                                # set the detection to false to state that the muscle movement has not been detected
                                            if detection == False:
                                                x = 0
                                                # reset the counter to 0 to to ignore the false detection of the muscle movement
                                                loop_counter += 1
                                                if loop_counter > 20:
                                                    movement_mouse = False
                                                    # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                        if mode >= 2: # vertial movement
                            while movement_mouse == True:
                                for i in range(0,50):
                                    EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                    EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                    EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                    EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                    EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                    print(EMG_BLE_VALUE)
                                    EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                    if EMG_BLE_VALUE < 0:
                                        EMG_BLE_VALUE = 0
                                    if EMG_BLE_VALUE < 1300:
                                        EMG_BLE_VALUE = 0
                                    if EMG_BLE_VALUE > 1800:
                                        x += 1
                                        if x >= 5:
                                            mode_counter += 1
                                            movement_mouse = True
                                    EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                    # set the old value to the current value to be used in the next iteration
                                    if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                        # if the current value is greater than the old value then the muscle movement has been detected
                                        detection = True
                                        # set the detection to true to state that the muscle movement has been detected
                                        idle = False
                                        # set the idle to false to state that the idle mode has been deactivated
                                    if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                        # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                        detection = False
                                        # set the detection to false to state that the muscle movement has not been detected
                                    if detection == False:
                                        x = 0
                                        # reset the counter to 0 to to ignore the false detection of the muscle movement
                                        loop_counter += 1
                                        if loop_counter > 20:
                                            movement_mouse = False
                                            # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                if mode_counter == 1:
                                    while movement_mouse == True:
                                        EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                        EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                        EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                        print(EMG_BLE_VALUE)
                                        EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                        if EMG_BLE_VALUE < 0:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE < 1300:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE > 1800:
                                            x += 1 
                                            if x >= 5:
                                                pyautogui.moveTo(None,-100,2) #move the mouse up 100 pixcels of the monitor over to 2 seconds 
                                                x = 0
                                        EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                        # set the old value to the current value to be used in the next iteration
                                        if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                            # if the current value is greater than the old value then the muscle movement has been detected
                                            detection = True
                                            # set the detection to true to state that the muscle movement has been detected
                                        if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                            # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                            detection = False
                                            # set the detection to false to state that the muscle movement has not been detected
                                        if detection == False:
                                            x = 0
                                            # reset the counter to 0 to to ignore the false detection of the muscle movement
                                            loop_counter += 1
                                            if loop_counter > 20:
                                                movement_mouse = False
                                                # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                if mode_counter >= 2:
                                    while movement_mouse == True:
                                        EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                        EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                        EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                        EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                        print(EMG_BLE_VALUE)
                                        EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                        if EMG_BLE_VALUE < 0:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE < 1300:
                                            EMG_BLE_VALUE = 0
                                        if EMG_BLE_VALUE > 1800:
                                            i += 1 
                                            if i >= 5:
                                                pyautogui.moveTo(None,100,2) #move the mouse down 100 pixcels of the monitor over to 2 seconds 
                                                i = 0
                                        EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                        # set the old value to the current value to be used in the next iteration
                                        if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                            # if the current value is greater than the old value then the muscle movement has been detected
                                            detection = True
                                            # set the detection to true to state that the muscle movement has been detected
                                        if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                            # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                            detection = False
                                            # set the detection to false to state that the muscle movement has not been detected
                                        if detection == False:
                                            x = 0
                                            # reset the counter to 0 to to ignore the false detection of the muscle movement
                                            loop_counter += 1
                                            if loop_counter > 20:
                                                movement_mouse = False
                                                # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                    #---------------------------Mouse movement control---------------------------------------#
                if counter >= 2 : # if the counter is 2 more mouse click control are actived
                    #---------------------------Mouse click control------------------------------------------#
                    while idle == False:
                            for i in range(0,50):
                                EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                print(EMG_BLE_VALUE)
                                EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                if EMG_BLE_VALUE < 0:
                                    EMG_BLE_VALUE = 0
                                if EMG_BLE_VALUE < 1300:
                                    EMG_BLE_VALUE = 0
                                if EMG_BLE_VALUE > 1800:
                                        x += 1 
                                        if x >= 5:
                                            mode += 1
                                            Mouse_click = True
                                            x = 0
                                EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                # set the old value to the current value to be used in the next iteration
                                if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                    # if the current value is greater than the old value then the muscle movement has been detected
                                    detection = True
                                    # set the detection to true to state that the muscle movement has been detected
                                    idle = False
                                    # set the idle to false to state that the idle mode has been deactivated
                                if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                    # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                    detection = False
                                    # set the detection to false to state that the muscle movement has not been detected
                                if detection == False:
                                    x = 0
                                    # reset the counter to 0 to to ignore the false detection of the muscle movement
                                    loop_counter += 1
                                    if loop_counter > 20:
                                        counter = 0
                                        idle = True
                                        # if the code has been running for 10 iteration with no activity then the idle state has been reached
                            if mode == 1: # mouse click mode
                                    while Mouse_click == True:
                                        for i in range(0,50):
                                            EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                            EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                            EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                            EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                            EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                            print(EMG_BLE_VALUE)
                                            EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                            if EMG_BLE_VALUE < 0:
                                                EMG_BLE_VALUE = 0
                                            if EMG_BLE_VALUE < 1300:
                                                EMG_BLE_VALUE = 0
                                            if EMG_BLE_VALUE > 1800:
                                                x += 1
                                                if x >= 5:
                                                    mode_counter += 1
                                                    Mouse_click = True
                                            EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                            # set the old value to the current value to be used in the next iteration
                                            if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                                # if the current value is greater than the old value then the muscle movement has been detected
                                                detection = True
                                                # set the detection to true to state that the muscle movement has been detected
                                            if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                                # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                                detection = False
                                                # set the detection to false to state that the muscle movement has not been detected
                                            if detection == False:
                                                loop_counter += 1
                                                if loop_counter > 20:
                                                    Mouse_click = False
                                                    # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                        if mode_counter == 1:
                                            while Mouse_click == True:
                                                EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                                EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                                EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                                EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                                EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                                print(EMG_BLE_VALUE)
                                                EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                                if EMG_BLE_VALUE < 0:
                                                    EMG_BLE_VALUE = 0
                                                if EMG_BLE_VALUE < 1300:
                                                    EMG_BLE_VALUE = 0
                                                if EMG_BLE_VALUE > 1800:
                                                    x += 1 
                                                    if x >= 5:
                                                        pyautogui.click(button='left') #left mouse click activated
                                                        x = 0
                                                EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                                # set the old value to the current value to be used in the next iteration
                                                if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                                    # if the current value is greater than the old value then the muscle movement has been detected
                                                    detection = True
                                                    # set the detection to true to state that the muscle movement has been detected
                                                if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                                    # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                                    detection = False
                                                    # set the detection to false to state that the muscle movement has not been detected
                                                if detection == False:
                                                    loop_counter += 1
                                                    if loop_counter > 20:
                                                        Mouse_click = False
                                                        # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                                    
                                        if mode_counter >= 2:
                                            while Mouse_click == True:
                                                EMG_BLE_VALUE = await client.read_gatt_char(BLE_UUID) # wait for the Custom BLE Value to update and retrieve from the BlE UUID protocal
                                                EMG_BLE_VALUE = ''.join('{:02x}'.format(x) for x in EMG_BLE_VALUE) # format the bytearray into a standard hex string format i.e from b\07\01 to 0701
                                                EMG_BLE_VALUE = EMG_BLE_VALUE [::-1]    # invert the HEX string IE from 0701 to 1070 
                                                EMG_BLE_VALUE = EMG_BLE_VALUE [:-1]     # remove the last zero to from the hex code to ensure that it is the correct hex code
                                                EMG_BLE_VALUE = int(EMG_BLE_VALUE ,16)  # convert the HEx string into intergor value 
                                                print(EMG_BLE_VALUE)
                                                EMG_BLE_VALUE = (EMG_BLE_VALUE - 1023)
                                                if EMG_BLE_VALUE < 0:
                                                    EMG_BLE_VALUE = 0
                                                if EMG_BLE_VALUE < 1300:
                                                    EMG_BLE_VALUE = 0
                                                if EMG_BLE_VALUE > 1800:
                                                    i += 1 
                                                    if i >= 5:
                                                        pyautogui.click(button='right') #right mouse click activated
                                                        i = 0
                                                EMG_BLE_VALUE_old = EMG_BLE_VALUE
                                                # set the old value to the current value to be used in the next iteration
                                                if EMG_BLE_VALUE_old >= EMG_BLE_VALUE:
                                                    # if the current value is greater than the old value then the muscle movement has been detected
                                                    detection = True
                                                    # set the detection to true to state that the muscle movement has been detected
                                                if EMG_BLE_VALUE_old <= EMG_BLE_VALUE:
                                                    # if the current value is less than the old value then the muscle movement has not been detected and a false detection has been detected
                                                    detection = False
                                                    # set the detection to false to state that the muscle movement has not been detected
                                                if detection == False:
                                                    loop_counter += 1
                                                    if loop_counter > 20:
                                                        Mouse_click = False
                                                        # reset the function state to false as the idle state has been reached and the user is no longer using the system 
                    #---------------------------Mouse click control------------------------------------------#
                #----------------------------------------Function selection and execution---------------------------------------# 
                
    except Exception as e: # if there is no connection to the BLE device then the program will exit
        print(e) 
    finally:
        await client.disconnect()
asyncio.run(main(address))
