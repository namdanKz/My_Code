import sys
def read_file(filename):
    text = open(filename).read()
    text = text.splitlines()
    text2 = [x.split(",") for x in text]
    text3 = []
    for i in range(len(text2)):
        if i == 0:
            continue
        text3.append(text2[i])
    return text3

def print_team(data,team):
    for i in data:
        #print(i)
        if team in i:
            print(f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]}")
filename = "data1.txt"
team_list = read_file(filename)
for i in range(len(team_list)):
    x = team_list[i]
    score = int(x[2])*3 + int(x[3])
    team_list[i].append(score)
while True:
    team = input("Team: ")
    if team.lower() == "q":
        print("Bye") 
        sys.exit()
    print_team(team_list,team)