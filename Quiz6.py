def addScore(team,score):
    for i in range(len(teamList)):
        if team == teamList[i]:
            scoreList[i] += score

data,dataInput,matchList,resultList,teamList,scoreList,sortData = [],[],[],[],[],[],[] 

while True:
    fName = input("Enter a file name: ")
    try:
        dataInput = open(fName).read().splitlines()
    except EnvironmentError:
        print("File doesn't exist")
        continue
    for row in dataInput:
        segment = row.split(',')
        try:
            segment[0] = int(segment[0])
        except:
            None
        data.append(segment)
    break
for i in range(1,len(data)):
    matchList.append([data[i][2],data[i][3]])
    resultList.append(data[i][4].split('-'))
    
for i in matchList:
    if i[0] in teamList:
        continue
    teamList.append(i[0])
teamList.sort()

scoreList = [0]*len(teamList)
resultList = [[int(score[0]),int(score[1])] for score in resultList]

for i in range(len(matchList)):
    if resultList[i][0] > resultList[i][1]:
        addScore(matchList[i][0],3)
    elif resultList[i][0] < resultList[i][1]:
        addScore(matchList[i][1],3)
    else:
        addScore(matchList[i][0],1)
        addScore(matchList[i][1],1)
        
for i in range(len(data)):
    for j in data:
        if j[0] == i:
            sortData.append([i,j[1],j[2],j[3],j[4]])
            
while True:
    menu = input("(d)ata, (t)eam, (s)core: ")
    if not menu.lower() in ['d','t','s']:
        print("Menu doesn't exist")
        continue
    if menu == 'd':
        print("+-----+-----+----+----+------+")
        print(f"|{data[0][0]}|{data[0][1]}|{data[0][2]}|{data[0][3]}|{data[0][4]}")
        print("+-----+-----+----+----+------+")
        for row in sortData:
            print(f"|{row[0]:^5}|{row[1]:^5}|{row[2]:^4}|{row[3]:^4}|{row[4]:^6}|")
    elif menu == 't':
        print("+-No-|--Team--+")
        for i in range(len(teamList)):
            print(f" {i+1:<4}|  {teamList[i]:<6}")
    else:
        print("+-No-|--Team--+-Score-")
        for i in range(len(teamList)):
            print(f" {i+1:<4}|  {teamList[i]:<6}|   {scoreList[i]:<3}")
        

     

