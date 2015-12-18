'''
PING a server with count times and get the RTT list
'''
from subprocess import Popen, PIPE
import re
import sys

def extract_number(s,notfound='NOT_FOUND'):
    regex=r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    return re.findall(regex,s)

def extractPingInfo(pingStr):
    curDataList = pingStr.split()
    pingData = {}
    for curData in curDataList:
        dataStr = curData.split('=')
        dataVal = extract_number(dataStr[1],notfound='NOT_FOUND')
        pingData[dataStr[0]] = float(dataVal[0])
    return pingData

## Call system command to ping a
def ping(ip, count):
    '''
    Pings a host and return True if it is available, False if not.
    '''
    if sys.platform == 'win32':
        cmd = ['ping', '-n', str(count), ip]
    else:
        cmd = ['ping', '-c', str(count), ip]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print stdout
    rttList = parsePingRst(stdout, count)
    return rttList

def getMnRTT(ip, count=3):
    rttList = ping(ip, count)
    if len(rttList) > 0:
        mnRTT = sum(rttList) / float(len(rttList))
    else:
        mnRTT = 500.0
    return mnRTT

def parsePingRst(pingString, count):
    rtts = []
    lines = pingString.splitlines()
    for line in lines:
        curline = line
        # print curline
        if "time=" in curline:
            curDataStr = curline.split(':', 2)[1]
            curDataDict = extractPingInfo(curDataStr)
            print curDataDict
            rtts.append(curDataDict['time'])
    return rtts

if __name__ == "__main__":
    mnRTT = getMnRTT('130.211.180.109')
    print mnRTT