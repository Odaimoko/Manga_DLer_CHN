import threading, time, os

# multiprocessing.Queue
# sys.path.append("..")
# import iMyUtil
# =======================CONSTS==========================

dl_dir = "../"
main_log_dir = "../log/"

dl_log_dir = main_log_dir + "dl/"
# log文件放在一起，已下载每一个单独放在对应文件夹

main_already_pic_file = "already_pic.txt"
main_already_ep_file = "already_ep.txt"
main_log_file = "log.txt"

# =======================IDS==========================
ID_163 = "_163_"
ID_ikm = "_iKanMan_"


#


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


def createFile(name, logfile=None):
	import os
	if os.path.exists(name):
		return False
	name_list = name.split("/")
	if len(name_list) > 1:
		path = name_list[:-1]
		createFolder("/".join(path), logfile)
	with open(name, "w") as f:
		pass
	return True
