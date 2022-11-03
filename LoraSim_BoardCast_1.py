#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
 LoRaSim: simulate collisions in LoRa - multiple base stations variant
 Copyright © 2016 Thiemo Voigt <thiemo@sics.se> and Martin Bor <m.bor@lancaster.ac.uk>

 This work is licensed under the Creative Commons Attribution 4.0
 International License. To view a copy of this license,
 visit http://creativecommons.org/licenses/by/4.0/.

 Do LoRa Low-Power Wide-Area Networks Scale? Martin Bor, Utz Roedig, Thiemo Voigt
 and Juan Alonso, MSWiM '16, http://dx.doi.org/10.1145/2988287.2989163

 $Date: 2016-10-17 13:23:52 +0100 (Mon, 17 Oct 2016) $
 $Revision: 218 $
"""

"""
 SYNOPSIS:
   ./loraDirMulbs.py <nodes> <avgsend> <experiment> <simtime> <basestation> [collision]
 DESCRIPTION:
    nodes
        number of nodes to simulate
    avgsend
        average sending interval in milliseconds
    experiment
        experiment is an integer that determines with what radio settings the
        simulation is run. All nodes are configured with a fixed transmit power
        and a single transmit frequency, unless stated otherwise.
        0   use the settings with the the slowest datarate (SF12, BW125, CR4/8).
        1   similair to experiment 0, but use a random choice of 3 transmit
            frequencies.
        2   use the settings with the fastest data rate (SF6, BW500, CR4/5).
        3   optimise the setting per node based on the distance to the gateway.
        4   use the settings as defined in LoRaWAN (SF12, BW125, CR4/5).
        5   similair to experiment 3, but also optimises the transmit power.
    simtime
        total running time in milliseconds
    basestation
        number of base stations to simulate. Can be either 1, 2, 3, 4, 6, 8 or 24.
    collision
        set to 1 to enable the full collision check, 0 to use a simplified check.
        With the simplified check, two messages collide when they arrive at the
        same time, on the same frequency and spreading factor. The full collision
        check considers the 'capture effect', whereby a collision of one or the
 OUTPUT
    The result of every simulation run will be appended to a file named expX.dat,
    whereby X is the experiment number. The file contains a space separated table
    of values for nodes, collisions, transmissions and total energy spent. The
    data file can be easily plotted using e.g. gnuplot.
