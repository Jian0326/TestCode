#-*-coding:utf-8-*- 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,InvalidElementStateException,WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as PQ
from lxml import etree
import selenium.webdriver.support.ui as UI
import time
from weiboList import WeiboList

class WeiBo(object):
	"""docstring for WeiBo"""
	def __init__(self, arg):
		super(WeiBo, self).__init__()
		self.arg = arg

	def start(self):
		self.input()
		self.driver = webdriver.Chrome()
		# self.driver.set_window_size(1440, 900)
		print u'正在加载网页请稍等片刻!'
		try:
			self.driver.get("http://weibo.com/")
		except Exception, e:
			self.driver.save_screenshot("screenshot.png")
		
		try:
			print self.driver.current_url
			time.sleep(1)
			self.sendAccountAndPassword()
		except NoSuchElementException,e:
			print u"无法获取element控件",e
			
	def getElement(self,elementType,name):
		element = WebDriverWait(self.driver, 0).until(EC.visibility_of_element_located((elementType, name)))
		return element

	def sendAccountAndPassword(self):
		elementAccount = self.getElement(By.ID, "loginname")
		elementPassword = self.getElement(By.NAME,"password")
		elementAccount.clear()
		elementPassword.clear()
		time.sleep(0.2)
		elementAccount.send_keys(self.account)
		elementPassword.send_keys(self.password)
		self.submit()

	def submit(self):
		print u"正在提交信息"
		btn = self.getElement(By.XPATH,"//a[@tabindex='6']")
		if btn.is_displayed() == False:
			self.driver.execute_script('arguments[0].visibility="visible"',btn)
		btn.click()
		print u"提交成功,开始验证账号密码,如果出现验证码无法解释"
		time.sleep(1) #--延时两秒再判断
		try:
			self.driver.find_element(By.XPATH,"//div[@class='W_layer W_layer_pop']")
			print u"密码错误"
			self.input()
			self.sendAccountAndPassword()
		except NoSuchElementException, e:
			print u"查找不到错误信息说明已经ok"
			print u"登陆成功,开始获取微博",self.driver.current_url
			for i in range(1,4):
				js = "window.scrollTo(0,document.body.scrollHeight)"
				self.driver.execute_script(js)
				time.sleep(1)
			self.pageSource(self.driver.page_source)
		
	def input(self):
		self.account = raw_input('请输入微博账号:\n'.decode('utf-8').encode('gbk')).strip()
		self.password = raw_input('请输入微博密码:\n'.decode('utf-8').encode('gbk')).strip()

	def pageSource(self,html):
		doc = PQ(html)
		list = []
		items = doc("div")
		for item in items:
			if doc(item).attr("action-type") == "feed_list_item" :
				list.append(item)
		self.weiboList = WeiboList({"list":list,"doc":doc})
		print len(items),len(list)
	
weibo = WeiBo({})
weibo.start()
