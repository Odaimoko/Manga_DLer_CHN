# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
import threading
import time
from urllib import request, error, parse
import paya.basedler as basedler
from paya.const import *
import js2py


class DLer(basedler.BaseDLer):
	main_site = "http://www.ikanman.com"
	book_page = "/comic/"
	dl_site = ["http://i.hamreus.com:8080", "http://p.yogajx.com",
	           "http://cf.hamreus.com:8080", "http://idx0.hamreus.com:8080"]  # 下载地址path自带/
	# 它的图床还有可能不一样= =估计是到了比较新的漫画（或者比较新的章节）
	# 自动/ / 电信/连通/


	log_book_file = log_dir + "book_log.txt"

	def __init__(self, bookid):
		basedler.BaseDLer.__init__(self)
		self.bookid = bookid  # str
		self.bookname = DLer.getBookName(self.bookid)
		if self.bookname is None:  # 现在还没有本地书库
			record_log(DLer.log_book_file, "未能找到书本", ID_ikm, self.bookid)
			self.can_dl = False
			return
		self.dl_path = dl_dir + self.bookname + ID_ikm + "/"

		self.already_pic_file_name = self.dl_path + already_pic_file  # 天才麻将少女/_163_already_pic.txt
		initializeAlready(self.already_pic_set, self.already_pic_file_name)

		self.already_ep_file_name = self.dl_path + already_ep_file
		initializeAlready(self.already_ep_set, self.already_ep_file_name)

		self.log_file_name = dl_log_dir + self.bookname + ID_ikm + log_file  # log/天才麻将少女_163_log.txt
		createFile(self.log_file_name)

		self.mikanse_file_name = self.dl_path + shippai_file
		exist_mikanse = os.path.exists(self.mikanse_file_name)
		if not exist_mikanse:
			createFile(self.mikanse_file_name, initial="{}")
		with open(self.mikanse_file_name, "r") as f:
			self.mikanse = json.load(f)
		print(type(self.mikanse))

		self.to_dl_list = set()  # 待下载话，为以后选择话数下载准备

		self.zip = True

		self.record(self.bookname, ID_ikm, "初始化成功")

	def getBookName(content):  # static method
		# content => bookId

		book_url = DLer.main_site + DLer.book_page + content
		webpage = ""
		try:
			response = request.urlopen(book_url)
			webpage = response.read().decode("utf8")  # 也许人家不是utf8
		except error.URLError:
			record_log(DLer.log_book_file, "获取", content, "超时，重试看看！~？")
			return None

		# 如果人家换了呢
		patt = re.compile(r'<div class="book-title">.*<ul class="detail-list cf">')
		bookname = patt.findall(webpage)
		# print(bookname)
		if not bookname:
			# 空list，说明这个页面不存在漫画，也就是id给错了
			record_log(DLer.log_book_file, "书本ID", content, "错啦，不存在。")
			return None
		bookname = bookname[0]
		end = bookname.find('</h1')
		start = bookname.find('<h1>')
		bookname = bookname[start + 4:end]
		# print(bookname)
		return bookname

	def dl_ep(self, pages, ep_url, folder_name):
		# folder_name是这一章的目录
		# script_symbol = "eval(decryptDES"
		script_symbol = "function(p,a,c,k,e,d)" # 这个应该永远不出= =
		from multiprocessing.pool import Pool
		import multiprocessing
		record_log(self.log_file_name, "开始下载", folder_name, "共", pages, "页")
		p = Pool(multiprocessing.cpu_count())
		createFolder(folder_name, self.log_file_name)
		page_rq = request.Request(ep_url)
		start = time.clock()
		response = request.urlopen(page_rq)
		end = time.clock()
		self.record("读取一话页面耗时", end - start, "s")
		str_con = response.read().decode("utf8")
		# str_con="""
