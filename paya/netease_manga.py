import json
import os, sys
import re
import threading
import time
from urllib import request, error
# sys.path.append("..")

import basedler
from const import *

# multiprocessing.Queue
# import iMyUtil

already_tenma_file = "already_tenma_json.txt"
log_tenma_file = "tenma_log_json.txt"
already_tenma = set()
local_tenma = "天才麻将少女_本篇_json/"
num_of_threads = 4


def tema(ep_url, folder_name):
	# 此处 addtoalready 是加入图片，编号为 #folder_name_#图片编号
	
	# if True:
	# 	print(folder_name, ep_url)
	# 	res=request.urlopen("https://manhua.163.com/")
	# 	print(res.read().decode("utf8")[:19].encode("utf8"))
	# 	return
	
	createFolder(folder_name)
	# page_rq = request.Request("https://manhua.163.com/reader/4458002705630123103/")
	page_rq = request.Request(ep_url)
	response = request.urlopen(page_rq)
	str_con = response.read().decode("utf8")
	patt = re.compile(r"url: window.IS_SUPPORT_WEBP ?.*,?")
	pics_raw = patt.findall(str_con)
	num = 0
	for pics in pics_raw:
		num += 1
		url = pics.split(": ")[2]  # 得到地址（分隔后最后一个）
		url = url[1:len(url) - 2]  # 得到地址（拿来用）
		file_name = folder_name + '{:0>3}'.format(str(num)) + ".png"
		if file_name in already_tenma:
			# record_log(log_tenma_file, file_name, "已下载")
			continue
		try:
			rq = request.Request(url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
			rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
			response = request.urlopen(rq, timeout=3000)
			with open(file_name, "wb") as pic:
				pic.write(response.read())
				addToAlready(file_name, already_tenma, already_tenma_file)
		except Exception as e:
			record_log(log_tenma_file, "This Folder: ", folder_name, " Time out, pic: ", num, " , URL: ", url)
			record_log(log_tenma_file, e)
	record_log(log_tenma_file, folder_name, "下载完成")


# threading.current_thread().join()

def TEMA():
	# Deprecated: Using episode urls saved locally
	eps = []
	with open("tenma_downloadMenu.txt", "r") as f:
		for line in f.read().splitlines():
			eps.append(line)
	eps.reverse()
	num_of_ep = 0
	for ep in eps:
		num_of_ep += 1
		ep_folder_name = local_tenma + '{:0>4}'.format(str(num_of_ep)) + '/'  # 格式化文件夹名字，用0补全前面
		# print(ep,ep_folder_name)
		tema(ep, ep_folder_name)


def try_getJson():
	# threads = [threading.Thread() for i in range(num_of_threads)]
	#
	# # using_set=set()
	# # unused_set = set([th for th in threads])
	#
	# def getThreadUnused():
	# 	print("alive? ",[th.is_alive() for th in threads])
	# 	for th in threads:
	# 		if not th.is_alive():
	# 			return th
	# 	return None
	# for th in threads:
	# 	th.start()
	
	json_url = "https://manhua.163.com/book/catalog/4458002705630123103.json"
	rq = request.Request(json_url)
	response = request.urlopen(rq)
	menu_js = response.read().decode("utf8")
	js = json.loads(menu_js)
	print(type(js["catalog"]["sections"][0]["sections"][0]))
	print(len(js["catalog"]["sections"][0]["sections"]))
	num_of_ep = 0
	for each in js["catalog"]["sections"][0]["sections"]:
		num_of_ep += 1
		# if(num_of_ep>5):
		# 	print("say ggooooooddbyeee")
		# 	break
		bookId = each["bookId"]
		pages = each["wordCount"]
		sectionId = each["sectionId"]
		fullTitle = each["fullTitle"]
		url_one_wa = "https://manhua.163.com/reader/" + bookId + "/" + sectionId + "/"
		ep_folder_name = local_tenma + '{:0>4}'.format(str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
		tema(url_one_wa, ep_folder_name)
	# print(ep_folder_name)
	# print(len(unused_set))
	# 	try:
	# 		# next_thread = unused_set.pop()
	# 		next_thread = getThreadUnused()
	# 		print(next_thread.name)
	#
	# 		next_thread._target = tema
	# 		next_thread._args = (url_one_wa, ep_folder_name)
	# 		next_thread._kwargs=dict()
	# 		record_log("开始下载", ep_folder_name)
	# 		next_thread.run()
	# 		# next_thread.join()
	# 	# unused_set.add(next_thread)
	# 	except KeyError as k:
	# 		# 所有线程都在运行
	# 		print("火鹤")
	#
	# 		# for th in threads:
	# 		# 	th.join()
	# 		# unused_set = set([th for th in threads])
	#
	# print(threading.enumerate())


# ================================================================================





# for each in js["catalog"]["sections"][0]["sections"]:
# 	num_of_ep += 1
# 	if num_of_ep == 2:
# 		return
# 	bookId = each["bookId"]
# 	pages = each["wordCount"]
# 	sectionId = each["sectionId"]
# 	fullTitle = each["fullTitle"]
# 	url_one_wa = "https://manhua.163.com/reader/" + bookId + "/" + sectionId + "/"
# 	ep_folder_name = dl_dir + bookname + "/" + '{:0>4}'.format(
# 		str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
# 	print(url_one_wa)
# ep_dl_with_pool(pages, url_one_wa, ep_folder_name)
class DLer(basedler.BaseDLer):
	# 初始化静态成员：网易地址
	
	main_site = "https://manhua.163.com/"
	book_page = "source/"
	json_page = "book/catalog/"
	log_book_file = log_dir + "book_log.txt"
	
	# 一个漫画对应一个
	def __init__(self, bookid):
		basedler.BaseDLer.__init__(self)
		self.bookid = bookid  # str
		self.bookname = safe_file_name(DLer.getBookName(self.bookid))
		if self.bookname == None:  # 现在还没有本地书库
			record_log(DLer.log_book_file, "未能找到书本", ID_163, self.bookid)
			self.can_dl = False
			return
		
		self.dl_path = dl_dir + self.bookname + ID_163 + "/"
		
		self.already_pic_file_name = self.dl_path + already_pic_file  # 天才麻将少女/_163_already_pic.txt
		initializeAlready(self.already_pic_set, self.already_pic_file_name)
		
		self.already_ep_file_name = self.dl_path + already_ep_file
		initializeAlready(self.already_ep_set, self.already_ep_file_name)
		
		self.log_file_name = dl_log_dir + self.bookname + ID_163 + log_file  # log/天才麻将少女_163_log.txt
		createFile(self.log_file_name)
		self.to_dl_list = set()  # 待下载话，为以后选择话数下载准备
		
		self.zip = True
	
	def getBookName(content):  # static method
		# content => bookId
		book_url = DLer.main_site + DLer.book_page + content
		try:
			response = request.urlopen(book_url)
			webpage = response.read().decode("utf8")  # 也许人家不是utf8
			# 如果人家换了呢
			patt = re.compile(r'book-title=".*" h5Domain')
			bookname = patt.findall(webpage)
			# print(bookname)
			if not bookname:
				# 空list，说明这个页面不存在漫画，也就是id给错了
				record_log(DLer.log_book_file, "书本ID错啦，不存在。")
				return None
			bookname = bookname[0]
			bookname = bookname.replace('book-title="', '').replace('" h5Domain', '')
			return bookname
		except error.URLError:
			record_log(DLer.log_book_file, "获取超时，重试看看！~？")
			return None
	
	# def dl_pic(self, pic_url, file_name):
	# 	# Return True: Successfully , False otherwise
	# 	dl_times = 0
	# 	while dl_times < self.MAX_DL_TIMES:
	# 		dl_times += 1
	# 		rq = request.Request(pic_url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
	# 		# rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
	# 		try:
	# 			response = request.urlopen(rq, timeout=3000)
	# 			with open(file_name, "wb") as pic:
	# 				pic.write(response.read())
	# 				addToAlready(file_name, self.already_pic_set, self.already_pic_file_name)
	# 		except error.URLError as t:
	# 			record_log(self.log_file_name, "下载", file_name, "超时", dl_times, "times")
	# 		except Exception as e:
	# 			record_log(self.log_file_name, "其他错误", e)
	# 		else:
	# 			return True
	# 	# record_log(self.log_file_name, "Shippai This Folder:", folder_name, ", pic No:", num, " , URL: ", url)
	# 	return False
	
	def dl_ep(self, pages, ep_url, folder_name):
		""":returns 1 stands for no err, 0 stands for error occurrence"""
		record_log(self.log_file_name, "开始下载", folder_name, "共", pages, "页")
		# p = Pool(pages)
		createFolder(folder_name, self.log_file_name)
		page_rq = request.Request(ep_url)
		response = request.urlopen(page_rq)
		str_con = response.read().decode("utf8")
		patt = re.compile(r"url: window.IS_SUPPORT_WEBP ?.*,?")
		pics_raw = patt.findall(str_con)
		num = 0
		shippai = 0
		for pics in pics_raw:
			num += 1
			url = pics.split(": ")[2]  # 得到地址（分隔后最后一个）
			url = url[1:len(url) - 2]  # 得到地址（拿来用）
			file_name = folder_name + '{:0>3}'.format(str(num)) + ".jpg"  # 还是说其他格式？
			
			# 应是jpg，因为有jfif的前缀
			
			if file_name in self.already_pic_set:
				record_log(self.log_file_name, file_name, "已下载")
				continue
			isDLed = self.dl_pic(url, file_name)
			# result = p.apply_async(pic_dl_with_pool, args=(url, file_name))
			# isDLed = result.get() # 直接获取返回值，去你大爷的callback
			# record_log(self.log_file_name,"isDLed",isDLed)
			
			# if isDLed:
			# record_log(self.log_file_name, "图片下载成功", file_name)
			if not isDLed:
				shippai += 1
				record_log(self.log_file_name, "Shippai This Folder:", folder_name, ", pic No:", num, " , URL: ", url)
		if not shippai:
			addToAlready(folder_name, self.already_ep_set, self.already_ep_file_name)
			return 1
		else:
			return 0
		# p.close()
		# p.join()
	
	def dl_whole_book(self):
		json_url = "https://manhua.163.com/book/catalog/" + self.bookid + ".json"
		rq = request.Request(json_url)
		response = request.urlopen(rq)
		menu_js = response.read().decode("utf8")
		js = json.loads(menu_js)
		# print(type(js["catalog"]["sections"][0]["sections"][0]))
		# print(len(js["catalog"]["sections"][1]["sections"]))
		num_of_chap = 0
		chapters = js["catalog"]["sections"]
		for chapter in chapters:
			# chapter 是一个json，dict。 有 16 个key
			num_of_chap += 1
			# 多个篇章的文件夹分开装
			chaptername = safe_file_name(chapter["fullTitle"])
			# 如果只有一个chapter，就不分开
			if len(chapters) == 1:
				chap_foldername = self.dl_path
			else:
				chap_foldername = self.dl_path + '{:0>2}'.format(
					str(num_of_chap)) + "_" + chaptername + '/'  # 格式化文件夹名字，用0补全前面
			# print(len(chapter)) # 因为这个是dict，所以len就是 16（dict里元素个数）
			# print( chapter )
			record_log(self.log_file_name, "开始下载篇章", chap_foldername)
			
			num_of_ep = 0
			for subsection in chapter["sections"]:
				ep_dl_count = 0
				num_of_ep += 1
				bookId = subsection["bookId"]
				pages = subsection["wordCount"]
				sectionId = subsection["sectionId"]
				fullTitle = safe_file_name(subsection["fullTitle"])
				url_one_wa = "https://manhua.163.com/reader/" + bookId + "/" + sectionId + "/"
				ep_folder_name = chap_foldername + '{:0>4}'.format(
					str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
				# print(ep_folder_name,url_one_wa)
				if ep_folder_name in self.already_ep_set:
					record_log(self.log_file_name, ep_folder_name, "已下载")
					continue
				dl_succeeded = 0
				while ep_dl_count < basedler.BaseDLer.MAX_EP_TIMES and not dl_succeeded:
					ep_dl_count += 1
					if (ep_dl_count > 1):
						record_log(self.log_file_name,"重试",ep_folder_name,"第",ep_dl_count,"次")
					# if not succeed dling this ep, retry
					dl_succeeded = self.dl_ep(pages, url_one_wa, ep_folder_name)
