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
        print(f"Round = {count}")
        
    print(f"Hop={Hopcount} ",end="")
    for i in range(7,13):
        print(f"SF{i}={x[i]} ",end="")
    print(f"Sum = {sum(x)} ",end="")
    print(f"% = {100*(x[7]/Hopcount):.2f}")




print("Start")
for i in range(144,145):
    MyProtocal(i)

