class myNode():
    def __init__(self, id, period, packetlen):
        # ! add for create packet
        self.packetlen = packetlen
        self.cansend = False # ! initial is can't send 
        
        # ! neighbor
        self.neighbor_same = []
        self.neighbor_upper = []
        self.neighbor_lower = []
        
        self.temp_same = []
        self.temp_upper = []
        self.temp_lower = []
        
        self.finished = False
        
        # ! inital layer = 0
        self.SFlevel = 0
        
        self.id = id
        self.period = period
        self.x = 0
        self.y = 0
        self.packet = []
        
        
        
        self.parent = -1
        self.child = []
        
        self.sent = 0