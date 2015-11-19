

from django.shortcuts import render
from django.views.generic import View

from django.conf import settings

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import goslate

import random

import json

import re

import os


corpora = 'files/corpora/'

comp_folder = 'files/comparison/'

corpora_json = 'files/corpora_json/'

compfalse_folder = 'files/comp_false/'

true_folder = 'files/trues/'

false_folder = 'files/falses/'

gs = goslate.Goslate()


class Home(View):
	
	def get(self, request):
				
		template = 'base.html'

		return render(request, template, {	})




class Easy(View):

	def get(self, request):

		warning = ''
		
		while(True):

			articles = []
			for file in os.listdir(corpora_json):
				if file.endswith("_en.json"):
					articles.append(file)

			if(articles == []):
				template = 'no_sent.html'
				return render(request, template, {
					
				})

			random_article = random.choice(articles)

			article = (re.search('(.+?)_', random_article)).group(1)
			
			article_en = corpora_json + article + '_en.json'
			article_tr = corpora_json + article + '_tr.json'
			comp_file = comp_folder + article + '_comp.json'
			true_file = true_folder + article + '_true.json'
			false_file = false_folder + article + '_false.json'


			sent_list = parseArticles(article_en, article_tr) #random sentence

			item_en = sent_list[0]
			text_en = item_en['text']
			sent_num = item_en['sent_num']


			with open(comp_file, 'r') as f:
				comparison = json.load(f)

			comp = next((comp for comp in comparison if comp['sent_num'] == sent_num), None)


			if(len(sent_list) == 1):

				false_en = {'sent_num': sent_num, 'lang': 'en', 'text': text_en}	
				appendjson(false_file, false_en)

				removejson(comp_file, comp)

				removejson(article_en, item_en)

				continue;
			
			item_tr = sent_list[1]
			text_tr = item_tr['text']
			

			if(comp['true'] + comp['false'] < 5):
				break;


			elif(comp['true'] > comp['false']):

				trues = {'text_en': text_en, 'text_tr': text_tr}	

				appendjson(true_file, trues)

				removejson(comp_file, comp)

				removejson(article_en, item_en)

				removejson(article_tr, item_tr)


			elif(comp['false'] > comp['true']):

				false_en = {'sent_num': sent_num, 'lang': 'en', 'text': text_en}	
				appendjson(false_file, false_en)

				false_tr = {'sent_num': sent_num, 'lang': 'tr', 'text': text_tr}	
				appendjson(false_file, false_tr)

				removejson(comp_file, comp)

				removejson(article_en, item_en)

				removejson(article_tr, item_tr)

		trans_en = gs.translate(text_en, 'tr')

		trans_tr = gs.translate(text_tr, 'en')

		wordcloud = WordCloud().generate(text_en)
		plt.imshow(wordcloud)

		fig1 = plt.gcf()
		fig1.savefig('static/images/out2.png', dpi=100)
				
		template = 'easy.html'

		return render(request, template, {
				'sent_en': text_en,
				'sent_tr': text_tr,
				'sent_num': sent_num,
				'article' : article,
				'trans_en' : trans_en,
				'trans_tr' : trans_tr,
		})




class TrueE(View):

	def get(self, request, snum, article):

		vote_as(comp_folder + article + '_comp.json', snum, 'true')

		return Easy.as_view()(self.request)




class FalseE(View):

	def get(self, request, snum, article):

		vote_as(comp_folder + article + '_comp.json', snum, 'false')

		return Easy.as_view()(self.request)




class Hard(View):
	
	def get(self, request):

		articles = []
		for file in os.listdir(false_folder):
			if file.endswith("_false.json"):
				articles.append(file)

		if(articles == []):
			template = 'no_sent.html'
			return render(request, template, {
					
			})

		random_article = random.choice(articles)

		article = (re.search('(.+?)_', random_article)).group(1)

		false_file = false_folder + article + '_false.json'


		with open(false_file, 'r') as f:
			falsejson = json.load(f)

		falselen = len(falsejson)

		false_en = ""
		false_tr = ""
		sent_numen = ""
		sent_numtr = ""
			
		while(falselen):
			falseen = random.choice(falsejson)
			if(falseen['lang'] == 'en'):
				false_en = falseen['text']
				sent_numen = falseen['sent_num']
				break;
		while(falselen):
			falsetr = random.choice(falsejson)
			if(falsetr['lang'] == 'tr'):
				false_tr = falsetr['text']
				sent_numtr = falsetr['sent_num']
				break;

		if(false_en == "" or false_tr == ""):
			template = 'no_sent.html'
			return render(request, template, {
					
			})

		trans_en = gs.translate(false_en, 'tr')

		trans_tr = gs.translate(false_tr, 'en')

		wordcloud = WordCloud().generate(false_en)
		plt.imshow(wordcloud)

		fig1 = plt.gcf()
		fig1.savefig('static/images/out.png', dpi=100)
		
		template = 'hard.html'

		return render(request, template, {
				'false_en': false_en,
				'false_tr': false_tr,
				'sent_numen': sent_numen,
				'sent_numtr': sent_numtr,
				'article' : article,
				'trans_en' : trans_en,
				'trans_tr' : trans_tr,
		})


