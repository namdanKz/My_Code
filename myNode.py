import math

Myconst = [0]*13
Myconst[7] = 32/63
Myconst[8] = 16/63
Myconst[9] = 8/63
Myconst[10] = 4/63
Myconst[11] = 2/63
Myconst[12] = 1/63

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
        
        
        self.recived =[[] for _ in range(13)]
        
        self.temp_same = []
        self.temp_upper = []
        self.temp_lower = []
        
        self.finished = False
        
        # ! inital layer = 0
        self.SFlevel = [[] for _ in range(13)]
        for i in range(7,13):
            self.SFlevel[i] = 99
        
        
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
        
        self.SFSlot = []
        self.HopCount = 0
        self.Transmission = 0
        
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
            #self.SFlevel[self.SF] = SfLv+1
        return
    
    def ResetSF(self):
        self.SF = 7
    
    def IncreaseSF(self):
        if self.SF < 12:
            self.SF += 1
    
    def IncreaseSFLevel(self):
        self.SFlevel[self.SF] += 1
    
    def UpdateSFLevel(self,newLevel):
        self.SFlevel[self.SF] = newLevel
    
    def GetSFLevel(self):
        return self.SFlevel[self.SF]
    
    def GetReached(self):
        return self.reached[self.SF]
    
    def CheckRecived(self,id):
        if id in self.recived[self.SF]:
            return True
        self.recived[self.SF].append(id)
        return False
    
    def GetnbLower(self):
        return self.nbLower[self.SF]
    
    def GetnbSame(self):
        return self.nbSame[self.SF]
    
    def GetnbUpper(self):
        return self.nbSame[self.SF]
    
    
    #Hopcount from main file
    # def GetSlot(self):
    #     self.SFSlot = [0] * 13
    #     Hop = self.HopCount
    #     while True:
    #         if Hop == 0:
    #             break
    #         for i in range(7,13):
    #             added = math.ceil(Hop/2) # Ceiling for Last hop
    #             if i == 7:
    #                 self.SFSlot[i] += added
    #             else:
    #                 while (self.SFSlot[i]+added)*2 > self.SFSlot[i-1]:
    #                     added -= 1 
    #                 if added == 0: # Not sure
    #                     break
    #                 self.SFSlot[i] += added
    #             Hop -= added

    def GetSlot(self):
        """ 
        new function
        use const from model
        """
        self.SFSlot = [0] * 13
        Trans = self.Transmission
        for i in range(7,13):
            add = math.ceil(self.Transmission*Myconst[i])
            while True:
                if add*2 > self.SFSlot[i-1] and i != 7:
                    add -= 1
                    continue
                break
            self.SFSlot[i] += add
            Trans -= add
            if Trans == 0:
                break
        if Trans != 0:
            self.SFSlot[7] += Trans
    
    

