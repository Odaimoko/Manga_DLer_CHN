from urllib import request, error
from const import *
import socket


class BaseDLer:
	MAX_DL_TIMES = 1
	MAX_EP_TIMES = 3
	def __init__(self):
		self.can_dl = True
		self.already_pic_set = set()
		self.already_ep_set = set()  # 记录已下载的话数
		self.log_file_name = ""
		self.already_pic_file_name = ""
		self.success_dl_site = -1  # 标记着成功下载的标号，如果成功了，以后就一直用这个。

		self.mikanse_file_name = ""
		self.mikanse = dict()  # 存下没有下好的，key:文件夹名，value：dict：文件名key+url的value

	def _init(self):
		pass

	def check_db(self):
		"""
		如果db里有，直接读取db里的，并不更新（因为一开程序自动更新已存在的）
		"""
		return False

	def get_chaplist(self):
		# name only
		pass

	def get_eplist_for_one_chap(self, index=0):
		'''
		
		:param index: the index of chapter
		:return: str list, just name
		'''
		pass

	def record(self, *content):
		record_log(self.log_file_name, *content)

	def dl_pic(self, pic_url, file_name):
		# Return True: Successfully , False otherwise
		# pic_url may be a list or a str
		# print(type(pic_url))
		allpath = file_name.split('/')
		folder_name = "/".join(allpath[:-1])
		pure_file_name = allpath[-1]

		dl_result = ()  # 只用记录一次

		def record_broken_pic():
			if folder_name in self.mikanse.keys():  # 创建对应字典
				d = self.mikanse.get(folder_name)  # 文件名key+url的value
				d[pure_file_name] = pic_url
			else:
				self.mikanse[folder_name] = dict()
				self.mikanse[folder_name][pure_file_name] = pic_url

		def dl_one(pic_url):  # receives a str
			# print("进入dl_one_子例程")
			dl_times = 0
			to_record = ()
			while dl_times < BaseDLer.MAX_DL_TIMES:
				dl_times += 1
				rq = request.Request(pic_url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
				# rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
				try:
					start = time.clock()
					response = request.urlopen(rq, timeout=2)
					end = time.clock()
					# self.record("Reading pics..", end - start, "s")
					start = time.clock()
					with open(file_name, "wb") as pic:
						pic.write(response.read())
						addToAlready(file_name, self.already_pic_set, self.already_pic_file_name)
					end = time.clock()
				# self.record("Writing pics...", end - start, "s")
				except Exception as e:
					record_broken_pic()
					to_record = ("错误", e)

				# except socket.timeout as s:
				# 	to_record = ("下载", file_name, "超时", dl_times, "times")
				# 	break
				# except error.URLError as t:
				# 	if t.errno == 403:
				# 		to_record = (t,)
				# 		break
				# 	# if dl_times < 3:
				# 	# 	continue
				else:  # 没有发生错误
					to_record = (True,)
					break
			return to_record

		if isinstance(pic_url, str):
			# self.record("进入单图")
			dl_result = dl_one(pic_url)
			if True in dl_result:
				# record_log(self.log_file_name,)
				return True
			else:
				record_log(self.log_file_name, dl_result)
				return False

		elif isinstance(pic_url, list):
			isDLed = False
			# print("多图")
			if self.success_dl_site != -1:
				dl_result = dl_one(pic_url[self.success_dl_site])
				if True in dl_result:
					record_log(self.log_file_name, "图片下载完成", file_name)
					return True
			# 如果成功的没下载好，那就重新扫一遍，但是同样的不扫
			for i, url in enumerate(pic_url):
				# 遍历所有下载地址，如果有一个下载成功就好
				if i == self.success_dl_site:
					continue
				dl_result = dl_one(url)
				if True in dl_result:
					self.success_dl_site = i
					record_log(self.log_file_name, "图片下载完成", file_name)
					return True
				else:
					pass
			record_log(self.log_file_name, dl_result)
			return False

	def zip_one_ep(foldername):
		# print(foldername[:-1]+'.zip') # 目录最后带有/
		import zipfile
		f = zipfile.ZipFile(foldername[:-1] + '.zip', 'w', zipfile.ZIP_DEFLATED)
		startdir = foldername
		for dirpath, dirnames, filenames in os.walk(startdir):
			for filename in filenames:
				f.write(dirpath + filename, filename)
		f.close()

	def dl_whole_book(self):
		pass

	def _dl(self):
		if self.can_dl:
			self.dl_whole_book()

	def log_wrapper(self, *text):
		log = log_time(*text, self.record)
		return log
