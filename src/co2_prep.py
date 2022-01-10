#co2 prep

import json

fileName = "owid-co2-data.json"
f = open(fileName,)
data = json.load(f)

co2 = []

for designation in data:
    location = designation
    year = ""
    localCo2 = 0
    globalPercent = 0
    
    if location == "United States":
        for a in data[location]:
            for b in data[location][a]:
                
                for c in b:
                    if c == "year" and b.get(c) > 1949 and b.get(c) < 2011:
                        year = int(b.get(c))
                        localCo2 = b.get("co2")
                        globalPercent = b.get("share_global_co2")
                        newEntry = []
                        newEntry.append(year)
                        newEntry.append(localCo2)
                        newEntry.append(globalPercent)
                        newEntry.append(localCo2 * 1)
                        co2.append(newEntry)


strO = str(co2)
newO = ""
prevC = ""
for c in strO:
    # prevC = c
    if c == "," and prevC == "]":
        newO += "\n"
    elif c == "]":
        prevC = c
        # newO += ","
    elif c == "[":
        prevC = c
        # continue
    elif c == ",":
        newO += " "
    elif c == " ":
        preC = c
    else:
        newO += c
        prevC = c
    prevC = c

f = open("co2_output.txt", "w")
f.write(str(newO))
f.close()
