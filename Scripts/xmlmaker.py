import json
import os
import re


true_folder = "../files/trues"

last_corpora = "../files/corpora/last_corpora/"

articles = []

while(True):

	time.sleep(10)	

	new_articles = []

	for file in os.listdir(true_folder):
			if file not in articles:
				new_articles.append(file)
				articles.append(file)

	if(new_articles):

		for farticle in new_articles:

			article = (re.search('(.+?)_', farticle)).group(1)

			with open(true_folder + article + '_true.json', 'r') as f:
				jsonobj = json.load(f)

			enstring = "<?xml version='1.0' encoding='UTF-8'?>\n<root>\n	"
			trstring = "<?xml version='1.0' encoding='UTF-8'?>\n<root>\n	"
	
			i = 1
			jslen = len(jsonobj)

			for js in jsonobj:

				if(i == jslen):

					enstring = enstring + "<s id='s" + str(i) + "'>" + js['text_en'] + "</s>\n"
					trstring = trstring + "<s id='s" + str(i) + "'>" + js['text_tr'] + "</s>\n"

				else:
	
					enstring = enstring + "<s id='s" + str(i) + "'>" + js['text_en'] + "</s>\n	"
					trstring = trstring + "<s id='s" + str(i) + "'>" + js['text_tr'] + "</s>\n	"
	
				i = i + 1

			enstring = enstring + "</root>"
			trstring = trstring + "</root>"
	
			if(not (os.path.isfile(last_corpora + article + '_true_en.xml'))):
				with open(last_corpora + article + '_true_en.xml', 'w') as f:
					f.write(enstring)
	
			if(not (os.path.isfile(last_corpora + article + '_true_tr.xml'))):
				with open(last_corpora + article + '_true_tr.xml', 'w') as f:
					f.write(trstring)



