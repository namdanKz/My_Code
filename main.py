import math
def MyProtocal(Hopcount):
    x = [0] * 13
    Hop = Hopcount
    count = 0
    while True:
        if Hop == 0:
            break
        for i in range(7,13):
            added = math.ceil(Hop/2) # Ceiling for Last hop
            if i == 7:
                x[i] += added
            else:
                while (x[i]+added)*2 > x[i-1]:
                    added -= 1 
                if added == 0: # Not sure
                    break
                x[i] += added
            Hop -= added
        count += 1
        
    print(f"Hop={Hopcount} ",end="")
    for i in range(7,13):
        print(f"SF{i}={x[i]} ",end="")
    print(f"Sum = {sum(x)} ",end="")
    print(f"% = {100*(x[7]/Hopcount):.2f}")
    
    
Myconst = [0]*13
Myconst[7] = 32/63
Myconst[8] = 16/63
Myconst[9] = 8/63
Myconst[10] = 4/63
Myconst[11] = 2/63
Myconst[12] = 1/63

def NewSlot(Transmission):
    x = [0] * 13
    Trans = Transmission
    for i in range(7,13):
        add = math.ceil(Transmission*Myconst[i])
        while True:
            if add*2 > x[i-1] and i != 7:
                add -= 1
                continue
            break
        x[i] += add
        Trans -= add
        if Trans == 0:
            break
    # if Trans != 0:
    #     x[7] += Trans
    print(f"Total ={Transmission} ",end="")
    for i in range(7,13):
        print(f"SF{i}={x[i]} ",end="")
    print(f"Sum = {sum(x)} ",end="")
    print(f"% = {100*(x[7]/Transmission):.2f}")
    


print("Start")
for i in range(5000,5010):
    #MyProtocal(i)
    NewSlot(i)

