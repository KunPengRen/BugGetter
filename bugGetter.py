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
import time
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.header import Header

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
KEYWORD4 = "smart contract vulnerabilities"
#only for Github
KEYWORD5 = "smart contract security"
KEYWORD6 = "smart contract analysis tools"

#email address 
#Confidentiality
MSGRECEIVER = "123@foxmail.com"
MSGSENDER = "456@163.com"
MSGAuthorizationCode = "1"

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
	print("Github key1 complete.")
	time.sleep(5)
	pro2 = searchGit(KEYWORD2)
	collectProjects(gitInfo, pro2)
	print("Github key2 complete.")
	time.sleep(5)
	pro3 = searchGit(KEYWORD3)
	collectProjects(gitInfo, pro3)
	print("Github key3 complete.")
	time.sleep(5)
	pro4 = searchGit(KEYWORD4)
	collectProjects(gitInfo, pro4)
	print("Github key4 complete.")
	time.sleep(5)
	pro5 = searchGit(KEYWORD5)
	collectProjects(gitInfo, pro5)
	print("Github key5 complete.")
	time.sleep(5)
	pro6 = searchGit(KEYWORD6)
	collectProjects(gitInfo, pro6)
	print("Github key6 complete.")
	time.sleep(5)
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
	changePro = updateChecker(gitInfo)
	if len(changePro) != 0:
		sendMail(changePro)
	else:
		print("No change.")
	return

#send mail
def sendMail(_changePro):
	text = str()
	for item in _changePro:
		text += str(item)
		text += "\n"
	#set mail content
	message = MIMEText(text, "plain", "utf-8")
	message["from"] = MSGSENDER #"15850673022@163.com"
	message["to"] = MSGRECEIVER #"harleyxiao@foxmail.com"
	message["Subject"] = Header("Github projects update.")
	#set 163 mail server
	smtpObj = smtplib.SMTP() 
	smtpObj.connect("smtp.163.com")    
	smtpObj.login(MSGSENDER, MSGAuthorizationCode)
	smtpObj.sendmail(MSGSENDER, MSGRECEIVER, message.as_string())
	print("Send mail successfully")


#Update checker
def updateChecker(_gitInfo):
	f = open(GIT_FILE, "r", encoding = "utf-8")
	old_Info = dict()
	for i in f:
		li = i.split()
		old_Info[li[0]] = li[1]
	f.close()
	changePro = list()
	for item in _gitInfo.keys():
		if item not in old_Info.keys():
			changePro.append(item)
		elif _gitInfo[item] != old_Info[item]:
			changePro.append(item)
		else:
			continue
	return changePro
	'''
	if _gitInfo.keys() != old_Info.keys():
		return True 
	else:
		for i in _gitInfo.keys():
			if _gitInfo[i] != old_Info[i]:
				return True 
		return False
	'''

#ieee search
def getIeeeHref(_url):
	paperList = list()
	browser = webdriver.Chrome()	#use Chrome
	browser.get(_url)
	time.sleep(5)
	print(1)
	js = 'window.scrollTo(0, document.body.scrollHeight);'
	browser.execute_script(js)
	print(2)
	time.sleep(5)
	browser.execute_script(js)
	print(3)
	paperNum = browser.find_elements_by_xpath("//*[@href]")
	for item in paperNum:
		site = item.get_attribute("href")
		paperList.append(site)
	paperNum = getIeeeNumber(paperList)
	return paperNum
	
#extract paper number from href
def getIeeeNumber(_list):
	paperNumber = set()
	#p = re.compile("(.)+/arnumber=[1-9]{7}$")
	for i in _list:
		if "arnumber" in i:
			num = i[-7:]
			paperNumber.add(num)
	print(len(paperNumber))
	return paperNumber
			
#make ieee search url
def makeIeeeUrl(_prefix, _suffix, _keyword):
	text = _keyword.replace(" ", "%20")
	return _prefix + text + _suffix




#test code
if __name__ == "__main__":
	GithubMain()
	#updateChecker()
	#getIeeeHref(r"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=smart%20contract%20bugs&highlight=false&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL&rowsPerPage=50")
 
