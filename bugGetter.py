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
GIT_PAGE_NUMBER = "1"
GIT_SUFFIX = "&per_page=100&page="+GIT_PAGE_NUMBER
GIT_FILE = "githubProInfo.txt"
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
KEYWORD6 = "smart contract analysis tools"

#functions

#make search url
def makeUrl(_search, _keyword, _suffix, _type):
	url = _search
	if _type == GIT_TYPE:
		text = _keyword.replace(" ", "+")
		url += text
		url +=  _suffix
	return url


#get url, send query and return result
def getPage(_url, _text, _suffix, _type):
	search_text = _url
	if _type == GIT_TYPE:
		text = _text.replace(" ", "+")
		search_text += text
		search_text += _suffix
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

def getPage_re(_url, _type):
	search_text = _url
	if _type == GIT_TYPE:
		r = getHtml(search_text)
		if r:
			return r, search_text
		else:
			return None

#This function uses re to get target string
def parserHtml_re(_text, _url,  _type, _keyword):
	if _type == GIT_TYPE:
		proInfo = dict()
		#tranfer data struct
		page_dict = _text.json()
		#get project number to computer the number of page
		proNum = page_dict["total_count"]
		if proNum <= 100:
			getGithubProInfo(page_dict, proInfo)
			#print(len(proInfo))
			return proInfo
		else:
			while proNum >= 0:
				getGithubProInfo(page_dict, proInfo)
				proNum -= 100
				new_url = makeUrl(GIT_SEARCH, _keyword, GIT_SUFFIX, GIT_TYPE)
				new_url = addGitPage(new_url)
				#page_num += 1
				(page, url) = getPage_re(new_url, GIT_TYPE)
				page_dict = page.json()
			#print(len(proInfo))
			return proInfo

#This function makes the "GIT_PAGE_NUMBER" add 1
def addGitPage(_url):
	new_url = ""
	page = _url[-1]
	page_num = eval(page)
	page_num += 1
	_url = _url[:-1]
	_url += str(page_num)
	new_url = _url
	return new_url



#This function is used to get Githun project name
def getGithubProInfo(_dict, _proInfo):
	#this is list
	for item in _dict["items"]:
		for key in item.keys():
			_proInfo[item["full_name"]] = item["updated_at"] 
	return 

#This function merges several query results into a collection
def collectProjects(_main, _part):
	for proName in _part:
		if proName not in _main.keys():
			#new project
			_main[proName] = _part[proName]

#Search Github function
def searchGit(keyword):
	(page, url) = getPage(GIT_SEARCH, keyword, GIT_SUFFIX, GIT_TYPE)
	proInfo = parserHtml_re(page, url, GIT_TYPE, keyword)
	return proInfo

#search Github main function
def GithubMain():
	gitInfo = dict()
	pro1 = searchGit(KEYWORD1)
	collectProjects(gitInfo, pro1)
	pro2 = searchGit(KEYWORD2)
	collectProjects(gitInfo, pro2)
	pro3 = searchGit(KEYWORD3)
	collectProjects(gitInfo, pro3)
	pro4 = searchGit(KEYWORD4)
	collectProjects(gitInfo, pro4)
	pro5 = searchGit(KEYWORD5)
	collectProjects(gitInfo, pro5)
	pro6 = searchGit(KEYWORD6)
	collectProjects(gitInfo, pro6)
	print("Collected a total of ", len(gitInfo), " projects.")
	f = open(GIT_FILE, "w+")
	for proName in gitInfo.keys():
		line = str()
		line += str(proName)
		line += " "
		line += gitInfo[proName]
		line += "\n"
		f.write(line)
	f.close()
	return


#test code
if __name__ == "__main__":
	GithubMain()



 
