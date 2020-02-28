#-*- coding = utf-8 -*-

'''
This program helps semi-automatically extend the Jiuzhou framework 
by sending query requests to the IEEE Digital Library, 
ACM Digital Library, 
and Github.
'''

#import library
import requests 
from bs4 import BeautifulSoup
import re
import json

#https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=smart%20contract%20bugs&highlight=true&returnFacets=ALL&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals

#define url and text
#eg. https://github.com/search?q=smart+contract+bugs
GIT_TYPE = 1
GIT_SEARCH_TEXT = ""
GIT_SEARCH = "https://api.github.com/search/repositories?q="
GIT_SUFFIX = "&per_page="
#eg. https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=smart%20contract%20bugs&highlight=true&returnFacets=ALL&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals
IEEE_TYPE = 2
IEEE_SEARCH_TEXT = ""
IEEE_SEARCH = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=" + IEEE_SEARCH_TEXT +"&highlight=true&returnFacets=ALL&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals"
#wait 
ACM_TYPE = 3
ACM_SEARCH_TEXT = ""
ACM_SEARCH = ""

#define search keywords
KEYWORD1 = "smart contract bugs"
KEYWORD2 = "smart contract problems"
KEYWORD3 = "smart contract defects"
KEYWORD4 = "smart contract vulnerability"
#only for Github
KEYWORD5 = "smart contract security"
KEYWORD6 = "smart contract analysis tool"

#functions

#get url, send query and return result
def getPage(_url, _text, _type):
	search_text = _url
	if _type == GIT_TYPE:
		text = _text.replace(" ", "+")
		search_text += text
	r = getHtml(search_text)
	if r:
		return r, search_text
	else:
		return None

#This function is used to get html code
def getHtml(_url):
	headers = {'user_agent': 'Mozilla/5.0'}
	r = requests.get(_url, headers = headers)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	return r


#This function used BeautifulSoup to parser html
def parserHtml(_page, _type):
	soup = BeautifulSoup(_page, "html.parser")
	if _type == GIT_TYPE:	
		#获取项目数
		n_pattern = "<h3>(.)*<>"
		print(soup.find_all("h3", string = re.compile("results")))
		print(len(soup.find_all("a")))

#This function uses re to get target string
def parserHtml_re(_text, _url,  _type):
	if _type == GIT_TYPE:
		proInfo = dict()
		#转变数据格式
		page_dict = _text.json()
		#get project number to computer the number of page
		proNum = page_dict["total_count"]
		if proNum < 30:
			getGithubProInfo(page_dict, proInfo)
		while proNum >= 0:
			getGithubProInfo(page_dict, proInfo)
			proNum -= 30
			search_text = _url
			if proNum <= 100:
				search_text += "&per_page=100"
			for key in proInfo.keys():
				print(key, proInfo[key])



#This function is used to get Githun project name
def getGithubProInfo(_dict, _proInfo):
	#this is list
	for item in _dict["items"]:
		for key in item.keys():
			_proInfo[item["full_name"]] = item["updated_at"] 
	return 


#test code
(page, url) = getPage(GIT_SEARCH, KEYWORD5, GIT_TYPE)
parserHtml_re(page, url, GIT_TYPE)
 
