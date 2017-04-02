import threading, time, os, re, string
from functools import wraps
from threading import Timer

# multiprocessing.Queue
# sys.path.append("..")
# import iMyUtil
# =======================CONSTS==========================
"""
文件夹名字若无说明，统一在后面加/
"""
dl_dir = "../"
log_dir = "../log/"
dl_log_dir = log_dir + "dl/"
data_dir = "../data/"
# log文件放在一起，已下载每一个单独放在对应文件夹

already_pic_file = "already_pic.txt"
already_ep_file = "already_ep.txt"
log_file = "log.txt"
shippai_file = "shippai.json"
db_file = "db"

# =======================IDS==========================
ID_163 = "_163_"
ID_ikm = "_iKanMan_"


# FUNCS


def initializeAlready(alreadySet, alreadyFile):
	exist = os.path.exists(alreadyFile)
	if exist:
		with open(alreadyFile, "rb") as f:
			already_text = f.read().decode("utf8")
			for line in already_text.splitlines():
				# 记录全部url，包括http:// 和末尾的/
				alreadySet.add(line)
			del already_text
	else:
		createFile(alreadyFile)


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


def createFolder(name, logfile=None):
	import os
	name = name.strip().rstrip("/")
	exist = os.path.exists(name)
	if exist:
		# print(name + " already here.")
		pass
	else:
		# print(name + " created.")
		os.makedirs(name)
		if logfile:
			record_log(logfile, name + " created.")


def createFile(name, logfile=None, initial=""):
	import os
	if os.path.exists(name):
		return False
	name_list = name.split("/")
	if len(name_list) > 1:
		path = name_list[:-1]
		createFolder("/".join(path), logfile)
	with open(name, "w") as f:
		f.write(initial)
	return True


def hex2dec(string_num):
	return int(string_num.upper(), 16)


def url_utf8tostr(url):
	find_utf8 = re.compile(r"%\w\w")
	chinese = find_utf8.findall(url)
	# print("chinese",chinese)
	if not chinese:  # if there's no %\w\w, which means all is chars chinese will be an empty list
		return url
	chars = []
	for char in chinese:
		chars.append(hex2dec(char[1:]))
	chars = bytes(chars).decode("utf8")
	real_url = ""
	ind = 0
	i = 0
	for c in url:
		if i > 0:
			i -= 1
			continue
		if c == "%":
			real_url += chars[ind]
			ind += 1
			i += 8  # 1个utf8是9位，所以后面8个都不看
		else:
			real_url += c
	return real_url


def encodeURIComponent(to):
	# to = "一步"
	bs = to.encode()
	result = ""
	for l in list(bs):
		result += (hex(l)).replace("0x", '%')
	return result.upper()


def writeTo(content, file=None):
	if not file:
		with open("temp.txt", "w") as f:
			f.write(str(content))
			f.write("\n")


def log_time(*text, record=None):
	def real_deco(func):
		@wraps(func)
		def impl(*args, **kw):
			start = time.clock()
			func(*args, **kw)
			end = time.clock()
			r = print if not record else record
			t = (func.__name__,) if not text else text
			print(r, t)
			r(*t, "花费时间", end - start, "秒")

		return impl

	return real_deco


def time_limit(interval):
	# 抛出Timeout Error
	def deco(func):
		def time_out():
			raise TimeoutError()

		@wraps(func)
		def deco(*args, **kwargs):
			timer = Timer(interval, time_out)
			timer.start()
			res = func(*args, **kwargs)
			return res

		return deco

	return deco

#
# def safe_file_name(s):
# 	if s==None:
# 		return None
# 	return s.replace("/", "／").replace("\\", "＼").replace("?", "？").\
# 		replace("|", "｜").replace("<", "＜").replace(">", "＞").\
# 		replace(",", "：").replace("\"", "＂").replace("*", "＊")


def create_safefilepath_table():
	table =  {
		"/": "／",
		"\\": "＼",
		"?": "？",
		"|": "｜",
		"<": "＜",
		">": "＞",
		":": "：",
		"\"": "＂",
		"*": "＊"
	}
	table.update({
		c: None for c in set([chr(i) for i in range(128)]).difference(string.printable)
	})
	return str.maketrans(table)


safefilepath_table = create_safefilepath_table()


def safe_file_name(s):
	"""Return a safe directory name."""
	return s.translate(safefilepath_table)

# OTHERS

js_lib_by_py = """
var escape = function(text){pyimport urllib; return urllib.parse.quote(text)};
var unescape = function(text){pyimport urllib; return urllib.parse.unquote(text)};
var encodeURIComponent = function(text){pyimport urllib; return urllib.parse.quote(text, safe='~()*!.\\'')};
var decodeURIComponent = unescape;
"""
