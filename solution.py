from socket import *
import os
import sys
import struct
import time
import select
import binascii
from statistics import stdev

# Should use stdev
totaltime = 0
packetmin = 0
packetmax = 0
packet_times = []


ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        #readlist, writelist, exceptionlist, timex = select.select([mySocket], [], [], timeLeft)
        #print("readlist ", readlist)
        #print("writelist ", writelist)
        #print("exceptionlist ", exceptionlist)
        #print("timex ", timex)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fill in start
        global totaltime
        global packetmin
        global packetmax
        global packet_times

        #print("socket", addr)
        #print("recPacket", recPacket)

        icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq_num, icmp_data = struct.unpack_from("bbHHhd", recPacket, 20)

        #print("icmp type ", icmp_type)
        #print("icmp code ", icmp_code)
        #print("icmp check sum ", icmp_checksum)
        #print("icmp id ", icmp_id)
        #print("icmp data", icmp_data, icmp_data.__sizeof__())
        #print("how long in select ", howLongInSelect)

        packet_times.append(howLongInSelect)
        totaltime = totaltime + howLongInSelect
        #print("total Time ", totaltime)

        if (packetmin == 0 and packetmax == 0):
            packetmin = packetmax = howLongInSelect
        else:
            if (howLongInSelect > packetmax):
                packetmax = howLongInSelect
            else:
                if (howLongInSelect < packetmin):
                    packetmin = howLongInSelect




        # Fetch the ICMP header from the IP packet

        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    ### fao
    #print("header ", header)
    #print("data ", data)
    #print("packet ", packet)

    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str

    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    #vars = []
    try:
        dest = gethostbyname(host)
        #print("Pinging " + dest + " using Python:")
        #print("")
        # Calculate vars values and return them
        #global totaltime
        #global packetmin
        #global packetmax
        #global packet_times


    #  vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]


    # Send ping requests to a server separated by approximately one second

        for i in range(0, 4):
            delay = doOnePing(dest, timeout)
            print(delay)
            #print("packet min = ", packetmin)
            #print("packet max = ", packetmax)
            time.sleep(1)  # one second

        packetavg = totaltime / 4
        #print("packet avg = ", packetavg)
        #print("packet times = ", packet_times)
        #print("stdev = ", stdev(packet_times))
        vars = [str(round(packetmin, 2)), str(round(packetavg, 2)), str(round(packetmax, 2)), str(round(stdev(packet_times), 2))]
        #print(vars)
    except:
        print("----- ", host, "ping statistics -----")
        vars = ['0', '0.0', '0', '0.0']
        #print(vars)
    return vars


if __name__ == '__main__':
    ping("127.0.0.1")
    ping("google.co.il")
    ping("No.no.e")

