import json
import os
import re
import threading
import time
from urllib import request, error
from paya import basedler
from paya.const import *


class ikanman_DLer(basedler.BaseDLer):
	main_site = "http://www.ikanman.com/"
	book_page = "comic/"
	log_book_file = main_log_dir + "book_log.txt"

	def __init__(self, bookid):
		basedler.BaseDLer.__init__(self)
		self.bookid = bookid  # str
		self.bookname = ikanman_DLer.getBookName(self.bookid)
		if self.bookname == None:  # 现在还没有本地书库
			record_log(ikanman_DLer.log_book_file, "未能找到书本", ID_ikm, self.bookid)
			self.can_dl = False
			return
		self.dl_path = dl_dir + self.bookname + ID_ikm + "/"

		self.already_pic_file_name = self.dl_path + main_already_pic_file  # 天才麻将少女/_163_already_pic.txt
		initializeAlready(self.already_pic_set, self.already_pic_file_name)

		self.already_ep_file_name = self.dl_path + main_already_ep_file
		initializeAlready(self.already_ep_set, self.already_ep_file_name)

		self.log_file_name = dl_log_dir + self.bookname + ID_ikm + main_log_file  # log/天才麻将少女_163_log.txt
		createFile(self.log_file_name)
		self.to_dl_list = set()  # 待下载话，为以后选择话数下载准备

	def getBookName(content):  # static method
		# content => bookId

		book_url = ikanman_DLer.main_site + ikanman_DLer.book_page + content
		try:
			response = request.urlopen(book_url)
			webpage = response.read().decode("utf8")  # 也许人家不是utf8
			# 如果人家换了呢
			# patt = re.compile(r'<div class="book-title">.*(</div>)*?')
			patt = re.compile(r'<div class="book-title">.*<ul class="detail-list cf">')
			bookname = patt.findall(webpage)
			# print(bookname)
			if not bookname:
				# 空list，说明这个页面不存在漫画，也就是id给错了
				record_log(ikanman_DLer.log_book_file, "书本ID", content, "错啦，不存在。")
				return None
			bookname = bookname[0]
			end = bookname.find('</h1')
			start = bookname.find('<h1>')
			bookname = bookname[start + 4:end]
			# print(bookname)
			return bookname
		except error.URLError:
			record_log(ikanman_DLer.log_book_file, "获取", content, "超时，重试看看！~？")
			return None

	def dl_ep(self, pages, ep_url, folder_name):

		script_symbol = "eval(decryptDES"

		record_log(self.log_file_name, "开始下载", folder_name, "共", pages, "页")
		# p = Pool(pages)
		createFolder(folder_name, self.log_file_name)
		page_rq = request.Request(ep_url)
		response = request.urlopen(page_rq)
		str_con = response.read().decode("utf8")
		from bs4 import BeautifulSoup

		soup = BeautifulSoup(str_con, "html.parser")
		scripts = soup.find_all("script")  # body里的第一个script就是要的js们
		script = None
		# print(scripts)
		for s in scripts:
			# print(type(s.string))
			if s.string:  # Not None
				st = str(s.string)
				if script_symbol in st:
					script = st
					break
		script = script[5:-2]  # 去掉eval( 和 );
		# print(script)
		# 总之已经获取到加密后的JS了。 其实可以直接第五个？
		# 假定现在已经获取了解密后的    ========= 已经获取了！！！！！！！！！！！！！！
		# 如果可以，还是加载页面上的比较好
		with open("ikm_Kai_mitsu.js", "rb") as f:
			kaimitsu_js = f.read().decode("utf8")
		import js2py

		decrypt_result = js2py.eval_js(js_lib_by_py + kaimitsu_js + script)
		# print(type(decrypt_result)) # <class 'str'>
		print("decrypt_result",decrypt_result)
		# 应该在这里就修正decrypt_result 应该是，EX ASCII的
		true_list = [ord(c) for c in decrypt_result]
		# print("real encode", bytes(true_list))
		true_result = bytes(true_list).decode("utf8")
		print("true result",true_result)
		eval_result = js2py.eval_js(true_result)

		print(type(eval_result))  # <class 'js2py.base.JsObjectWrapper'>
		print("eval_result", eval_result)
		# Plaintext = str(eval_result)
		# b = bytes(Plaintext.encode("utf8"))
		# print(b)
		# wrong_bytes_decimal = list(b)
		# wrong_bytes_decimal.remove(92)
		# print("list version ", wrong_bytes_decimal)
		# right_slash_num = wrong_bytes_decimal.count(92)
		# while right_slash_num > 0:
		# 	pos_92 = wrong_bytes_decimal.index(92)
		# 	f1 = wrong_bytes_decimal[pos_92 + 2]
		# 	f2 = wrong_bytes_decimal[pos_92 + 3]
		# 	hexa = chr(f1) + chr(f2)
		# 	real = hex2dec(hexa)
		# 	wrong_bytes_decimal = wrong_bytes_decimal[:pos_92] + [real] + wrong_bytes_decimal[pos_92 + 4:]
		# 	right_slash_num -= 1
		# print("after ")
		# print("no92", str(bytes(wrong_bytes_decimal).decode("utf8")))
		di = js2py.eval_js(eval_result).list()

	# for it in di["files"]:
	# 	print(it)
	# patt = re.compile(r"url: window.IS_SUPPORT_WEBP ?.*,?")
	# pics_raw = patt.findall(str_con)
	# num = 0
	# shippai = 0
	# for pics in pics_raw:
	# 	num += 1
	# 	url = pics.split(": ")[2]  # 得到地址（分隔后最后一个）
	# 	url = url[1:len(url) - 2]  # 得到地址（拿来用）
	# 	file_name = folder_name + '{:0>3}'.format(str(num)) + ".png"  # 还是说其他格式？
	# 	if file_name in self.already_pic_set:
	# 		record_log(self.log_file_name, file_name, "已下载")
	# 		continue
	# 	isDLed = self.dl_pic(url, file_name)
	# 	# result = p.apply_async(pic_dl_with_pool, args=(url, file_name))
	# 	# isDLed = result.get() # 直接获取返回值，去你大爷的callback
	# 	# record_log(self.log_file_name,"isDLed",isDLed)
	#
	# 	# if isDLed:
	# 	# record_log(self.log_file_name, "图片下载成功", file_name)
	# 	if not isDLed:
	# 		shippai += 1
	# 		record_log(self.log_file_name, "Shippai This Folder:", folder_name, ", pic No:", num, " , URL: ", url)
	# # p.close()
	# # p.join()
	# if not shippai:
	# 	record_log(self.log_file_name, folder_name, "下载完成")
	# 	addToAlready(folder_name, self.already_ep_set, self.already_ep_file_name)
	# else:
	# 	record_log(self.log_file_name, folder_name, shippai, "张图片挂了")

	def dl_whole_book(self):
		# 怎么样只用response一次？getBookname里面也有一次。 或者存下来，之后删掉。
		book_url = ikanman_DLer.main_site + ikanman_DLer.book_page + self.bookid + "/"
		# book_url = "file:///C:/Users/%E5%BD%B1%E9%A3%8E%E7%A7%A6/Desktop/%E7%A5%9E%E5%A5%87%E5%AE%9D%E8%B4%9D%E7%89%B9%E5%88%AB%E7%AF%87%E6%BC%AB%E7%94%BB%E6%9C%AA%E4%BF%AE%E6%94%B9.html"
		# book_url = "file:///C:/Users/%E5%BD%B1%E9%A3%8E%E7%A7%A6/Desktop/%E7%A5%9E%E5%A5%87%E5%AE%9D%E8%B4%9D%E7%89%B9%E5%88%AB%E7%AF%87%E6%BC%AB%E7%94%BB_.html"
		# print(book_url)
		rq = request.Request(book_url)
		response = request.urlopen(rq)
		str_con = response.read().decode("utf8")
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(str_con, "html.parser")

		first_chap = soup.h4
		# print(first_chap)
		h4_and_div = [first_chap] + [tag for tag in first_chap.next_siblings]
		chapters = []
		divs = []
		for block in h4_and_div:
			# print(type(block.name))
			if block.name == "h4":
				chapter_name = block.contents[0].contents[0]
				chapter_name = str(chapter_name)
				chapters.append(chapter_name)
			elif block.name == "div":
				class_con = block["class"]
				if "chapter-list" in class_con:
					divs.append(block)  # 应该不会有一个chapter对应多个的list的吧 = =
		# print(chapters) # str
		# print(divs) # divs
		num_of_chap = 0
		chapters.reverse()
		divs.reverse()  # 他是从新到旧，但我编号要从旧到新
		#
		for i, div in enumerate(divs):
			num_of_chap += 1
			chaptername = chapters[i]

			if len(chapters) == 1:
				chap_foldername = self.dl_path
			else:
				chap_foldername = self.dl_path + '{:0>2}'.format(
					str(num_of_chap)) + "_" + chaptername + '/'  # 格式化文件夹名字，用0补全前面

			# eps = []
			uls = div.contents  # uls的顺序正确，内部顺序反过来
			num_of_ep = 0
			for ul in uls:
				lis = ul.contents
				lis.reverse()
				for li in lis:  # 这就是真的每一话了，需要 href=对应每一话地址 title名字 i 数量
					# ========= 获取每一话的对应信息 ===========
					num_of_ep += 1
					if num_of_ep > 1:
						break
					a = li.a

					ep_url = ikanman_DLer.main_site + a["href"]  # a[href]是/comic/6540/163709.html
					i_con = li.i.contents  # NaviString
					pages = str(i_con[0])[:-1]
					pages = int(pages)
					fullTitle = a["title"]
					ep_folder_name = chap_foldername + '{:0>4}'.format(
						str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
					print(ep_folder_name, ep_url)

					self.dl_ep(pages, ep_url, ep_folder_name)
				# print(a["href"])
				# print(type(a["href"]))
				# print(pages)

				# eps += lis
				# chapter_lis.append(eps

				# chapters = soup.find_all("h4") # <class 'bs4.element.ResultSet'>
				# chapters.reverse for c in chapters:
				# 	# 全部的chapter信息 每一个的都是 <class 'bs4.element.Tag'>
				# 	#形式为 <h4><span>单话</span></h4>
				# 	chapter_name = c.contents[0].contents[0] # 得到 单话 <class 'bs4.element.NavigableString'>
				# 	chapter_name = str(chapter_name)
				# 	print(str(chapter_name))
				# chapters = [str(c.contents[0].contents[0]) for c in chapters]
				# # 每一话h4的下一个兄弟是一个div，这个div里面只有一个元素ul【第一个contents】
				# # xxx 可以多个ul，他一一页装不下太多了，所以翻了页。解析就for的时候reverse他。
				# # ul里面每一个li【第二个contents】就是每一话



				# for chapter in chapters:
				# 	# chapter 是一个json，dict。 有 16 个key
				# 	num_of_chap += 1
				# 	# 多个篇章的文件夹分开装
				# 	chaptername = chapter["fullTitle"]
				# 	# 如果只有一个chapter，就不分开
				# 	if len(chapters) == 1:
				# 		chap_foldername = self.dl_path
				# 	else:
				# 		chap_foldername = self.dl_path + '{:0>2}'.format(
				# 			str(num_of_chap)) + "_" + chaptername + '/'  # 格式化文件夹名字，用0补全前面
				# 	# print(len(chapter)) # 因为这个是dict，所以len就是 16（dict里元素个数）
				# 	# print( chapter )
				# 	record_log(self.log_file_name, "开始下载篇章", chap_foldername)
				#
				# 	num_of_ep = 0
				# 	for subsection in chapter["sections"]:
				# 		num_of_ep += 1
				# 		# if num_of_ep == 2:
				# 		# 	return
				# 		bookId = subsection["bookId"]
				# 		pages = subsection["wordCount"]
				# 		sectionId = subsection["sectionId"]
				# 		fullTitle = subsection["fullTitle"]
				# 		url_one_wa = "https://manhua.163.com/reader/" + bookId + "/" + sectionId + "/"
				# 		ep_folder_name = chap_foldername + '{:0>4}'.format(
				# 			str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
				# 		# print(ep_folder_name,url_one_wa)
				# 		if ep_folder_name in self.already_ep_set:
				# 			record_log(self.log_file_name, ep_folder_name, "已下载")
				# 			continue
				# 		self.dl_ep(pages, url_one_wa, ep_folder_name)
