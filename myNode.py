class myNode():

    
    def __init__(self, id, period, packetlen):
        # initail sf is 7
        self.SF = 7
        self.AvailableTime = 0
        # ! add for create packet
        self.packetlen = packetlen
        self.cansend = False # ! initial is can't send 
        
        # ! nb = neighbor
        self.nbSame = [[] for _ in range(13)]
        self.nbUpper = [[] for _ in range(13)]
        self.nbLower = [[] for _ in range(13)]

        self.tmpSame = [[] for _ in range(13)]
        self.tmpUpper = [[] for _ in range(13)]
        self.tmpLower = [[] for _ in range(13)]

        
        self.temp_same = []
        self.temp_upper = []
        self.temp_lower = []
        
        self.finished = False
        
        # ! inital layer = 0
        self.SFlevel = [[] for _ in range(13)]
        for i in range(7,13):
            self.SFlevel[i] = 99
        #self.SFlevel = 0
        
        self.id = id
        self.period = period
        self.x = 0
        self.y = 0
        self.packet = []
        
        # ! nodes id of node that packets are not lost
        self.reached = [[] for _ in range(13)]
        
        self.parent = -1
        self.child = []
        
        self.sent = 0
        
    def ClearNeighbor(self,id):
        if id in self.nbLower[self.SF]:
            self.nbLower[self.SF].remove(id)
        elif id in self.nbSame[self.SF]:
            self.nbSame[self.SF].remove(id)
        elif id in self.nbUpper[self.SF]:
            self.nbUpper[self.SF].remove(id)    
        return

    def UpdateNeighbor(self,id,SfLv):
        self.ClearNeighbor(id)
        if self.SFlevel[self.SF] == SfLv:
            self.nbSame[self.SF].append(id)
        elif self.SFlevel[self.SF] < SfLv:
            self.nbUpper[self.SF].append(id)
        else:
            self.nbLower[self.SF].append(id)
            self.SFlevel[self.SF] = SfLv+1
        return
    
    def SFLevel(self):
        return self.SFlevel[self.SF]
    
    def Reached(self):
        return self.reached[self.SF]
    

