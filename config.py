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

sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-129.25,-126.75,-124.0])
sf9 = np.array([9,-132.25,-128.25,-127.5])
sf10 = np.array([10,-135.75,-130.25,-128.75])
sf11 = np.array([11,-138.5,-132.75,-128.75])
sf12 = np.array([12,-141.25,-132.25,-132.25])

sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])

sf_cofig = 7
cr_config = 1
bw_config = 125

# width of area of the experiment
maxDist = 250
part_config = 7

pktLen = 5

Ptx = 23 
gamma = 2.08
d0 = 40.0
var = 0           # variance ignored for now
Lpld0 = 127.41
GL = 0
