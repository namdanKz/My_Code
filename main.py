import math
def MyProtocal(Hopcount):
    x = [None] * 13
    Hop = Hopcount
    if Hop%2 == 0:
        Test = 1+Hop/2
    else:
        Test = math.ceil(Hop/2)
    CurrentSF = 7
    while Test/2 > 0:
        x[CurrentSF] = Test
        Test = math.floor(Test/2)
        CurrentSF += 1
        if CurrentSF > 12:
            break
    if Hop%2 != 0 and CurrentSF < 13:
        x[CurrentSF] = x[CurrentSF-1]
    for i in range(7,13):
        if x[i] != None:
            continue
            print(f"At SF{i} HopXXX = {x[i]}")
    y =[z for z in x if z != None]
    print(f"At Count = {Hopcount} Sum = {sum(y)}")

for i in range(50):
    MyProtocal(i)
