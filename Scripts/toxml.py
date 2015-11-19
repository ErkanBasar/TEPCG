#!/home/narkem/Anaconda3/bin/python

import re
import os
import readline
from nltk.tokenize import sent_tokenize


raw_articles = '../files/raw_articles/'

corpora = '../files/corpora/'


articles = []

while(True):

	new_articles = []

	for file in os.listdir(raw_articles):
		if file.endswith(".txt"):
			if file not in articles:
				new_articles.append(file)
				articles.append(file)


	if(new_articles):
		for article in new_articles:

			print(article + ": Corpora Generated")
	
			f1 = open(raw_articles + article)

			paragraphs = f1.readlines()

			article = (re.search('(.+?).txt', article)).group(1)	

			f = open(corpora + article + '.xml','w')

			f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\n<article>\n")

			prnum = 0;

			for parag in paragraphs:

				f.write("\n\t<pr id=\"pr" + str(prnum) + "\">\n")
    
				sent_tokenize_list = sent_tokenize(parag)
    
				snum = 0;
    
				for sentence in sent_tokenize_list:
        
					f.write("\t\t<s id=\"s" + str(prnum) + "." + str(snum) + "\">\n\t\t\t" 
							+ "<text>" + sentence + "</text>\n\t\t" 
							+ "</s>\n")
        
					snum = snum + 1
        
				prnum = prnum + 1
    
				f.write("\t</pr>")
    
			f.write("\n</article>")

			f.close()


