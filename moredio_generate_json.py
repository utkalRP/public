import csv, json

data =[]

name=""
tag=""
low=""
high=""
thumb="https://raw.githubusercontent.com/utkalRP/ExoPlayer/master/app/src/main/res/drawable/radio.png"
web=""
genre=[]
lang=[]
g=[]
l=[]
with open('in.csv') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        name=row['name']
        row['tag'] = tag
        low=row['low']
        row['high'] = high
        row['thumb'] = thumb
        row['web'] = web
        g.append(row['genre'])
        l.append(row['lang'])
        row['genre']=g.copy()
        row['lang']=l.copy()
        data.append(row)
        g.clear();
        l.clear()

with open('out.json','w') as jsonFile:
    jsonFile.write(json.dumps(data,indent=4))
