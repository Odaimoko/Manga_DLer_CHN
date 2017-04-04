def get_scale(root):
	"""To display in high-dpi we need to grab the scale factor from OS"""

	import platform, traceback, subprocess
	# There is no solution on XP

	if platform.system() == "Windows" and platform.release() == "XP":
		return 1.0

	# Windows
	# https://github.com/eight04/ComicCrawler/issues/13#issuecomment-229367171
	try:
		from ctypes import windll
		user32 = windll.user32
		user32.SetProcessDPIAware()
		w = user32.GetSystemMetrics(0)
		return w / root.winfo_screenwidth()
	except ImportError:
		pass
	except Exception as e:
		traceback.print_exc()

	# GNome
	try:
		args = ["gsettings", "get", "org.gnome.desktop.interface", "scaling-factor"]
		with subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True) as p:
			return float(p.stdout.read().rpartition(" ")[-1])
	except Exception:
		traceback.print_exc()

	return 1.0

class UIdraw:
	pass

class EventBinder:
	pass

class MainUI:
	def __init__(self):
		pass