class TrueH(View):

	def get(self, request, snumen, snumtr, article):

		hard_true(article, snumen, snumtr)

		return Hard.as_view()(self.request)



class FalseH(View):

	def get(self, request, snumen, snumtr, article):

		return Hard.as_view()(self.request)




############################################ methods



def hard_true(article, snumen, snumtr):

		false_file = false_folder + article + '_false.json'
		compfalse_file = compfalse_folder + article + '_comp_false.json'
		falsetrue_file = true_folder + article + '_true.json'

		with open(false_file, 'r') as f:
			falsejson = json.load(f)

		falseen = next((falseen for falseen in falsejson if (falseen['sent_num'] == snumen) and (falseen['lang'] == 'en')), None)
		falsetr = next((falsetr for falsetr in falsejson if falsetr['sent_num'] == snumtr and (falsetr['lang'] == 'tr')), None)
		result = {"content":[falseen,falsetr],"tn":1}
		
		
		if(not (os.path.isfile(compfalse_file))):

			
			appendjson(compfalse_file, result)

		else:
			with open(compfalse_file, 'r') as f:
				compjson = json.load(f)
			
			idk = False
			for comp in compjson:

				if(comp['content'] == result['content']):
					idk = True
					if(comp['tn'] < 4):
						comp['tn'] = comp['tn'] + 1
						
						with open(compfalse_file, 'w') as f:
							json.dump(compjson, f)
					else:

						falsejson.remove(falseen)

						falsejson.remove(falsetr)

						with open(compfalse_file, 'r') as f:
							compjson = json.load(f)

						for comp in compjson:

							

							if(comp['content'] == []):

								compjson.remove(comp)

							else:

								if falseen in comp['content'] or falsetr in comp['content']:

									compjson.remove(comp)

						for comp in compjson:

							if falsetr in comp['content']:

								compjson.remove(comp)

						for comp in compjson:

							if falseen in comp['content']:

								compjson.remove(comp)
										

						if(falsejson == []):

							os.remove(false_file)

						else:

							with open(false_file, 'w') as f:
								json.dump(falsejson,f)

						if(compjson == [{"content":[],"tn":0}] or compjson == []):

							os.remove(compfalse_file)

						else:

							with open(compfalse_file, 'w') as f:
								json.dump(compjson, f)

						result3 = {"text_en":falseen['text'],"text_tr":falsetr['text']}
						
						appendjson(falsetrue_file, result3)

			if(not idk):

				appendjson(compfalse_file, result)



def appendjson(file_name, item):

	if(os.path.isfile(file_name)):  #if file already exists; load it first
		with open(file_name, 'r') as f:
			hedejson = json.load(f)
	else:
		hedejson = []
				
	hedejson.append(item)

	with open(file_name, 'w') as f:
		json.dump(hedejson, f)	




def removejson(file_name, item):

	with open(file_name, 'r') as f:
		hedejson = json.load(f)

	hedejson.remove(item)

	if(hedejson == []): #if list is empty; remove the file
		os.remove(file_name)
	else:
		with open(file_name, 'w') as f:
			json.dump(hedejson, f)





def vote_as(file_name, snum, vote):

		with open(file_name, 'r') as f:
			comparison = json.load(f)

		comp = next((comp for comp in comparison if comp['sent_num'] == snum), None)

		comp[vote] = comp[vote] + 1 

		with open(file_name, 'w') as f:
				json.dump(comparison, f)




def parseArticles(file_en, file_tr):

	with open(file_en, 'r') as f:
		articles_en = json.load(f)

	with open(file_tr, 'r') as f:
		articles_tr = json.load(f)

	en_sent = random.choice(articles_en)

	tr_sent = next((sent for sent in articles_tr if sent['sent_num'] == en_sent['sent_num']), None)

	if(tr_sent == None):			
		sent_list = [en_sent]
	else:
		sent_list = [en_sent, tr_sent]

	return sent_list




