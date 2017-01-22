from urllib import request, error
from paya.const import *


class BaseDLer:
	MAX_DL_TIMES = 3

	def __init__(self):
		self.can_dl = True
		self.already_pic_set = set()
		self.already_ep_set = set()  # 记录已下载的话数
		self.log_file_name = ""
		self.already_pic_file_name = ""
		self.success_dl_site = -1  # 标记着成功下载的标号，如果成功了，以后就一直用这个。

	def _init(self):
		pass

	def dl_pic(self, pic_url, file_name):
		# Return True: Successfully , False otherwise
		# pic_url may be a list or a str
		# print(type(pic_url))

		dl_result = ()  # 只用记录一次

		def dl_one(pic_url):  # receives a str
			dl_times = 0
			while dl_times < self.MAX_DL_TIMES:
				dl_times += 1
				rq = request.Request(pic_url)  # 也许有机会重用一个对象，因为这里每次都要新建一个
				# rq.add_header('User-Agent', 'Mozilla/4.0(compatible;MSIE5.5;WindowsNT)')
				try:
					response = request.urlopen(rq, timeout=3000)
					with open(file_name, "wb") as pic:
						pic.write(response.read())
						addToAlready(file_name, self.already_pic_set, self.already_pic_file_name)
					to_record = (True)
				except error.URLError as t:
					if dl_times < 3:
						continue
					if t.code == 403:
						to_record = (t,)
					else:
						to_record = ("下载", file_name, "超时", dl_times, "times")
						break
				except Exception as e:
					if dl_times < 3:
						continue
					to_record = ("其他错误", e)
				else:  # 没有发生错误
					to_record = (True,)
			return to_record

		if isinstance(pic_url, str):
			print("进入单图")
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

	def dl_whole_book(self):
		pass

	def _dl(self):
		if self.can_dl:
			self.dl_whole_book()
