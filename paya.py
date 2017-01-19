from urllib import request, parse, error
import re, json
import sys, time
import threading, multiprocessing
from multiprocessing.pool import Pool

# multiprocessing.Queue
# sys.path.append("..")
# import iMyUtil

dl_dir = ""

already_tenma_file = "already_tenma_json.txt"
log_tenma_file = "tenma_log_json.txt"
already_tenma = set()
local_tenma = "天才麻将少女_本篇_json/"
num_of_threads = 4


def initializeAlready(alreadySet, alreadyFile):
	try:
		with open(alreadyFile, "rb") as f:
			already_text = f.read().decode("utf8")
			for line in already_text.splitlines():
				# 记录全部url，包括http:// 和末尾的/
				alreadySet.add(line)
			del already_text
	except FileNotFoundError as e:
		# 未创建，创啊
		with open(alreadyFile, "w") as f:
			pass


lock_already = threading.Lock()
lock_log_file = threading.Lock()


def addToAlready(content, alreadySet, alreadyFileName):
	if content in alreadySet:
		return
	lock_already.acquire()
	try:
		alreadySet.add(content)
		with open(alreadyFileName, "ab") as al:
			al.write(str(content).encode("utf8"))
			al.write("\n".encode())
	finally:
		lock_already.release()


def record_log(logFileName, *src):
	lock_log_file.acquire()
	try:
		print(*src)
		with open(logFileName, "ab") as lo:
			# 解决直接write出现 encode 错误，还是手动encode+写入二进制
			lo.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).encode())
			lo.write(":".encode())
			for s in src:
				lo.write(" ".encode())
				lo.write(str(s).encode())
			lo.write("\n".encode())
	finally:
		lock_log_file.release()


def createFolder(name):
	import os
	name = name.strip().rstrip("/")
	exist = os.path.exists(name)
	if exist:
		# print(name + " already here.")
		pass
	else:
		os.makedirs(name)
		# print(name + " created.")
		record_log(log_tenma_file, name + " created.")


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



log_book_file = "book_log.txt"


def getBookName(site, content):
	if site == "163":
		# content => bookId
		book_url = "https://manhua.163.com/source/" + content
		try:
			response = request.urlopen(book_url)
			webpage = response.read().decode("utf8")  # 也许人家不是utf8
			# 如果人家换了呢
			patt = re.compile(r'<p class="book-title">.*</p>')
			bookname = patt.findall(webpage)
			bookname = bookname[0]
			bookname = bookname.replace('<p class="book-title">', '').replace('</p>', '')
			return bookname
			print(bookname)
		except error.URLError:
			record_log(log_book_file, "获取超时")
			return None


local_tenma_pool = "天才麻将少女_本篇_pool/"
already_tenma_pool = set()
already_tenma_file_pool = "already_tenma_pool.txt"
log_tenma_file_pool = "tenma_log_pool.txt"
MAX_DL_TIMES = 3


def pic_dl_with_pool(pic_url, file_name):
	# Return True: Successfully , False otherwise
	dl_times = 0
	while dl_times < MAX_DL_TIMES:
		dl_times += 1
		try:
			rq = request.Request(pic_url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
			# rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
			response = request.urlopen(rq, timeout=3000)
			with open(file_name, "wb") as pic:
				pic.write(response.read())
				addToAlready(file_name, already_tenma_pool, already_tenma_file_pool)
		except error.URLError as t:
			record_log(log_tenma_file_pool, "下载", file_name, "超时", dl_times, "times")
		except Exception as e:
			record_log(log_tenma_file_pool, "其他错误", e)
		else:
			return True
	# record_log(log_tenma_file_pool, "Shippai This Folder:", folder_name, ", pic No:", num, " , URL: ", url)
	return False


def ep_dl_with_pool(pages, ep_url, folder_name):
	record_log(log_tenma_file_pool, "开始下载", folder_name,"共", pages, "页")
	# p = Pool(pages)
	createFolder(folder_name)
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
		file_name = folder_name + '{:0>3}'.format(str(num)) + ".png"
		if file_name in already_tenma_pool:
			record_log(log_tenma_file_pool, file_name, "已下载")
			continue
		isDLed = pic_dl_with_pool(url, file_name)
		# result = p.apply_async(pic_dl_with_pool, args=(url, file_name))
		# isDLed = result.get() # 直接获取返回值，去你大爷的callback
		# record_log(log_tenma_file_pool,"isDLed",isDLed)
		if isDLed:
			record_log(log_tenma_file_pool,"图片下载成功",file_name)
		if not isDLed:
			shippai += 1
			record_log(log_tenma_file_pool, "Shippai This Folder:", folder_name, ", pic No:", num, " , URL: ", url)
	# p.close()
	# p.join()
	if not shippai:
		record_log(log_tenma_file_pool, folder_name, "下载完成")
	else:
		record_log(log_tenma_file_pool, folder_name, shippai, "张图片挂了")


# def bool_dl_with_pool(json_url):
def book_dl_with_pool(bookId):
	bookname = getBookName("163", bookId)
	if bookname == None:
		return record_log(log_book_file, "未能找到书本", 163, bookId)
	json_url = "https://manhua.163.com/book/catalog/" + str(bookId) + ".json"
	rq = request.Request(json_url)
	response = request.urlopen(rq)
	menu_js = response.read().decode("utf8")
	js = json.loads(menu_js)
	# print(type(js["catalog"]["sections"][0]["sections"][0]))
	# print(len(js["catalog"]["sections"][1]["sections"]))
	num_of_chap = 0
	for each_section in js["catalog"]["sections"]:
		num_of_chap+=1
		# 多个篇章的文件夹分开装
		chaptername = each_section["fullTitle"]
		chap_foldername = dl_dir+bookname+"/"+'{:0>2}'.format(
				str(num_of_chap)) + "_" + chaptername + '/'  # 格式化文件夹名字，用0补全前面
		# print(len(each_section)) # 因为这个是dict，所以len就是 16（dict里元素个数）
		# print( each_section )
		record_log(log_tenma_file_pool,"开始下载篇章",chap_foldername)


		num_of_ep = 0
		for subsection in each_section["sections"]:
			num_of_ep += 1
			# if num_of_ep == 2:
			# 	return
			bookId = subsection["bookId"]
			pages = subsection["wordCount"]
			sectionId = subsection["sectionId"]
			fullTitle = subsection["fullTitle"]
			url_one_wa = "https://manhua.163.com/reader/" + bookId + "/" + sectionId + "/"
			ep_folder_name = chap_foldername + '{:0>4}'.format(
				str(num_of_ep)) + " " + fullTitle + '/'  # 格式化文件夹名字，用0补全前面
			# print(ep_folder_name,url_one_wa)
			ep_dl_with_pool(pages, url_one_wa, ep_folder_name)

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

if __name__=="__main__":
	# 使用多线程： 用每个线程下载不同的图片（每一话新开pool）
	# initializeAlready(already_tenma, already_tenma_file)
	# try_getJson()
	tenma = "4458002705630123103"
	L_Dart = "4603479161120104695"  # 神契 幻奇谭
	# getBookName("163", L_Dart)
	initializeAlready(already_tenma_pool,already_tenma_file_pool)
	book_dl_with_pool(L_Dart)