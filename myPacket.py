import math
import random
import numpy as np
import config as cf
from myNode import myNode

# this is an array with measured values for sensitivity
# see paper, Table 3
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])

sensi = cf.sensi

minsensi = np.amin(sensi)

#
# this function creates a packet (associated with a node)
# it also sets all parameters, currently random
#
class myPacket():
    def __init__(self, nodeID, plen, distance, bs,SF):
        # new: base station ID
        self.bs = bs
        self.nodeid = nodeID
        # randomize configuration values
        self.sf = SF
        self.cr = cf.cr_config
        self.bw = cf.bw_config
        
        # for experiment 3 find the best setting
        # OBS, some hardcoded values
        Prx = cf.Ptx  ## zero path loss by default
        
        # frequencies: lower bound + number of 61 Hz steps
        self.freq = 860000000 + random.randint(0,2622950)

        self.freq = 860_000_000

        # log-shadow
        Lpl = cf.Lpld0 + 10*cf.gamma*math.log10(distance/cf.d0)
        #Lpl = 20*math.log10(self.freq) + 20 *math.log10(distance)
        Prx = cf.Ptx - cf.GL - Lpl
        
        # transmission range, needs update XXX
        self.transRange = 150
        self.pl = plen
        self.symTime = (2.0**self.sf)/self.bw
        self.arriveTime = 0
        self.rssi = Prx

        
        self.rectime = airtime(self.sf,self.cr,self.pl,self.bw)
        # denote if packet is collided
        self.collided = 0
        self.processed = 0
        # mark the packet as lost when it's rssi is below the sensitivity
        # don't do this for experiment 3, as it requires a bit more work
        
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
        
        # ! note this in paper
        self.lost = self.rssi < minsensi
        
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
            