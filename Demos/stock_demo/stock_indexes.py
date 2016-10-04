from yahoo_finance import Share
import json
import os, sys
from bs4 import BeautifulSoup
import urllib2

# Get top 10 most active stocks
class stockIndexes:

	def __init__(self,top):
		self.main(top)

	def get_indexes(self):	
		return self.indexes


	def main(self,top):	
		send_request = True


		url = "http://www.wsj.com/mdc/public/page/2_3021-activcomp-actives.html"
		
		while(send_request):
			request = urllib2.Request(url)
			try:
				content = urllib2.urlopen(url)
			except urllib2.URLError as e:
				if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					print 'Reason: ', e.reason
				elif hasattr(e, 'code'):
					print 'The server couldn\'t fulfill the request.'
					print 'Error code: ', e.code
			else:
				send_request = False

		marketHtml = content.read()
		content.close()
		count = 0

		soup = BeautifulSoup(marketHtml,"html5lib")
		active_stock_indexes = []
		for tag in soup.find_all('a'):
			string = str(tag.string)
			index_open = string.find("(")
			index_close = string.find(")")

			if(index_open != -1 and index_close != -1):
				active_stock_indexes.append(string[index_open+1:index_close])
				count += 1

			if(count == top):
				break

		self.indexes = (count,active_stock_indexes)	