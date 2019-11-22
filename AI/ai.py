from get_sym import *
structuredData=diseases
#print("##########################################ai.py is called1##################################")
#structuredData2=mainx()
#print("##########################################ai.py is called2###################################")
listp=[]
def sort(listp):
	l=len(listp)
	for i in range(0,l):
		for j in range(0,l-i-1):
			if(listp[j][1]>listp[j+1][1]):
				temp=listp[j]
				listp[j]=listp[j+1]
				listp[j+1]=temp
	return listp

for i in structuredData:
	flag=0
	for j in i:
		for k in structuredData2:
			if(k==j[0]):
				j[2]=1
				flag=1
				break

	if(flag==1):
		listp.append(i)

print (listp)

for i in listp:
	sum=0
	for j in i:
		if(j[2]==1):
			sum+=j[1]
	i.append(sum)


print(listp)

#listp= [['jaundice', ['pain', 30,1], ['a', 4, 1], 34], ['dengue', ['pain', 1, 40], ['b', 0, 50], 40]]

sum=0
for i in listp:
	sum+=i[3]

for i in listp:
	i.append(i[3]/sum)
print(listp)

listp=sort(listp)

print(listp)

#listp = [['jaundice', ['pain', 1, 30], ['a', 1, 4], 34, 0.4594594594594595], ['dengue', ['pain', 1, 40], ['b', 0, 50], 40, 0.5405405405405406]]
