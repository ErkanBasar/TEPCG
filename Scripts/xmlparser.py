#!/home/narkem/Anaconda3/bin/python

import os
import re
import json
import time
import xml.etree.ElementTree as ET

corpora = '../files/corpora/'

corpora_json = '../files/corpora_json/'


articles = []

while(True):

	time.sleep(10)	

	new_articles = []

	for file in os.listdir(corpora):
		if file.endswith(".xml"):
			if file not in articles:
				new_articles.append(file)
				articles.append(file)

	if(new_articles):

		for article in new_articles:

			print(article + ": Corpora parsed in JSON")

			article = (re.search('(.+?).xml', article)).group(1)

			tree = ET.parse(corpora + article + '.xml')
			root = tree.getroot()

			parsedjson = []

			i = 0

			for paragraph in root.findall('pr'):

			    j = 1

			    for sentence in paragraph.findall('s'):
        
			        sent_num = "s"+str(i)+"."+str(j)

			        text = sentence.find('text').text
        
			        sent_list = { 'sent_num' : sent_num, 'text' :  text}
        
			        parsedjson.append(sent_list)

			        j = j + 1
        
			    i = i + 1

			with open(corpora_json + article + '.json', 'w') as f:
					json.dump(parsedjson, f)	



