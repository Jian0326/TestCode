#-*-coding:utf-8-*- 
import urllib2
import urllib
import cookielib
import re
import thread
import time

class Tool:
	#去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
	"""docstring for BDTB"""
	def __init__(self, baseUrl,seeLZ,floorTag):
		self.baseUrl = baseUrl
		self.seeLZ = '?see_lz' + str(seeLZ)
		self.file = None
		self.floor = 1
		#是否写入楼分隔符的标记
		self.floorTag = floorTag
		#默认的标题，如果没有成功获取到标题的话则会用这个标题
		self.defaultTitle = u'百度贴吧'
		self.tool = Tool()

	def getPage(self,pageNum):
		try:
			url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u"连接百度贴吧失败,错误原因",e.reason
                return None

	def getTitle(self):
		page = self.getPage(1)
		pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow  .*?>(.*?)</h3>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getPageNum(self,page):
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getContent(self,page):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items = re.findall(pattern,page)
		contents = []
		for item in items:
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content.encode('utf-8'))
		return contents

	def setFileTitle(self,title):
		if title is not None:
			self.file = open(title + '.txt',"w+")
		else:
			self.file = open(self.defaultTitle + '.txt',"w+")

	def writeData(self,contents):
		for item in contents:
			if self.floorTag == '1':
				floorLine = '\n' + str(self.floor) + u'-------------------------------\n'
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def  start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle()
		self.setFileTitle(title)
		if pageNum == None:
			print u'URL失效'
			return
		try:
			print u"该帖子共有" + str(pageNum) + u"页"
			for i in range(1,int(pageNum) + 1):
				print u"正在写入第" + str(i) + u"页数据"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError,e:
			print u"写入异常，原因" + e.message
		finally:
			print u"写入任务完成"


print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n".decode('utf-8').encode('gbk'))
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n".decode('utf-8').encode('gbk'))
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()

