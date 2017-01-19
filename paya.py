from urllib import request, parse
import re, json
import sys, time

# sys.path.append("..")
# import iMyUtil

already_tenma_file = "already_tenma.txt"
log_tenma_file = "tenma_log.txt"
already_tenma = set()
local_tenma = "天才麻将少女_本篇/"

with open(already_tenma_file, "rb") as f:
	already_text = f.read().decode("utf8")
	for line in already_text.splitlines():
		# 记录全部url，包括http:// 和末尾的/
		already_tenma.add(line)
	del already_text


def addToAlready(content, alreadySet, alreadyFileName):
	if content in alreadySet:
		return
	alreadySet.add(content)
	with open(alreadyFileName, "ab") as al:
		al.write(str(content).encode("utf8"))
		al.write("\n".encode())


def record_log(logFileName, *src):
	print(" ".join(src))
	with open(logFileName, "ab") as lo:
		# 解决直接write出现 encode 错误，还是手动encode+写入二进制
		lo.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).encode())
		lo.write(":".encode())
		for s in src:
			lo.write(" ".encode())
			lo.write(str(s).encode())
		lo.write("\n".encode())


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
			record_log(log_tenma_file, file_name, "已下载")
			continue
		try:
			with open(file_name, "wb") as pic:
				rq = request.Request(url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
				rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
				response = request.urlopen(rq, timeout=3000)
				pic.write(response.read())
				addToAlready(file_name, already_tenma, already_tenma_file)
		except Exception as e:
			record_log(log_tenma_file, "This Folder: ", folder_name, " Time out, pic: ", num, " , URL: ", url)
			record_log(log_tenma_file, e)
	record_log(log_tenma_file, folder_name, "下载完成")


def TEMA():
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
	json_url = "https://manhua.163.com/book/catalog/4458002705630123103.json"
	rq = request.Request(json_url)
	response = request.urlopen(rq)
	menu_js = response.read().decode("utf8")
	js = json.loads(menu_js)
	print(type(js["catalog"]["sections"][0]["sections"][0]))
	print(len(js["catalog"]["sections"][0]["sections"]))
	# for each in js["catalog"]["sections"]:
	# 	print(each)
# TEMA()

try_getJson()