#Ran to clean data by summarising crimes into categories and prior records into yes/no

import csv
r = csv.reader(open('finaldbofalltime.csv'))
lines = [l for l in r]

for i in range(1, 519):
    
        '''#if "none" in lines[i][16].lower() or "n/a" in lines[i][16].lower():
           # lines[i][16]= "No"
        #else: lines[i][16] = "Yes"
        
        crime=""
        if "shot" in lines[i][17].lower() or "murdered" in lines[i][17].lower() or "killed" in lines[i][17].lower() or "assassinated" in lines[i][17].lower() or "killing" in lines[i][17].lower() or "murder" in lines[i][17].lower() or "death" in lines[i][17].lower() or "died" in lines[i][17].lower() or "stabbed" in lines[i][17].lower() or "die" in lines[i][17].lower():
            crime+="murder "
            
        if "robbed" in lines[i][17].lower() or "rob" in lines[i][17].lower() or "robbery" in lines[i][17].lower() or "stole" in lines[i][17].lower():
            crime+="robbery "
            
        if "burglary" in lines[i][17].lower() or "burgled" in lines[i][17].lower():
            crime+="burglary "
            
        if "rape" in lines[i][17].lower() or "raped" in lines[i][17].lower() or "sex" in lines[i][17].lower() or "sexually" in lines[i][17].lower() or "molested" in lines[i][17].lower():
            crime+="rape "
            
        if "hostage" in lines[i][17].lower() or "abducted" in lines[i][17].lower() or "abduction" in lines[i][17].lower() or "kidnapping" in lines[i][17].lower() or "kidnapped" in lines[i][17].lower():
            crime+="abduction "
        
        if crime=="":
            crime = "N/A"
            
        lines[i][17] = crime''' 
        num=0
        num1=0
        num2=0
        num3=0
        num4=0
        
        x = lines[i][21]
        if int(x) > 1: 
            print(i)
       
        x = lines[i][22]
        if int(x) > 1:
            print(i)
    
        
        x = lines[i][23]
        if int(x) > 1:
            print(i)
    
        
        
        
        
            
'''writer = csv.writer(open('finaldbofalltime.csv', 'w'))
writer.writerows(lines)'''