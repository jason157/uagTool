# coding=utf-8
# coding=utf-8
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from GuiFunctions import *

class GuiMain(tk.Tk):
	def __init__(self):
		'''初始化'''
		self.root=super().__init__()  # 有点相当于tk.Tk()
		self.createWidgets()
		self.resizable(False, False)

		'''初始化菜单'''
		self.menubar = tk.Menu(self.root)  # 创建菜单栏

		# 创建“文件”下拉菜单
		filemenu = tk.Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="打开", command=self.__file_open)
		#filemenu.add_command(label="新建", command=self.__file_new)
		#filemenu.add_command(label="保存", command=self.__file_save)
		filemenu.add_separator()
		filemenu.add_command(label="退出", command=self.quit)

		# 创建“编辑”下拉菜单
		## 也许用不到这几个菜单
		editmenu = tk.Menu(self.menubar, tearoff=0)
		editmenu.add_command(label="OCS批量开户接口", command=self.OpenAccount2OCS)
		#editmenu.add_command(label="导出选中会议", command=self.__edit_export)
		#editmenu.add_command(label="撤销/返回", command=self.__edit_paste)

		# 创建“帮助”下拉菜单
		helpmenu = tk.Menu(self.menubar, tearoff=0)
		helpmenu.add_command(label="使用说明", command=self.__help_usage)
		helpmenu.add_command(label="关于", command=self.__help_about)


		# 将前面三个菜单加到菜单栏
		self.menubar.add_cascade(label="文件", menu=filemenu)
		self.menubar.add_cascade(label="功能", menu=editmenu)
		self.menubar.add_cascade(label="帮助", menu=helpmenu)

		# 最后再将菜单栏整个加到窗口 root
		self.config(menu=self.menubar)

		# 初始化 后显示帮助
		self.__help_usage()

	def __file_open(self):
		self.textbox.delete('1.0', tk.END)  # 先删除所有
		filename=tk.filedialog.askopenfilename()
		if os.path.isfile(filename):
			self.filedata=openFile(filename)
			try:
				confList=getConfList(self.filedata)
				for confItem in confList:
					self.textbox.insert(tk.END, confItem + '\r\n')
			except IndexError:
				messagebox.showerror('打开', '读取文件错误！\n请选择正确的文件，谢谢！')  # 消息提示框
		else:
			messagebox.showinfo('打开', '没有选择文件')  # 消息提示框
			pass
	def __file_new(self):
		messagebox.showinfo('新建', '文件-新建！')  # 消息提示框
		pass

	def __file_save(self):
		messagebox.showinfo('保存', '文件-保存！')  # 消息提示框
		pass

	def __edit_export(self):
		pass

	def __edit_cut(self):
		messagebox.showinfo('剪切', '编辑-剪切！')  # 消息提示框
		pass

	def __edit_copy(self):
		messagebox.showinfo('复制', '编辑-复制！')  # 消息提示框
		pass

	def __edit_paste(self):
		messagebox.showinfo('粘贴', '编辑-粘贴！')  # 消息提示框
		pass

	def __help_about(self):
		messagebox.showinfo('关于', '作者：Jason \n verion 0.0.1 \n 感谢您的使用！ ')  # 弹出消息提示框
	def __help_usage(self):
		usageString='使用帮助:\n这是UAG日志分析的小程序\n' +\
		'首先要在文件->打开中打开uag.log文件(其他包含会议信息的文件也可以）\n' +\
		'如果检测到会议记录，就会分析并列出会议简要信息\n' + \
		'有如下两种操作：\n' + \
		'1.选中对应会议的行后“单击”右键，就可以看到会议的详情\n' + \
		'2.选中对应会议的行后“双机”右键，就可以保存当前会议的对应日志\n' + \
		'其他功能正在努力，请期待……\n'
		self.textbox.insert(tk.END, usageString + '\r\n')
		#messagebox.showinfo('使用帮助',usageString)


	def getFilename(self):
		return self.filename


	def createWidgets(self):
		'''界面'''
		self.title('uag日志处理工具')
		self.columnconfigure(0, minsize=50)

		# 定义一些变量
		self.Timeentryvar = tk.StringVar()
		self.Numentryvar = tk.StringVar()
		self.gfilename = tk.StringVar()
		self.keyvar = tk.StringVar()
		self.keyvar.set('关键字')
		items = ['BufferPool', 'Close', 'Data Capture', 'Compress', 'Pqty', 'Sqty']

		# 先定义顶部和内容两个Frame，用来放置下面的部件

		contentframe = tk.Frame(self)

		contentframe.pack(side=tk.TOP)

		# 内容区域（三个部件）
		# -- 前两个滚动条一个竖直一个水平
		rightbar = tk.Scrollbar(contentframe, orient=tk.VERTICAL)
		bottombar = tk.Scrollbar(contentframe, orient=tk.HORIZONTAL)
		self.textbox = tk.Text(contentframe, yscrollcommand=rightbar.set, xscrollcommand=bottombar.set)
		# -- 放置位置
		rightbar.pack(side=tk.RIGHT, fill=tk.Y)
		bottombar.pack(side=tk.BOTTOM, fill=tk.X)
		self.textbox.pack(side=tk.LEFT, fill=tk.BOTH)
		# -- 设置命令
		rightbar.config(command=self.textbox.yview)
		bottombar.config(command=self.textbox.xview)
		# --text鼠标绑定
		self.textbox.bind("<Button-3>", self.mouseRightClick)
		self.textbox.bind("<Double-Button-1>", self.mouseLeftDoubleClick)
		self.textbox.tag_configure("current_line", background="LightGrey")
		self.textbox.bind("<Motion>", self._highlightline)
	'''
	搜索框，暂时隐藏
	'''
	def searchWidgets(self,topframe):
		topframe = tk.Frame(self, height=80)
		topframe.pack(side=tk.TOP)
		# 顶部区域（四个部件）
		# -- 前三个直接用 tk 的 widgets，第四个下拉列表 tk 没有，ttk 才有，比较麻烦
		gTimelabel = tk.Label(topframe, text='时间:')
		gTimeentry = tk.Entry(topframe, textvariable=self.Timeentryvar)
		gNumlabel = tk.Label(topframe, text='号码:')
		gNumentry = tk.Entry(topframe, textvariable=self.Numentryvar)
		gSearchbutton = tk.Button(topframe, command=self.__opendir, text='开始搜索')
		# -- 绑定事件
		gTimelabel.bind('<Return>', func=self.__refresh)
		gNumlabel.bind('<Return>', func=self.__refresh)
		# gcombobox.bind('<ComboboxSelected>', func=self.__refresh) # 绑定 <ComboboxSelected> 事件
		# -- 放置位置
		gTimelabel.grid(row=0, column=0, sticky=tk.W)
		gTimeentry.grid(row=0, column=1)
		gNumlabel.grid(row=0, column=2, sticky=tk.W)
		gNumentry.grid(row=0, column=3)
		gSearchbutton.grid(row=0, column=4)

	def __opendir(self):
		'''打开文件夹的逻辑'''
		self.textbox.delete('1.0', tk.END)  # 先删除所有

		#self.dirname = filedialog.askdirectory()  # 打开文件夹对话框
		self.filename=filedialog.askopenfilename()
		self.gfilename.set(self.filename)  # 设置变量entryvar，等同于设置部件Entry

		if not self.filename:
			messagebox.showwarning('警告', message='未选择文件！')  # 弹出消息提示框

		self.textbox.update()

	def __refresh(self, event=None):
		'''更新的逻辑'''
		self.textbox.delete('1.0', tk.END)  # 先删除所有

		self.dirlist = os.listdir(self.entryvar.get())
		for eachdir in self.dirlist:
			self.textbox.insert(tk.END, eachdir + '\r\n')

		self.textbox.update()

	def addmenu(self, Menu):
		'''添加菜单'''
		Menu(self)
	def showListToTextBox(self,itemList):
		self.textbox.delete('1.0', tk.END)  # 先删除所有
		for echitem in itemList:
			self.textbox.insert(tk.END, echitem + '\r\n')
		self.textbox.update()


	def getLineContent(self):
		pass
	'''
	右键在行中的时候，弹出窗口显示本行包含的会议信息
	'''
	def mouseRightClick(self,even=None):
		linestring = self.textbox.get("current linestart","current lineend+1c")
		if "Time" and "UAGID" and "Number" in linestring:
			Confinfo=getConfInfo(self.filedata,linestring)
			self.popUpText(Confinfo)
		else:
			pass
	def mouseLeftDoubleClick(self,even=None):
		#messagebox.showwarning('警告', message='左键单击测试！')  # 弹出消息提示框
		linestring = self.textbox.get("current linestart", "current lineend+1c")
		if "Time" and "UAGID" and "Number" in linestring:
			saveFilename=tk.filedialog.asksaveasfilename()
			if saveFilename:
				fileSave = open(saveFilename, 'w', encoding="UTF8")
				UAGID = getUAGIDfromConfList(linestring)
				for line in self.filedata:
					if UAGID in line:
						fileSave.write(line)
				fileSave.close()
			else:
				pass
		else:
			pass
		if len(linestring) < 1:
			pass


	def mouseRightDoubleClick(self,even=None):
		messagebox.showwarning('警告', message='未选择文件！')  # 弹出消息提示框
	def popUpText(self,ConfInfo):
		PopupFrame = tk.Toplevel(self)
		#PopupFrame.pack(side=tk.TOP)
		Popuprightbar = tk.Scrollbar(PopupFrame, orient=tk.VERTICAL)
		Popupbottombar = tk.Scrollbar(PopupFrame, orient=tk.HORIZONTAL)
		Popuptextbox = tk.Text(PopupFrame, yscrollcommand=Popuprightbar.set, xscrollcommand=Popupbottombar.set)
		Popuptextbox = tk.Text(PopupFrame, yscrollcommand=Popuprightbar.set, xscrollcommand=Popupbottombar.set)
		Popuptextbox.pack(side=tk.LEFT, fill=tk.BOTH)
		# -- 设置命令
		#Popuprightbar.config(command=self.Popuptextbox.yview)
		#Popupbottombar.config(command=self.Popuptextbox.xview)
		Popuptextbox.delete('1.0', tk.END)  # 先删除所有
		for key in ConfInfo:
			if type(ConfInfo[key])==str:
				Popuptextbox.insert(tk.END, key +":" +ConfInfo[key]+'\r\n')
			if type(ConfInfo[key])==list:
				for item in ConfInfo[key]:
					Popuptextbox.insert(tk.END, key + ":" + item + '\r\n')
			if type(ConfInfo[key])==dict:
				tempdic=ConfInfo[key]
				for okey in tempdic:
					Popuptextbox.insert(tk.END, okey + ":" + tempdic[okey] + '\r\n')
		Popuptextbox.update()

	def _highlightline(self, event=None):
		self.textbox.tag_remove("current_line", 1.0, "end")
		self.textbox.tag_add("current_line", "current linestart", "current lineend+1c")

	def OpenAccount2OCS(self):
		self.textbox.delete('1.0', tk.END)  # 先删除所有
		numlist=[]
		filename=tk.filedialog.askopenfilename()
		if os.path.isfile(filename):
			self.filedata=openFile(filename)
			for num in self.filedata:
				num=num.strip('\n')
				if num.isdigit():
					numlist.append(num)
					#self.textbox.insert(tk.END, num + '\r\n')
					pureNumberFlag=True
				else:
					pureNumberFlag = False
					self.textbox.insert("current linestart", num + ":号码错了" + '\r\n')
			self.textbox.delete('1.0', tk.END)  # 先删除所有
			for num in numlist:
				returncode = OpenAccountToOCS(num)
				if int(returncode)==200:
					self.textbox.insert("current linestart",num + "200 OK" +'\r\n')
				else:
					self.textbox.insert("current linestart", num + ":出现错误了" + '\r\n')
					pass
		else:
			messagebox.showinfo('打开', '没有选择文件')  # 消息提示框
			pass