"""

from myNode import myNode
import simpy
import random
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Rectangle
from datetime import datetime
import config
import matplotlib.pyplot as plt
#from myPacket import myPacket


now = datetime.now()
dt_string = now.strftime("%b%d_%H%M%S")

#test save log
fPacketPkg = f"expPkg{dt_string}.csv"
fPacketNode = f"expNode{dt_string}.csv"
#Text for header

NodeSpace = "_"*6
NodeHeader = f"Node-ID{NodeSpace} X{NodeSpace} Y{NodeSpace}\n"
with open(fPacketNode, "a") as myfile:
    myfile.write(NodeHeader)
myfile.close()

PacketHeader = f"At{NodeSpace} Node-{NodeSpace} to Node-{NodeSpace}\n"
with open(fPacketPkg, "a") as myfile:
    myfile.write(PacketHeader)
myfile.close()

#open(fPacketLog,'w').close()
#open(fPacketNode,'w').close()
NewLine = '\n'




# turn on/off graphics
graphics = 0

# do the full collision check
full_collision = False

# experiments:
# 0: packet with longest airtime, aloha-style experiment
# 0: one with 3 frequencies, 1 with 1 frequency
# 2: with shortest packets, still aloha-style
# 3: with shortest possible packets depending on distance



# this is an array with measured values for sensitivity
# see paper, Table 3
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])

# ! Move class packet 
# ! Move Node to new file

#
# this function creates a packet (associated with a node)
# it also sets all parameters, currently random
#
class myPacket():
    def __init__(self, nodeid, plen, distance, bs,SF):
        global experiment
        global Ptx
        global gamma
        global d0
        global var
        global Lpld0
        global GL

        # new: base station ID
        # ! bs = destination node number
        self.bs = bs
        self.nodeid = nodeid
        # randomize configuration values
        self.sf = random.randint(6,12)
        self.cr = random.randint(1,4)
        self.bw = random.choice([125, 250, 500])

        # for certain experiments override these
        if experiment==1 or experiment == 0:
            self.sf = 12
            self.cr = 4
            self.bw = 125

        # for certain experiments override these
        if experiment==2:
            self.sf = 6
            self.cr = 1
            self.bw = 500
        
        # ! Toomtam 
        self.sf = SF
        self.cr = 4
        self.bw = 125
        
        
        # for experiment 3 find the best setting
        # Obs, some hardcoded values
        Prx = Ptx  ## zero path loss by default

        # log-shadow
        Lpl = Lpld0 + 10*gamma*math.log(distance/d0)
        Prx = Ptx - GL - Lpl

        if (experiment == 3):
            minairtime = 9999
            minsf = 0
            minbw = 0

            for i in range(0,6):
                for j in range(1,4):
                    if (sensi[i,j] < Prx):
                        self.sf = sensi[i,0]
                        if j==1:
                            self.bw = 125
                        elif j==2:
                            self.bw = 250
                        else:
                            self.bw=500
                        at = airtime(self.sf,4,20,self.bw)
                        if at < minairtime:
                            minairtime = at
                            minsf = self.sf
                            minbw = self.bw

            self.rectime = minairtime
            self.sf = minsf
            self.bw = minbw
            if (minairtime == 9999):
                print ("does not reach base station")
                exit(-1)
        
        # transmission range, needs update XXX
        self.transRange = 150
        self.pl = plen
        self.symTime = (2.0**self.sf)/self.bw
        self.arriveTime = 0
        self.rssi = Prx
        # frequencies: lower bound + number of 61 Hz steps
        self.freq = 860000000 + random.randint(0,2622950)

        # for certain experiments override these and
        # choose some random frequences
        if experiment == 1:
            self.freq = random.choice([860000000, 864000000, 868000000])
        else:
            self.freq = 860000000
        
        self.rectime = airtime(self.sf,self.cr,self.pl,self.bw)
        # denote if packet is collided
        self.collided = 0
        self.processed = 0
        # mark the packet as lost when it's rssi is below the sensitivity
        # don't do this for experiment 3, as it requires a bit more work
        # ! note this in paper
        if experiment != 3:
            global minsensi
            if self.sf == 7:
                minsensi = sensi[0,1]
            elif self.sf == 8:
                minsensi = sensi[1,1]
            elif self.sf == 9:
                minsensi = sensi[2,1]
            elif self.sf == 10:
                minsensi = sensi[3,1]
            elif self.sf == 11:
                minsensi = sensi[4,1]
            elif self.sf == 12:
                minsensi = sensi[5,1]
            self.lost = self.rssi < minsensi
            if self.lost:
                print("node {} bs {} lost {} min{}".format(self.nodeid, self.bs, self.lost,minsensi))
            else:
                print("node {} bs {} lost {} min{}".format(self.nodeid, self.bs, self.lost,minsensi))

#
# check for collisions at base station
# Note: called before a packet (or rather node) is inserted into the list
#
# conditions for collions:
#     1. same sf
#     2. frequency, see function below (Martins email, not implementet yet):
def checkcollision(packet:myPacket):
    col = 0 # flag needed since there might be several collisions for packet
    # lost packets don't collide
    if packet.lost:
       return 0
    #if packetsAtbs[packet.bs]:
    if packetsAtNode[packet.bs]:
        for other in packetsAtNode[packet.bs]:
            if other.id != packet.nodeid:
               # simple collision
               if frequencyCollision(packet, other.packet[packet.bs]) \
                   and sfCollision(packet, other.packet[packet.bs]):
                   if full_collision:
                       if timingCollision(packet, other.packet[packet.bs]):
                           # check who collides in the power domain
                           c = powerCollision(packet, other.packet[packet.bs])
                           # mark all the collided packets
                           # either this one, the other one, or both
                           for p in c:
                               p.collided = 1
                       else:
                           # no timing collision, all fine
                           pass
                   else:
                       packet.collided = 1
                       other.packet[packet.bs].collided = 1  # other also got lost, if it wasn't lost already
                       col = 1
        return col
    return 0

#
# frequencyCollision, conditions
#
#        |f1-f2| <= 120 kHz if f1 or f2 has bw 500
#        |f1-f2| <= 60 kHz if f1 or f2 has bw 250
#        |f1-f2| <= 30 kHz if f1 or f2 has bw 125
def frequencyCollision(p1,p2):
    if (abs(p1.freq-p2.freq)<=120 and (p1.bw==500 or p2.freq==500)):
        return True
    elif (abs(p1.freq-p2.freq)<=60 and (p1.bw==250 or p2.freq==250)):
        return True
    else:
        if (abs(p1.freq-p2.freq)<=30):
            return True
    return False

def sfCollision(p1:myPacket, p2:myPacket):
    # node id 0 = gateway in this algorithm
    # p2 is destination so every sf can send to sf8
    if p2.bs == 0:
        return True
    if p1.sf == p2.sf:
        # p2 may have been lost too, will be marked by other checks
        return True
    return False

def powerCollision(p1, p2):
    powerThreshold = 6 # dB
    if abs(p1.rssi - p2.rssi) < powerThreshold:
        # packets are too close to each other, both collide
        # return both packets as casualties
        return (p1, p2)
    elif p1.rssi - p2.rssi < powerThreshold:
        # p2 overpowered p1, return p1 as casualty
        return (p1,)
    # p2 was the weaker packet, return it as a casualty
    return (p2,)

def timingCollision(p1, p2):
    # assuming p1 is the freshly arrived packet and this is the last check
    # we've already determined that p1 is a weak packet, so the only
    # way we can win is by being late enough (only the first n - 5 preamble symbols overlap)

    # assuming 8 preamble symbols
    Npream = 8

    # we can lose at most (Npream - 5) * Tsym of our preamble
    Tpreamb = 2**p1.sf/(1.0*p1.bw) * (Npream - 5)

    # check whether p2 ends in p1's critical section
    p2_end = p2.addTime + p2.rectime
    p1_cs = env.now + Tpreamb
    if p1_cs < p2_end:
        # p1 collided with p2 and lost
        return True
    return False

# this function computes the airtime of a packet
# according to LoraDesignGuide_STD.pdf
#
def airtime(sf,cr,pl,bw):
    H = 0        # implicit header disabled (H=0) or not (H=1)
    DE = 0       # low data rate optimization enabled (=1) or not (=0)
    Npream = 8   # number of preamble symbol (12.25  from Utz paper)

    if bw == 125 and sf in [11, 12]:
        # low data rate optimization mandated for BW125 with SF11 and SF12
        DE = 1
    if sf == 6:
        # can only have implicit header with SF6
        H = 1

    Tsym = (2.0**sf)/bw
    Tpream = (Npream + 4.25)*Tsym
    payloadSymbNB = 8 + max(math.ceil((8.0*pl-4.0*sf+28+16-20*H)/(4.0*(sf-2*DE)))*(cr+4),0)
    Tpayload = payloadSymbNB * Tsym
    return Tpream + Tpayload 

#
# main discrete event loop, runs for each node
# a global list of packet being processed at the gateway
# is maintained
#
def transmit(env,node:myNode):
    #while True:
    while not node.finished:
        if not node.cansend:
            yield env.timeout(1)
            continue
        
        yield env.timeout(random.expovariate(1.0/float(node.period)))

        # time sending and receiving
        # packet arrives -> add to base station

        node.sent = node.sent + 1
        
        global packetSeq
        packetSeq = packetSeq + 1


        # * namdanKz 
        # * change from 0 to nrbs to all node in system
        # ! Excep itself

        global nrbs
        for bs in range(0, nrAllNode):
           # *if (node in packetsAtbs[bs]):
           txt = f"PKG from {node.id} to {bs} "
           if bs == node.id: # ! it self no packet 
               continue
           if (node in packetsAtNode[bs]):
                print ("ERROR: packet already in")
           else:
                # adding packet if no collisio
                
                if node.id < bs:
                    send_packet = pack_mat[node.id][bs]
                else:
                    send_packet = pack_mat[bs][node.id]

                if (checkcollision(send_packet)==1): 
                    node.packet[bs].collided = 1
                else:
                    node.packet[bs].collided = 0
                packetsAtNode[bs].append(node)
                node.packet[bs].addTime = env.now
                node.packet[bs].seqNr = packetSeq

        # take first packet rectime
        if node.id == 0: #node 0 ไม่มี packet ที่ 0
            yield env.timeout(node.packet[1].rectime)
        else:
            yield env.timeout(node.packet[0].rectime)
            
        # if packet did not collide, add it in list of received packets
        # unless it is already in
        for bs in range(0, nrAllNode):
            if bs == node.id: # ! it self no packet 
               continue
            if node.packet[bs].lost:
                lostPackets.append(node.packet[bs].seqNr)
            else:
                if node.packet[bs].collided == 0:
                    #packetsRecbs[bs].append(node.packet[bs].seqNr)
                    packetsRecNode[bs].append(node.packet[bs].seqNr)
                    if (recPackets):
                        if (recPackets[-1] != node.packet[bs].seqNr):
                            recPackets.append(node.packet[bs].seqNr)
                    else:
                        recPackets.append(node.packet[bs].seqNr)
                    # ! packet are recived || node send to nodes[bs] 
                    if not nodes[bs].cansend: # ! first recived
                        nodes[bs].cansend = True
                        nodes[bs].SFlevel = node.SFlevel+1
                        node.neighbor_upper.append(nodes[bs])
                        nodes[bs].neighbor_lower.append(node)
                    else:
                        # * Clear all node in list first

                        if nodes[bs] in node.neighbor_lower:
                            node.neighbor_lower.remove(nodes[bs])
                        if nodes[bs] in node.neighbor_same:
                            node.neighbor_same.remove(nodes[bs])
                        if nodes[bs] in node.neighbor_upper:
                            node.neighbor_upper.remove(nodes[bs])

                        if node in nodes[bs].neighbor_lower:
                            nodes[bs].neighbor_lower.remove(node)
                        if node in nodes[bs].neighbor_same:
                            nodes[bs].neighbor_same.remove(node)
                        if node in nodes[bs].neighbor_upper:
                            nodes[bs].neighbor_upper.remove(node)

                        if node.SFlevel == nodes[bs].SFlevel:
                            node.neighbor_same.append(nodes[bs])
                            nodes[bs].neighbor_same.append(node)
                        elif node.SFlevel < nodes[bs].SFlevel:
                            node.neighbor_upper.append(nodes[bs])
                            nodes[bs].neighbor_lower.append(node)
                            nodes[bs].SFlevel = node.SFlevel+1
                            if node.id != 0:
                                print("Found")
                        else:
                            node.neighbor_lower.append(nodes[bs])
                            nodes[bs].neighbor_upper.append(node)
                            node.SFlevel = nodes[bs].SFlevel+1  
                
                else:
                    # XXX only for debugging
                    collidedPackets.append(node.packet[bs].seqNr)

        # complete packet has been received by base station
        # can remove it
        for bs in range(0, nrAllNode): 
            # *if (node in packetsAtbs[bs]):
            if (node in packetsAtNode[bs]):
                packetsAtNode[bs].remove(node)
               
                # reset the packet
                node.packet[bs].collided = 0
                node.packet[bs].processed = 0
                
        if node.neighbor_lower != node.temp_lower or node.neighbor_same != node.temp_same or node.neighbor_upper != node.temp_upper:
            node.temp_lower = node.neighbor_lower
            node.temp_same = node.neighbor_same
            node.temp_upper = node.neighbor_upper
        else:
            node.finished = True

def transmit2(env:simpy.Environment,node:myNode):
    while True:
        if not node.cansend:
            yield env.timeout(1)
            continue
        
        yield env.timeout(random.expovariate(1.0/float(node.period)))
        
        for i in range(0,10):
            for reach in node.reached[node.SF]:
                if node.id == reach:
                    # ! prevent from same node <<< this must be imposible but for sure 
                    continue
                #destination node
                destNode:myNode = nodes[reach]
                if node.SF != destNode.SF:
                    yield env.timeout(random.expovariate(1.0/float(node.period)))
                    continue
                # node is reciving packet
                if destNode.AvailableTime > env.now:
                    # can't send
                    continue
                if node.id < destNode.id:
                    packet_send:myPacket = pack_mat[node.SF][node.id][destNode.id]
                else:
                    packet_send = pack_mat[node.SF][destNode.id][node.id]
                if(checkcollision(packet_send)==1):
                    # can't send
                    continue
                # packet was sent from node to nodes[reach]
                destNode.AvailableTime = env.now + packet_send.rectime

                # First recived
                if not destNode.cansend:
                    destNode.cansend = True
                    destNode.SFlevel[destNode.SF] = node.SFlevel[node.SF]+1
                    node.nbUpper[node.SF].append(destNode.id)
                    destNode.nbLower[destNode.SF].append(node.id)
                else:
                    # * Clear all node in list first
                    node.ClearNeighbor(destNode.id)
                    destNode.ClearNeighbor(node.id)

                    node.UpdateNeighbor(destNode.id,destNode.SFlevel[destNode.SF])
                    destNode.UpdateNeighbor(node.id,node.SFlevel[node.SF])
        
            # take first packet rectime
            yield env.timeout(pack_mat[node.SF][0][1].rectime)
        if node.SF < 12:
            node.SF += 1
            if node.id != 0:
                node.cansend = False
            else:
                yield env.timeout(pack_mat[node.SF][0][1].rectime*10)
        else:
            node.cansend = False





#
# "main" program
#

# get arguments

if len(sys.argv) >= 6:
    nrNodes = int(sys.argv[1])
    avgSendTime = int(sys.argv[2])
    experiment = int(sys.argv[3])
    simtime = int(sys.argv[4])
    nrbs = int(sys.argv[5])
    if len(sys.argv) > 6:
        full_collision = bool(int(sys.argv[6]))
    print ("Nodes:", nrNodes)
    print ("AvgSendTime (exp. distributed):",avgSendTime)
    print ("Experiment: ", experiment)
    print ("Simtime: ", simtime)
    print ("nrbs: ", nrbs)
    if (nrbs > 4 and nrbs!=8 and nrbs!=6 and nrbs != 24):
        print("too many base stations, max 4 or 6 or 8 base stations")
        exit(-1)
    print ("Full Collision: "), full_collision
else:
    print ("usage: ./loraDir nrNodes avgSendTime experimentNr simtime nrbs [full_collision]")
    print ("experiment 0 and 1 use 1 frequency only")
    exit(-1)


# global stuff
nodes = []
packetsAtbs = []
env = simpy.Environment()

# * new
packetsAtNode = []
nrAllNode = nrbs + nrNodes

# max distance: 300m in city, 3000 m outside (5 km Utz experiment)
# also more unit-disc like according to Utz
nrCollisions = 0
nrReceived = 0
nrProcessed = 0

# global value of packet sequence numbers
packetSeq = 0

# list of received packets
recPackets=[]
collidedPackets=[]
lostPackets = []

Ptx = 23 #original = 14
gamma = 2.08
d0 = 40.0
var = 0           # variance ignored for now
Lpld0 = 127.41
GL = 0

sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])

# figure out the minimal sensitivity for the given experiment
minsensi = -200.0
if experiment in [0,1,4]:
    minsensi = sensi[5,2]  # 5th row is SF12, 2nd column is BW125
elif experiment == 2:
    minsensi = -112.0   # no experiments, so value from datasheet
elif experiment == 3:
    minsensi = np.amin(sensi) ## Experiment 3 can use any setting, so take minimum

minsensi = sensi[5,2]

Lpl = Ptx - minsensi
print ("amin", minsensi, "Lpl", Lpl)
#maxDist = d0*(math.e**((Lpl-Lpld0)/(10.0*gamma)))
maxDist = config.maxDist
print ("maxDist:", maxDist)

nodes:list[myNode]

# base station placement
bsx = maxDist+10
bsy = maxDist+10
xmax = bsx + maxDist + 20
ymax = bsy + maxDist + 20

# maximum number of packets the bs can receive at the same time
maxbsReceives = 8

maxX = 2 * maxDist * math.sin(60*(math.pi/180)) # == sqrt(3) * maxDist
print("maxX ", maxX)
maxY = 2 * maxDist * math.sin(30*(math.pi/180)) # == maxdist
print("maxY", maxY)


# prepare graphics and add sink
if (graphics == 1):
    plt.ion()
    plt.figure()
    ax = plt.gcf().gca()

    ax.add_patch(Rectangle((0, 0), maxX, maxY, fill=None, alpha=1))

# list of base stations
bs = []

# list of packets at each base station, init with 0 packets
# packetsAtbs = []
# packetsRecbs = []
# for i in range(0,nrbs):
#     b = mybs(i)
#     bs.append(b)
#     packetsAtbs.append([])
#     packetsRecbs.append([])

# * Copy
packetsAtNode = []
packetsRecNode = []


# ! ****** Log Method *******
def LogTxt_Node(node:myNode):
    textNode = f"Node ID ={node.id:>4} X ={node.x:>4} Y ={node.y:>4}\n"
    with open(fPacketNode, "a") as myfile:
        myfile.write(textNode)
    myfile.close()

def LogTxt_Pkg(time,send,to,result):
    textPkg = f"{time} from {send} to {to} {result}"
    with open(fPacketPkg, "a") as myfile:
        myfile.write(textPkg)
    myfile.close()


# ! Array for location

loX = []
loY = []

# * Gateway
gateway = myNode(0,avgSendTime,20)
gateway.x = int(maxDist/2.0)
gateway.y = int(maxDist/2.0)
gateway.SF = 7
for i in range(7,13):
    gateway.SFlevel[i] = 0

# 5*5 = 25 sqr box
eachPart = int(maxDist/5)

# number of node in each box

listLocation = []
# ! Generate node location function
def genNode():
    for i in range(0,maxDist+1,eachPart):
        tempLocation = []
        for j in range(0,maxDist+1,eachPart):
            x = random.randint(i,i+eachPart)
            y = random.randint(j-eachPart,j)
            # while not [x,y] in listLocation:
            #     x = random.randint(i,i+eachPart)
            #     y = random.randint(j,j+eachPart)
            listLocation.append([x,y])
    return


genNode()

LogTxt_Node(gateway)
gateway.cansend = True
nodes.append(gateway)
env.process(transmit2(env,gateway))
packetsAtNode.append([])
packetsRecNode.append([])

# * node id is next to base station
for i in range(nrbs,nrNodes+nrbs):
    # myNode takes period (in ms), base station id packetlen (in Bytes)
    # 1000000 = 16 min
    node = myNode(i, avgSendTime,20)
    
    node.x = listLocation[i-1][0]
    node.y = listLocation[i-1][1]
    
    LogTxt_Node(node)
    nodes.append(node)
    loX.append(node.x)
    loY.append(node.y)
    packetsAtNode.append([])
    packetsRecNode.append([])
    env.process(transmit2(env,node))

# * Create distance matrix and add packet to node
cols = nrAllNode
rows = nrAllNode
dist_mat = [[0 for i in range(cols)] for j in range(rows)]
pack_mat:list[myPacket]= [[] for _ in range(13)]
for i in range(7,13,1):
    pack_mat[i] = [[0 for i in range(cols)] for j in range(rows)]

for i in range(0,nrAllNode):
    # At i == j it's self (same node) dist = 0 package = null
    for j in range(i+1,nrAllNode):
        dist_node = np.sqrt((nodes[i].x-nodes[j].x)*(nodes[i].x-nodes[j].x)+(nodes[i].y-nodes[j].y)*(nodes[i].y-nodes[j].y))
        dist_mat[i][j] = dist_node
        
        for _ in range(7,13,1):
            packageAtNode = myPacket(nodes[i].id, nodes[i].packetlen, dist_node, j,_)
            pack_mat[_][i][j] = packageAtNode

            if not packageAtNode.lost:
                 nodes[i].reached[_].append(j)
                 nodes[j].reached[_].append(i)
        


#prepare show
if (graphics == 1):
    plt.xlim([0, xmax])
    plt.ylim([0, ymax])
    plt.draw()
    plt.show()

# store nodes and basestation locations
with open('nodes.txt', 'w') as nfile:
    for node in nodes:
        nfile.write('{x} {y} {id}\n'.format(**vars(node)))

with open('basestation.txt', 'w') as bfile:
    for basestation in bs:
        bfile.write('{x} {y} {id}\n'.format(**vars(basestation)))
        
# start simulation
env.run(until=simtime)

# print stats and save into file
# print "nrCollisions ", nrCollisions
# print list of received packets
#print recPackets
print ("nr received packets", len(recPackets))
print ("nr collided packets", len(collidedPackets))
print ("nr lost packets", len(lostPackets))



# # this can be done to keep graphics visible
# if (graphics == 1):
#     sys.stdin.read()

# plotting using plt.pyplot()

for i in nodes:
    if i.SFlevel[7] == 0:
        plt.plot(i.x,i.y,'ro')
    elif i.SFlevel[7] == 1:
        plt.plot(i.x,i.y,'go')
    elif i.SFlevel[7] == 2:
        plt.plot(i.x,i.y,'bo')
    elif i.SFlevel[7] == 3:
        plt.plot(i.x,i.y,'yo')
    elif i.SFlevel[7] == 4:
        plt.plot(i.x,i.y,'co')
    elif i.SFlevel[7] == 5:
        plt.plot(i.x,i.y,'mo')
    else:
        plt.plot(i.x,i.y,'ko')

# axis labeling
plt.xlabel('numbers')
plt.ylabel('values')

# figure name
plt.title('Dot Plot : Red Dots')
#plt.figure()
plt.show()
                                                    
exit(0)
#below not updated


# compute energy
energy = 0.0
mA = 90    # current draw for TX = 17 dBm
V = 3     # voltage XXX
sent = 0
for i in range(0,nrNodes):
#    print "sent ", nodes[i].sent
    sent = sent + nodes[i].sent
    energy = (energy + nodes[i].packet.rectime * mA * V * nodes[i].sent)/1000.0
print ("energy (in mJ): "), energy
