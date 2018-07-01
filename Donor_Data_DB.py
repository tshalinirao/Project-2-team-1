
import requests as req
import pprint as pp
import pandas as pd
import sys, json, pymongo
from pymongo import MongoClient
import os 
import csv

##Connecting to Database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Declare the database
db = client.Donor_Data
# Declare the collection
collection = db.projects


# print(collection.count())


results = db.projects.find()
for result in results:
    print(result)



url = "https://api.donorschoose.org/common/json_feed.html?APIKey=DONORSCHOOSE&newSince=1483256682&max=1000"

# Who was the director of the movie Aliens?
data = req.get(url).json()
post_id = collection.insert_many(data['proposals'])
data


# In[58]:


cursor = collection.find({},
    {'_id':0,'id': 1, 'title': 1, 'percentFunded': 1, 'numDonors': 1,'costToComplete':1,'numStudents':1,
     'totalPrice':1,'teacherId':1,'schoolTypes.id':1,'schoolName':1,'city':1,'zip':1,
     'state':1,'latitude':1,'longitude':1,'expirationDate':1,'fundingStatus':1,'gradeLevel.name':1,'povertyType.label':1,
     'subject.name':1})

flattened_records = []
for data_rec in cursor:
   #print(data_rec['gradeLevel']['name'])
    flattened_record = {
            'id': data_rec['id'],
            'title': data_rec['title'],
            'percentFunded' : data_rec['percentFunded'] if 'percentFunded' in data_rec.keys() else '',
            'numDonors': data_rec['numDonors'] if 'numDonors' in data_rec.keys() else '',
            'costToComplete' : data_rec['costToComplete'] if 'costToComplete' in data_rec.keys() else '',
            'numStudents': data_rec['numStudents'] if 'numStudents' in data_rec.keys() else '',
            'totalPrice' : data_rec['totalPrice'] if 'totalPrice' in data_rec.keys() else '',
            'schoolName': data_rec['schoolName'] if 'schoolName' in data_rec.keys() else '',
            'zip' : data_rec['zip'] if 'zip' in data_rec.keys() else '',
            'state': data_rec['state'] if 'state' in data_rec.keys() else '',
            'latitude' : data_rec['latitude'] if 'latitude' in data_rec.keys() else '',
            'longitude': data_rec['longitude'] if 'longitude' in data_rec.keys() else '',
            'expirationDate' : data_rec['expirationDate'] if 'expirationDate' in data_rec.keys() else '',
            'fundingStatus': data_rec['fundingStatus'] if 'fundingStatus' in data_rec.keys() else '',
            'gradelevel':data_rec['gradeLevel']['name'] if 'gradeLevel' in data_rec.keys() else '',
            'povertyType':data_rec['povertyType']['label'] if 'povertyType' in data_rec.keys() else '',
            'subject':data_rec['subject']['name'] if 'subject' in data_rec.keys() else ''
        
            
        
        }
    flattened_records.append(flattened_record)
    
#print(flattened_records)
# # Step 2: Iterate through the list of flattened records and write them to the csv file
with open('stack_039.csv', 'w') as outfile:
    fields = ['_id', 'id', 'title', 'percentFunded','numDonors','costToComplete','numStudents','totalPrice' ,'schoolName','zip','state'
        ,'latitude' ,'longitude','expirationDate' ,'fundingStatus','gradelevel','povertyType','subject']
    write = csv.DictWriter(outfile, fieldnames=fields)
    write.writeheader()
    for flattened_record in flattened_records:
        write.writerow(flattened_record)


# In[59]:


# print("id,title")
# cursor = collection.find()

# while (cursor.hasNext()) {
#     jsonObject = cursor.next();
#     print(jsonObject._id.valueOf() + "," + jsonObject.id + ",\"" + jsonObject.title +"\"")
# }

