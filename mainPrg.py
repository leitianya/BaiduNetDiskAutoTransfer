# coding:utf-8
#Version : 0.2 Beta
#Latest Update:2018-02-24
#


#THIS IS AN UNSTABLE VERSION

#link.txt 示例："https://pan.baidu.com/s/xxxx----2333"
#目前仅支持带提取码的链接批量转存

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os,sys

os.system('cls')
# Define Log Moudle
import logging
logFileName = (str(time.ctime())+"_LOG.log").replace(":","-").replace(" ","")
logger = logging.getLogger(__name__)
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
logHandler = logging.FileHandler(logFileName)
logHandler.setFormatter(logFormat)
logger.addHandler(logHandler)
#Log Level
logger.setLevel(logging.INFO)#日志级别

def findPath(WebDri,URL,destDir):#获取转存目录
	try:
		isFound = False
		nodePaths = WebDri.find_elements_by_class_name("treeview-txt")
		#debugNodePaths = WebDri.find_elements_by_css_selector("span."+destDir)
		#logger.debug(debugNodePaths)
		logger.debug("[+] nodePaths : %s" % str(nodePaths))
		for item in nodePaths:
			#print item.get_attribute("node-path")
			if (item.get_attribute("node-path") == destDir):
				print ("[+] 成功定位目标文件夹 : %s " % destDir)
				logger.info("[+] 成功定位目标文件夹 : %s " % destDir)
				logger.debug("[*] 目标文件夹原始信息 : %s" % str(item))
				item.click()
				isFound = True
				break
		return isFound
	except:
		logger.exception("[-] 发生错误 : %s" % URL)
		return False

def startTransfer(WebDri,URL,code,destDir):#转存主过程
	print ("[*] 正在获取 %s 提取码 %s ..." % (URL,code))
	logger.info("[*] 正在获取 %s 提取码 %s ...." % (URL,code))
	WebDri.get(URL)
	enterCodeBtn= WebDri.find_elements_by_class_name('g-button-blue-large')
	logger.debug("[*] 确认提取码按钮原始信息 : %s" % str(enterCodeBtn))
	codeTextEdit = WebDri.find_elements_by_class_name('LxgeIt')
	logger.debug("[*] 提取码输入框原始信息: %s" % str(codeTextEdit))
	if(codeTextEdit != []):
		codeTextEdit[0].send_keys(list(code))
		logger.debug("[*] 提取码 : %s 已输入." % code)
		enterCodeBtn[0].click()
	else:
		return False
	try:#定位转存按钮
		time.sleep(4)
		transferBtn = WebDri.find_elements_by_class_name('g-button')
		logger.debug("[*] 转存按钮原始信息 : %s" % str(transferBtn))
		if (transferBtn == []):
			print ("[-] 无法转存文件 %s" % URL)
			logger.warn("[-] Cannot 无法转存文件 %s" % URL)
			return False
		else:
			for item in transferBtn:
				if (item.get_attribute('title') == unicode("保存到网盘","gb2312")):
					logger.debug("[+] 已定位转存按钮 %s " % str(item))
					logger.info("[+] 已定位转存按钮")
					item.click()
					break
	except:
		logger.exception("[-] 发生错误 : %s" % URL)
		return False

	try:#判断是否登陆
		time.sleep(1)
		qrcode = WebDri.find_elements_by_class_name("tang-pass-qrcode-img")
		if (qrcode != []):
			print ("[-] 请先登录 !!!!!")
			logger.error("No Logon.")
			sys.exit()
	except:
		logger.exception("[-] 发生错误 : %s" % URL)
		return False

	try:#开始转存
		time.sleep(2)
		nodeSplitList = destDir.split("/")
		dir = ""
		for i in range(1,len(nodeSplitList)):#循环调用findPath()以确定转存目录
			dir += ("/"+nodeSplitList[i])
			logger.debug("[*] Current Dir : %s " % dir)
			if findPath(WebDri,URL,dir):
				print ("[+] 已发现目录 %s" % dir)
				logger.info("[+] 已发现目录 %s" % dir)
				time.sleep(2)
				continue
			else:
				print ("[-] 无法定位目标目录 : %s" % dir)
				logger.error("[-] 无法定位目标目录 : %s 原始目标目录 : %s " % (dir,destDir))
				return False
		pathConfirmBtn = WebDri.find_elements_by_class_name('g-button')
		if pathConfirmBtn == []:
			print ("[-] 无法转存文件 %s" % URL)
			logger.error("[-] 无法转存文件 %s" % URL)
			return False
		for item in pathConfirmBtn:
			if (item.get_attribute('title') == unicode("确定","gb2312")):
				logger.debug("[+] 已定位转存目录确认按钮 %s " % str(item))
				logger.info("[+] 已定位转存目录确认按钮")
				item.click()
				return True
	except:
		logger.exception("[-] 发生错误 : %s" % URL)
		return False

def login(WebDri):
	WebDri.get("https://pan.baidu.com/")
	print("登录网盘后请将页面切换到回收站并确认网页加载完毕后再执行下一步")
	raw_input("[?] 请确认你已经成功登录网盘.")
	logger.info("[+] Logon In")
	print ("[+] Logon In")

def main():
	try:
		errorLinkList = []
		gotLinkList = []
		destDir = "/Test/Testt"
		linkList = []
		try:
			with open("link.txt","r") as f:
				linkList = f.readlines()
				f.close()
		except:
			print ("[-] 无法打开指定文件，请查看日志")
			logger.exception("[*] Error On Opening File.")
			return
		print ("[*] 共找到 %d 个链接." % len(linkList))
		logger.info("[*] 共找到 %d 个链接." % len(linkList))
		print("[*] 正在启动Chrome")
		browser = webdriver.Chrome()
		login(browser)
		for item in linkList:
			item = item.strip()
			URL = item.split("----")[0]
			code = item.split("----")[1][:4]
			print ("[*] 开始文件转存过程")
			logger.info("[*] 开始文件转存过程")
			if (startTransfer(browser,URL,code,destDir) == False):
				errorLinkList.append((URL+"----"+code))
				print ("[-] 发生错误 : %s" % URL)
				logger.error(("[-] 发生错误 : %s" % URL))
			else:
				gotLinkList.append((URL+"----"+code+"\n"))
				print ("[+] 成功转存文件 : %s [%d/%d]" % (URL,len(gotLinkList),len(linkList)))
				print ("\n")
				logger.debug(str(gotLinkList))
				with open("gotLink.txt","w+") as f:
					f.writelines(gotLinkList)
					f.close()
		print ("[*] %d 链接错误" % len(errorLinkList))
		logger.info("[*] %d 链接错误" % len(errorLinkList))
		errFile = open("errLink.txt","w+")
		for item in errorLinkList:
			errFile.write(item)
			errFile.write("\n")
			print item
		errFile.close()
		print ("[+] All Task Done.Exiting...")
		browser.quit()
	except:
		logger.exception("")

if (__name__ == "__main__"):
	main()