class myNode():
    def __init__(self, id, period, packetlen):
        
        # initail sf is 7
        self.SF = 7
        
        self.AvailableTime = 0
        
        
        # ! add for create packet
        self.packetlen = packetlen
        self.cansend = False # ! initial is can't send 
        
        # ! neighbor
        self.neighbor_same = []
        self.neighbor_upper = []
        self.neighbor_lower = []
        
        # self.neighbor_same = [[] for _ in range(13)]
        # self.neighbor_upper = [[] for _ in range(13)]
        # self.neighbor_lower = [[] for _ in range(13)]
        
        # self.temp_same = [[] for _ in range(13)]
        # self.temp_upper = [[] for _ in range(13)]
        # self.temp_lower = [[] for _ in range(13)]
        
        self.temp_same = []
        self.temp_upper = []
        self.temp_lower = []
        
        self.finished = False
        
        # ! inital layer = 0
        # self.SFlevel = [[] for _ in range(13)]
        self.SFlevel = 0
        
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
        
