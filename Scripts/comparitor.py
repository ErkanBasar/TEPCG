#!/home/narkem/Anaconda3/bin/python

import os
import re
import json
import time
import xml.etree.ElementTree as ET

corpora = '../files/corpora/'

comp_folder = '../files/comparison/'


articles = []

while(True):

	time.sleep(10)

	new_articles = []

	for file in os.listdir(corpora):
		if file.endswith("_en.xml"):
			if file not in articles:
				new_articles.append(file)
				articles.append(file)

	if(new_articles):

		for article in new_articles:

			print(article + ": Comparison file are initiated.")

			article = (re.search('(.+?)_', article)).group(1) 

			lang = "_en"

			tree_en = ET.parse(corpora + article + lang + '.xml')
			root_en = tree_en.getroot()

			comparison = []

			i = -1

			for parag in root_en.findall('pr'):

			    i = i + 1
    
			    j = 0

			    for sent in parag.findall('s'):
        
			        j = j + 1

			        sent_num = "s"+str(i)+"."+str(j) # s{{paragraph num}}.{{sentence num}}
        
			        entry = {'sent_num': sent_num,'true':0,'false':4}
			        comparison.append(entry)


			with open(comp_folder + article + '_comp.json', 'w') as f:
			        json.dump(comparison, f)





