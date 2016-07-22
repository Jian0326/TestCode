#-*-coding:utf-8-*- 
import urllib2
import urllib
import cookielib
import re
import thread
import time
# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent':user_agent}
# try:
# 	request = urllib2.Request(url,headers = headers)
# 	response = urllib2.urlopen(request)
# except urllib2.URLError, e:
# 	if hasattr(e,'code'):
# 		print e.code
# 	if hasattr(e, 'reason'):
# 		print e.reason

# content = response.read().decode('utf-8')
# # print content
# pattern = re.compile('<div.*?author clearfix">(.*?)<div.*?content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
# items = re.findall(pattern, content)
# for item in items:
# 	print '******************************',len(item)
# 	for i in item:
# 		if not re.search("img",i):
# 			print i.replace('<br/>','\n')
# 	print '------------------------------'

class QUSB:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'
		self.headers = {'User-Agent':self.user_agent}
		self.stories = []
		self.enable = False

	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode("utf-8")
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u"连接糗事百科失败,错误原因",e.reason
				return None

	def  getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print '页面加载错误'
			return None
		pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
		items = pattern.findall(pageCode)
		pageStories = []
		for item in items:
			object = []
			for it in item:
				if not re.search("img", it):
					object.append(it.replace('<br/>','\n').strip())
			pageStories.append(object)
		return pageStories

	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self,pageStories,page):
		for story in pageStories:
			input = raw_input()
			self.loadPage()
			if input == 'Q':
				self.enable = False
				return
			print u"第%d页\t发布人：%s\t 赞：%s\n内容：%s" %(page,story[0],story[2],story[1])
			 
	
	def start(self):
		print u"正在读取糗事百科,按回车查看新段子，Q退出"
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)
			
spider = QUSB()
spider.start()
# python 爬虫   糗事百科 
