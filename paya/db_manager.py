from paya.const import db_file
from threading import *
import sqlite3
dblock = Lock()

class DBManager:
	'''
	管理本地数据库
	- 设置
	- 书本
	- 失败（为了不遍历书本）
	'''

	def __init__(self):
		pass

	def save_settings(self):
		pass

	def set_ep(self):
		pass

	def set_chap(self):
		pass

	def set_book(self):
		pass

	def set_shippai(self):
		pass

	def get_ep(self):
		pass

	def get_chap(self):
		pass

	def get_book(self):
		pass

	def get_shippai(self):
		pass

	def search(self):
		pass

	def checklocal(self):
		'''检查本地漫画目录和数据库是否匹配'''
		pass
	def upgrade_db(self):
		'''更新漫画数据库'''
		pass
