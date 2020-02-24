#-*- coding = utf-8 -*-

'''
This program helps semi-automatically extend the Jiuzhou framework 
by sending query requests to the IEEE Digital Library, 
ACM Digital Library, 
and Github.
'''

#import library
import requests 

https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=smart%20contract%20bugs&highlight=true&returnFacets=ALL&returnType=SEARCH&refinements=ContentType:Conferences&refinements=ContentType:Journals

#define url and text
#eg. https://github.com/search?q=smart+contract+bugs
GIT_TYPE = 1
GIT_SEARCH_TEXT = ""
GIT_SEARCH = "https://github.com/search?q="
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
	r =requests.get(_)

 
