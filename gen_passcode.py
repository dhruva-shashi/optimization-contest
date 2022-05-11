import json
import random


def rand_str(n):
    arr = []

    for i in range(0, 26):
        arr.append(chr(ord('a')+i))
    for i in range(0, 26):
        arr.append(chr(ord('A')+i))
    for i in range(0, 10):
        arr.append(chr(ord('0')+i))

    random.shuffle(arr)

    res = ''

    for i in range(0, n):
        res += arr[random.randint(0, 61)]

    return res


# Write comma separated teamnames inside the team list
teams = []
team_code = {}

for team in teams:
    team_code[rand_str(20)] = team


f = open('teams-passcode-mapping.json', 'w')
json.dump(team_code, f, indent=4)
f.close()

