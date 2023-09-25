import sqlite3
 
con = sqlite3.connect(input())
cur = con.cursor()

names = {"1": "Antipodally opalovaci",
         "2" : "Welsh Green Common",
         "3": "Hungarian Hornbill",
         "4": "Hebridean Black"}

dang = int(input())

result = cur.execute(f"""SELECT type_id, height, danger FROM registry
                        WHERE danger >= {dang}
                        ORDER BY distance DESC""").fetchall()

for elem in result:
    if str(elem[0]) == "1":
        name = names["1"]
    elif str(elem[0]) == "2":
        name = names["2"]
    elif str(elem[0]) == "3":
        name = names["3"]
    elif str(elem[0]) == "4":
        name = names["4"]
    print(name + " " + str(elem[1]) + " " + str(elem[2]))
    
con.close()
