#Webscraper which collects the data we need and writes it to a CSV
from bs4 import BeautifulSoup
import urllib
import csv
import warnings
warnings.filterwarnings("error")
r = urllib.urlopen('https://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html').read()
soup = BeautifulSoup(r,"html.parser")
print type(soup)

Execution=[]
OffInfo=[]
LinkLS=[]
Last=[]
First=[]
Number=[]
Age=[]
Date=[]
Race=[]
County=[]

for i in soup.findAll('tr'):
    td = i.findAll('td')
    print("k")
    print(len(td))
    for s, p in enumerate(td):
        if s==0:
            p.text.encode('utf-8')
            Execution.append(p.text)
        if s==1:
            for l in p.findAll('a'):
                OffInfo.append(l.get('href'))
        if s==2:
            for l in p.findAll('a'):
                LinkLS.append(l.get('href'))
        if s==3:
            p.text.encode('utf-8')
            Last.append(p.text)
        if s==4:
            p.text.encode('utf-8')
            First.append(p.text)
        if s==5:
            p.text.encode('utf-8')
            Number.append(p.text)
        if s==6:
            p.text.encode('utf-8')
            Age.append(p.text)
        if s==7:
            p.text.encode('utf-8')
            Date.append(p.text)
        if s==8:
            p.text.encode('utf-8')
            Race.append(p.text)
        if s==9:
            p.text.encode('utf-8')
            County.append(p.text)

print(OffInfo)
#To obtain statements from each link in the table:
root_url = "https://www.tdcj.state.tx.us/death_row/"

states = []

for link in LinkLS:
    print("ori")
    obtain = urllib.urlopen(root_url+link)
    soup = BeautifulSoup(obtain,"html.parser")
    #stat2 = BeautifulSoup(obtain.text)
    ps = soup.find_all('p')
    temp = ""
    for i in range(6, len(ps)):
        temp = temp + ps[i].get_text()
        temp.encode('utf-8')
    states.append(temp)

f = csv.writer(open("TexasDB.csv", "w"))
f.writerow(["Execution", "Lastname", "Firstname", "TDCJnumber", "Age", "Date", "Race", "County", "Statement", "DateReceived", "Education", "DateOfCrime", "AgeAtCrime", "Height", "Weight", "PriorOccupation", "PriorRecord", "Crime", "VictimRaceGender"]) # Write column headers as the first line


dateReceived = []
education = []
dateCrime = []
ageAtCrime = []
height = []
weight = []
priorOccupation = []
priorRecord = []
crime = []
victimRaceGender = []
count = 0

for link in OffInfo:
    print(link)
    image = 0 #flag for jpg's
    if link.find("jpg") != -1:
        image = 1
        dateReceived.append("pdf")
        education.append("pdf")
        dateCrime.append("pdf")
        ageAtCrime.append("pdf")
        height.append("pdf")
        weight.append("pdf")
        priorOccupation.append("pdf")
        priorRecord.append("pdf")
        crime.append("pdf")
        victimRaceGender.append("pdf")

    else:
        obtain = urllib.urlopen(root_url+link)
        soup = BeautifulSoup(obtain,"html.parser")

        x=0
        y=0
        for i in soup.findAll('tr'):
            td = i.findAll('td')
            x+=1
            for s, p in enumerate(td):
            #print(x)
            #print(s)
                if x== 3 and s==1:
                #if offinfo ends in pdf
                    p.text.encode('utf-8')
                    dateReceived.append(p.text)

                if x==6 and s ==1:
                    p.text.encode('utf-8')
                    education.append(p.text)

                if x==7 and s==1:
                    p.text.encode('utf-8')
                    dateCrime.append(p.text)


                if x==8 and s==2:
                    p.text.encode('utf-8')
                    ageAtCrime.append(p.text)

                if x==13 and s==2:
                    p.text.encode('utf-8')
                    height.append(p.text)

                if x==14 and s==2:
                    p.text.encode('utf-8')
                    weight.append(p.text)



    #ps = soup.find_all('p')
        temp2 = soup.findAll('p')

        try:
            #print temp2[1].br.nextSibling

            occ = temp2[1].br.nextSibling
            occ.encode('utf-8')
            priorOccupation.append(occ)
        except (IndexError, AttributeError) as e:
            priorOccupation.append("pdf")

        try:
            pri = temp2[2].br.nextSibling
            pri.encode('utf-8')
            priorRecord.append(pri)
        except (IndexError, AttributeError) as e:
            priorRecord.append("pdf")

        try:
            cri = temp2[3].br.nextSibling
            cri.encode('utf-8')
            crime.append(cri)
        except (IndexError, AttributeError) as e:
            crime.append("pdf")

        try:
            vic = temp2[5].br.nextSibling
            vic.encode('utf-8')
            victimRaceGender.append(vic)
        except (IndexError, AttributeError) as e:
            victimRaceGender.append("pdf")


for i in range(0, 530):
    f.writerow([Execution[i].encode('utf-8'), Last[i].encode('utf-8'), First[i].encode('utf-8'), Number[i].encode('utf-8'), Age[i].encode('utf-8'), Date[i].encode('utf-8'), Race[i].encode('utf-8'), County[i].encode('utf-8'), states[i].encode('utf-8'), dateReceived[i].encode('utf-8'), education[i].encode('utf-8'), dateCrime[i].encode('utf-8'), ageAtCrime[i].encode('utf-8'), height[i].encode('utf-8'), weight[i].encode('utf-8') , priorOccupation[i].encode('utf-8'), priorRecord[i].encode('utf-8'), crime[i].encode('utf-8'), victimRaceGender[i].encode('utf-8')])
    i += 1
