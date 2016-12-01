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
import urllib
import os

class WeiboList(object):
	"""docstring for WeiboList"""
	def __init__(self, arg):
		super(WeiboList, self).__init__()
		self.arg = arg
		doc = self.arg["doc"]
		for item in self.arg["list"]:
			doc = PQ(PQ(item).html())
			for img in doc("img"):
				url = doc(img).attr("src")
				self.save_img(url)


	def save_img(slef,url):
		pic_name = os.path.basename(url) #delete path, get the filename
		print pic_name
		urllib.urlretrieve(url,"F:\\weibo\\" + pic_name)
