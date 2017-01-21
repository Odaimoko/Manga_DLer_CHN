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

	def _init(self):
		pass

	def dl_pic(self, pic_url, file_name):
		# Return True: Successfully , False otherwise
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
			except error.URLError as t:
				record_log(self.log_file_name, "下载", file_name, "超时", dl_times, "times")
			except Exception as e:
				record_log(self.log_file_name, "其他错误", e)
			else:
				return True
		return False
	def dl_whole_book(self):
		pass
	def _dl(self):
		if self.can_dl:
			self.dl_whole_book()