# <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml"><head><title>恋爱足球my ball第01回_恋爱足球my ball漫画 - 看漫画</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta name="keywords" content="第01回,恋爱足球my ball,いのうえ空,漫画,看漫画" /><meta name="Description" content="恋爱足球my ball第01回,在线看恋爱足球my ball漫画就在看漫画" /><link rel="stylesheet" type="text/css" href="http://c.3qfm.com/css/detail_07A954DB218D118BF76A193BC9849504.css" /><script type="text/javascript" src="http://c.3qfm.com/scripts/config_25855B4C08F7A6545A30D049ABD0F9EE.js"></script><!--[if IE 6]><script type="text/javascript">document.execCommand("BackgroundImageCache", false, true);</script><![endif]--></head><body><div class="header"><div class="header-inner"><div class="w980"><div class="search fr pr"><input id="txtKey" value="" /><button id="btnSend">搜索</button><div id="sList" class="sList shadow"></div></div><span class="nav"><a href="/" title="返回首页" class="logo"></a><a href="/update/" class="pr new-update">最新更新<i></i></a><a href="/list/">漫画大全</a><a href="/list/wanjie/">完结</a><a href="/list/lianzai/">连载</a><a href="/rank/">排行榜</a><a href="/list/japan/">日本漫画</a></span><span class="more pr" id="nav-sec"><strong>更多类别</strong><i></i><div class="content shadow nav-sec"></div></span><span class="more pr" id="history"><strong>我的浏览记录</strong><i></i><div class="content shadow" id="hList"><span class="hNone">loading...</span></div></span><span class="menu-end"></span></div></div></div><div class="gg_950"><script type="text/javascript"> document.write('<a style="display:none!important" id="tanx-a-mm_27549993_4204197_26768731"></a>'); tanx_s = document.createElement("script"); tanx_s.type = "text/javascript"; tanx_s.charset = "gbk"; tanx_s.id = "tanx-s-mm_27549993_4204197_26768731"; tanx_s.async = true; tanx_s.src = "http://p.tanx.com/ex?i=mm_27549993_4204197_26768731"; tanx_h = document.getElementsByTagName("head")[0]; if(tanx_h)tanx_h.insertBefore(tanx_s,tanx_h.firstChild); </script></div><div class="w980 title"><div class="fr"><span class="lighter-close" id="lighter">关灯</span></div><div><h1><a href="/comic/18557/">恋爱足球my ball</a></h1><em>/</em><h2>第01回</h2><em>/</em><span>(<span id="page"></span>/32)</span></div></div><div class="w980 tc"><div class="main-btn"><a href="#" id="viewList" class="btn-red">目录列表</a><a href="#" class="btn-red prevC">上一章</a><a href="javascript:void(0);" id="prev" class="btn-red">上一页</a><select id="pageSelect"></select><a href="javascript:void(0);" id="next" class="btn-red">下一页</a><a href="#" class="btn-red nextC">下一章</a><a href="/comic/18557/#SOHUCS" class="btn-red" target="_blank">我要评论</a></div></div><div class="w980 clearfix sub-btn"><div class="servList fr" id="servList"><ul><li><a href="javascript:;">线路→</a></li></ul></div><div class="fl support"><ul><li class="pr" id="shortcuts"><a href="javascript:;" class="support-shortcuts">快捷键</a></li><li class="pr" id="qrcodes"><a href="javascript:;" id="tool-qr" class="qrcode">二维码</a></li><li><a href="javascript:;" id="tool-speed" class="speed">极速</a></li><li class="pr" id="zoomtool"><a href="javascript:;" id="tool-zoom" class="zoomin">缩放</a></li><li><a href="javascript:;" id="tool-rotate" class="rotate">旋转</a></li><li><a href="javascript:;" id="tool-crop" class="crop">裁切</a></li><li><a href="javascript:;" id="tool-gray" class="gray">滤镜</a></li><li><a href="javascript:;" id="support-error" class="error">报错</a></li><li><span class="pr arrow shareto">翻页→</span></li></ul></div><div class="fl pfList" id="share"></div></div><div class="clearfix"><table border="0" cellspacing="0" cellpadding="0" class="pr tbCenter cb"><tr><td align="center" id="tbBox"><div class="img-loading" id="imgLoading"><i></i><span>图片努力加载中，请稍候</span></div><div align="center" id="mangaBox"></div><div id="imgPreLoad"></div></td></tr></table></div><script type="text/javascript">window["\x65\x76\x61\x6c"](function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('R o={"p":4,"q":"n j","k":"4.2","m":r,"w":"x","y":["v.2.3","s.2.3","t.2.3","u.2.3","9.2.3","a.2.3","7.2.3","6.2.3","5.2.3","b.2.3","g.2.3","h.2.3","i.2.3","f.2.3","c.2.3","d.2.3","e.2.3","8.2.3","I.2.3","S.2.3","T.2.3","Q.2.3","N.2.3","O.2.3","P.2.3","U.2.3","10.2.3","Y.2.3","Z.2.3","W.2.3","X.2.3","V.2.3"],"D":E,"F":C,"z":"/A/l/B/K/","L":1,"M":"","J":G,"H":0}||{};',62,63,'D7BWAcHNgdwUwEbmARgBwFYMHZgE4B9AZmwz2DQIBYAmI87AnANjVUudauAyaJubBmBGnmwpUABgLY0ecil4Yqk3CmHMqeDKkYo8RbiipNlbFChmSMRVDWp4qOlEQKZVwBAEMANj8/gAJYAxiDBgQAmwIDSBoCMToDNsYDALgC2AJ7AwQCSAHYAZgD2npGe2V7JcMA01hho3PZmEq7M2FS4JjStNKgEzHi9GaXlwIA03pIogHtqwLmBPnAAzsDgXgAuABaLc9w+XgBeAI5p3n4EANbA/FOB2YFzq3BRub5zFbPZldWYiwBOcABumVF9DJWJJgNk4AAPZYA4BeYLLAgSObLFYAVwWCB8+WCJwIwVCdAI2kkoI6TFq5BovHoKkq9jwaHEwF+Xi+7z4RB0NEsKEkhkqwlEtXO9hInPO0mMREEREsZCZNEoKGw0sqhCqnxojCIkgZQA='['\x73\x70\x6c\x69\x63']('\x7c'),0,{})) </script><script type="text/javascript" src="http://c.3qfm.com/scripts/core_0BA1BF3DA711E363A46937D8393D038A.js"></script><div class="gg_950" style="margin-bottom:8px"><script type="text/javascript"> document.write('<a style="display:none!important" id="tanx-a-mm_27549993_4204197_58548400"></a>'); tanx_s = document.createElement("script"); tanx_s.type = "text/javascript"; tanx_s.charset = "gbk"; tanx_s.id = "tanx-s-mm_27549993_4204197_58548400"; tanx_s.async = true; tanx_s.src = "http://p.tanx.com/ex?i=mm_27549993_4204197_58548400"; tanx_h = document.getElementsByTagName("head")[0]; if(tanx_h)tanx_h.insertBefore(tanx_s,tanx_h.firstChild); </script></div><div class="gg_950 jghf"><script type="text/javascript" src="http://u.yiiwoo.com/seemh.js"></script></div><div class="w980 tc"><div class="pager" id="pagination"></div></div><div class="gg_950 jghf" style="margin-bottom:8px"><script src='http://121.40.25.88/seemh3.js'></script></div><div class="gg_300" style="margin:0 auto 12px; width:920px"><div class="gg_300 fl jghf" style="margin-right:10px;"><script src='http://121.40.25.88/ik300.js'></script></div><div class="gg_300 fl jghf" style="margin-right:10px;"><script src='http://121.40.25.88/ik3002.js'></script></div><div class="gg_300 fl jghf"><script src='http://121.40.25.88/ik3003.js'></script></div></div><div class="footer"><div class="footer-main"><div class="w980 tc"> 恋爱足球my ball第01回来自网友分享和上传，以便漫画爱好者研究漫画技巧和构图方式，禁止任何形式的下载！若喜欢，请支持购买正版！ <script type="text/javascript" src="http://c.3qfm.com/scripts/footer_2DB6C055C0D0ABD5D8ED8A4EA5ADCE93.js"></script></div></div></div></body></html>"""
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
		script = script[27:-2]  # 去掉eval( 和 );		# 2017-06-08：新的加密手段里，是WINDOW["EVAL"](所以是前面 15个

		patt = re.compile(r'function\(p.*;}\(')
		ma = patt.findall(script)
		script=script.replace(ma[0],"decode_pack(")
		# 情况这样：ikm_kai.JS里是新的解密js，那里定义好的decode_pack 函数，和这里的function(P A C K E D)一样
		#  所以应该去除的是最前面的func部分，换成decode pack

		print()
		# print(script)
		# 总之已经获取到加密后的JS了。 其实可以直接第五个？
		# 假定现在已经获取了解密后的    ========= 已经获取了！！！！！！！！！！！！！！
		# 如果可以，还是加载页面上的比较好 xxxx 如果重新洗一个encodeURIConnection

		kaimitsu_js = js2py.get_file_contents("ikm_kai.js")	# 20170608 他换了一种ikm的加密手段
		start = time.clock()
		decrypt_result = js2py.eval_js(kaimitsu_js + script)
		# print(type(decrypt_result)) # <class 'str'>
		# print("decrypt_result",decrypt_result)
		# 应该在这里就修正decrypt_result EX ASCII的
		result_in_bytes = [c for c in decrypt_result.encode("utf8")] # 把结果转成utf8码，然后化成256以内的bytes（int）的list
		# true_list = [ord(c) for c in decrypt_result] # 这里不好的是，如果有汉字，那么就会ORD(C)就会很大，下面bytes化只能0~255
		# print("real encode", bytes(true_list))
		true_result = bytes(result_in_bytes).decode("utf8")
		# print("true result",true_result)
		eval_result = js2py.eval_js(true_result)
		end = time.clock()
		self.record("JS耗时", end - start, "s")
		# print(type(eval_result))  # <class 'js2py.base.JsObjectWrapper'>

		# di = js2py.eval_js(eval_result)
		#  既然是个js的obj（dict），那么自然也就没有None和False了，eval_result已经是字符串
		# 类似于 {'path': '/ps3/z/镇魂街[许辰]/番外篇1/', 'burl': None, 'finished': False,
		# 'cname': '番外篇1', 'len': 12, 'status': 1, 'bid': 9082, 'bpic': '9082.jpg',
		# 'cid': 90440, 'files': ['001.jpg.webp', '002.jpg.webp'], 'bname': '镇魂街'}
		# 不应再次eval，而应该直接当作dict来直接获取里面的元素
		q = parse.quote
		files = eval_result["files"]
		# print(files) # 一个list(str)
		path = eval_result["path"]
		title = eval_result["bname"]
		subtitle = eval_result["cname"]
		dl_prefix = [dlsite + q(path) for dlsite in DLer.dl_site]
		shippai = 0
		for num, file in enumerate(files):
			num += 1  # won't change num permanently
			print("转换前", file)

			pic_url = [prefix + q(file.replace(".webp", "")).replace("%25", "%") for prefix in dl_prefix]
			# 如果本身有%20这样的空格，会转化成%2520，应该转回来
			#  pic_url = [prefix + q(file.replace(".webp", "")) for prefix in dl_prefix] # 废弃
			# print("转换后", pic_url)

			file_name = folder_name + '{:0>3}'.format(str(num)) + ".jpg"  # 还是说其他格式？ 就是jpg
			if file_name in self.already_pic_set:
				record_log(self.log_file_name, file_name, "已下载")
				continue
			# print(file_name, pic_url)
			# 必须把汉字转成utf8流
			# 其他错误 'ascii' codec can't encode characters in position 31-33: ordinal not in range(128)
			start = time.clock()
			isDLed = self.dl_pic(pic_url, file_name)
			end = time.clock()
			self.record("下载图片耗时", end - start, "s")
			if not isDLed:
				shippai += 1
		if not shippai:
			record_log(self.log_file_name, folder_name, "下载完成")
			if self.zip:
				basedler.BaseDLer.zip_one_ep(folder_name)
			addToAlready(folder_name, self.already_ep_set, self.already_ep_file_name)
		else:
			# 写入文件（重新写一遍）
			with open(self.mikanse_file_name,"w") as f:
				json.dump(self.mikanse,fp=f,indent="\t",sort_keys=True)
			record_log(self.log_file_name, folder_name, shippai, "张图片挂了")


	def dl_whole_book(self):
		record_log(self.log_file_name, "开始下载", self.bookname, ID_ikm)
		# 怎么样只用response一次？getBookname里面也有一次。 或者存下来，之后删掉。
		book_url = DLer.main_site + DLer.book_page + self.bookid + "/"
		# book_url = "file:///C:/Users/%E5%BD%B1%E9%A3%8E%E7%A7%A6/Desktop/%E7%A5%9E%E5%A5%87%E5%AE%9D%E8%B4%9D%E7%89%B9%E5%88%AB%E7%AF%87%E6%BC%AB%E7%94%BB%E6%9C%AA%E4%BF%AE%E6%94%B9.html"
		# book_url = "file:///C:/Users/%E5%BD%B1%E9%A3%8E%E7%A7%A6/Desktop/%E7%A5%9E%E5%A5%87%E5%AE%9D%E8%B4%9D%E7%89%B9%E5%88%AB%E7%AF%87%E6%BC%AB%E7%94%BB_.html"
		# print(book_url)
		rq = request.Request(book_url)
		start = time.clock()
		response = request.urlopen(rq)
		end = time.clock()
		self.record("耗时", end - start, "s")
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
					# if num_of_ep > 1:
					# 	break
					a = li.a

					ep_url = DLer.main_site + a["href"]  # a[href]是/comic/6540/163709.html
					i_con = li.i.contents  # NaviString
					pages = str(i_con[0])[:-1]
					pages = int(pages)
					fullTitle = a["title"]
					pure_folder_name = '{:0>4}'.format(str(num_of_ep)) + " " + fullTitle
					ep_folder_name = chap_foldername + pure_folder_name + '/'  # 格式化文件夹名字，用0补全前面
					# print(ep_folder_name, ep_url)

					if ep_folder_name in self.already_ep_set:
						record_log(self.log_file_name, ep_folder_name, "已下载")
						continue
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
				# self.record(self.mikanse)
