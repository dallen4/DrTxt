import time
crontable = []
outputs = []
with open('diseases.txt', 'r') as file:
	contents = file.readlines()

diseaseDict = dict()

for line in contents:
	currSplit = line.split('|', 3)
	diseaseDict[currSplit[0].lower()] = [currSplit[1], currSplit[2]]

	

def process_message(data):
    if data['channel'].startswith("D"):
        #outputs.append([data['channel'], "from repeat1 \"{}\" in channel {}".format(data['text'], data['channel']) ])
		if data['text'].lower() in diseaseDict.keys():
			outputs.append([data['channel'], "You have (a) {}?".format(data['text'])])
			outputs.append([data['channel'], "Symptoms include: \n\t {}".format(diseaseDict.get(data['text'])[0]).decode('utf-8').replace("\t", "\n\t")])
			outputs.append([data['channel'], "At-home treatments include: \n\t {}".format(diseaseDict.get(data['text'])[1]).decode('utf-8').replace("\t", "\n\t")])
		else:
			outputs.append([data['channel'], "I have no information about that disease."])
