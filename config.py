import numpy as np

# this is an array with measured values for sensitivity
# see paper, Table 3
# 0 = SF 
# 1 = sensi at BW125 2 at BW250 3 at BW500
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])

"""
 Sensitivity from SX1272DS Band 1
 125 kHz bandwidth
 250 kHz
 500 kHz
"""

# sf7 = np.array([7,-123,-120,-116])
# sf8 = np.array([8,-126,-123,-119])
# sf9 = np.array([9,-129,-125,-122])
# sf10 = np.array([10,-132,-128,-1125])
# sf11 = np.array([11,-133,-130,-128])
# sf12 = np.array([12,-136,-133,-130])

sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])
PkgTime = [0]*13
PkgTime[7] = 36
PkgTime[8] = 64
PkgTime[9] = 113
PkgTime[10] = 204
PkgTime[11] = 372
PkgTime[12] = 682



DistMode = 4 # Default = 4
NodeMode = 0 # Default = 0
PtxMode = 4 # Default = 4
TestCondition = [DistMode,NodeMode,PtxMode]


Dist_Setting = [11_000,12_000,13_000,14_000,15_000]
Node_Setting = [16,17,18,19,20]
Ptx_Setting =[10,11,12,13,14]

sf_cofig = 7
cr_config = 1
bw_config = 125



ProtocolMode = 1
ShowMode = 0 # 0 = Show , 1 = Not Show
PathLossMode = 0 # 0 = free spave , 1 = dortmund


# width of area of the experiment
maxDist = Dist_Setting[DistMode]#10_000
part_config = Node_Setting[NodeMode] # block number for node 15 = 15*15 =225 node
Ptx = Ptx_Setting[PtxMode] 


pktLen = 25
gamma = 2.08 #2.08 free space #2.65 dortmund
d0 = 1000 #40.0
var = 0           # variance ignored for now
Lpld0 = 127.41 #127.41 free space  #132.25 dortmund
GL = 0




