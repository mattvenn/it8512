'''
Open Source Initiative OSI - The MIT License:Licensing
Tue, 2006-10-31 04:56 nelson

The MIT License

Copyright (c) 2009 BK Precision
'''

import sys, dcload, time
err = sys.stderr.write
import csv

def TalkToLoad(load, port, baudrate):
    def test(cmd, results):
        if results:
            print cmd, "failed:"
            print "  ", results
            exit(1)
        else:
            print cmd
    load.Initialize(port, baudrate) # Open a serial connection
    print "Time from DC Load =", load.TimeNow()
    test("Set to remote control", load.SetRemoteControl())

    load.SetBatteryTestVoltage(4)
    load.SetCCCurrent(0.12)
    print "batt V =", load.GetBatteryTestVoltage()
    print "batt I =", load.GetCCCurrent()
    load.SetFunction('battery')
    print "Function =", load.GetFunction()

    load.TurnLoadOn()
    
    values = load.GetInputValues().split("\t")
    #wait for mode to switch (4th element in value array)
    time.sleep(1)
    with open('battery.csv', 'wb') as csvfile:
        csv_w = csv.writer(csvfile, delimiter=',')
        csv_w.writerow(['time','voltage','current','power'])
        while True:
            values = load.GetInputValues().split("\t")
            volts = values[0]
            amps = values[1]
            watts = values[2]
            volts = volts.replace(' V','')
            watts = watts.replace(' W','')
            amps = amps.replace(' A','')
            print load.TimeNow()
            print values
            csv_w.writerow([ load.TimeNow(),volts,amps,watts])
            #if mode changes back to 0x0 then the test is over
            if values[4] == '0x0':
                #test ended
                break
            time.sleep(10)
    #set back to local
    test("Set to local control", load.SetLocalControl())

if __name__ == '__main__':
    port        = '/dev/ttyUSB0'
    baudrate    = 4800
    load = dcload.DCLoad()
    TalkToLoad(load, port, baudrate)
