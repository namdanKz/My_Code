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

sf_cofig = 7
cr_config = 1
bw_config = 125

# width of area of the experiment
maxDist = 10_000
part_config = 15


ProtocolMode = 1
ShowMode = 1 # 0 = Show , 1 = Not Show

pktLen = 25

Ptx = 14 
gamma = 2.65 #2.08 #2.65
d0 = 1000 #40.0
var = 0           # variance ignored for now
Lpld0 = 132.25 #127.41 #132.25
GL = 0
