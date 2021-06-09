import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["proyecto3"]


print(mydb)
print(mycol)

i = []

for x in mycol.find():
    i.append(x)
print(i)
print(len(i))
