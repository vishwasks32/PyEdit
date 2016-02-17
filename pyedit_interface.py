#! /usr/bin/env python
# Author : Vishwas K Singh
# Program: A simple text editor
import os
import Tkinter as tk
import tkFileDialog as tkfd
import tkMessageBox as tkmb


class pyedit(tk.Frame):	
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.master.title('PyEdit - Untitled')
		global version
		version = 1.0
		self.showln = tk.IntVar()
		self.hltln = tk.IntVar()
		self.showinfo = tk.IntVar()
		self.clrsyntx = tk.IntVar()
                self.clrschemes ={
				'Default White': '000000.FFFFFF',
				'Greygarious Gray': '83406A.D1D4D1',
				'Lovely Lavender': '202B4B.E1E1EF',
				'Aquamarine': '5B8340.D1E7E0',
				'Bold Beige': '4B4620.FFF0E1',
				'Cobalt Blue': 'FFFFBB.3333AA',
				'Olive Green': 'D1E7E0.5B8340'
		}
		self.themechoice = tk.StringVar()
		self.createWidgets()

	def createWidgets(self):
		top = self.winfo_toplevel()
		self.menubar = tk.Menu(top)
		top['menu'] = self.menubar
		
		# Menus
		self.filemenu = tk.Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label='File', menu=self.filemenu)
		self.filemenu.add_command(label='New',accelerator='ctrl+N',command=self.new_file)
		self.filemenu.add_command(label='Open',accelerator='ctrl+O',command=self.open_file)
		self.filemenu.add_command(label='Save',accelerator='ctrl+S', command=self.save_file)
		self.filemenu.add_command(label='Save As', command=self.save_as)
		self.filemenu.add_separator()
	        self.master.protocol("WM_DELETE_WINDOW", self.exit_editor)
		self.filemenu.add_command(label='Exit',accelerator='alt+F4', command=self.exit_editor)

		self.editmenu = tk.Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label='Edit', menu=self.editmenu)
		self.editmenu.add_command(label='Undo',accelerator='ctrl+Z', compound=tk.LEFT,command=self.undo)
		self.editmenu.add_command(label='Redo',accelerator='ctrl+Y', command=self.redo)
		self.editmenu.add_separator()
		self.editmenu.add_command(label='Cut',accelerator='ctrl+X', command=self.cut)
		self.editmenu.add_command(label='Copy',accelerator='ctrl+C', command=self.copy)
		self.editmenu.add_command(label='Paste',accelerator='ctrl+V', command=self.paste)
		self.editmenu.add_separator()
		self.editmenu.add_command(label='Find All',accelerator='ctrl+F', command=self.on_find)
		self.editmenu.add_command(label='Select All',accelerator='ctrl+A', command=self.select_all)
		
		self.viewmenu = tk.Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label='View', menu=self.viewmenu)
		self.viewmenu.add_checkbutton(label='Toggle Line Number', variable=self.showln, command=self.update_line_number)
		self.showinfo.set(1)
		self.viewmenu.add_checkbutton(label='Show Info Bar at Bottom', variable=self.showinfo, command=self.update_line_number)
		self.viewmenu.add_checkbutton(label='Highlight Current Line',variable=self.hltln, command=self.toggle_highlight)
		#self.viewmenu.add_checkbutton(label='Color syntax',variable=self.clrsyntx, command=self.syntax_highlight)
		self.clrsyntx.set(1)
		self.themesmenu = tk.Menu(self.viewmenu,tearoff=0)
		self.viewmenu.add_cascade(label='Themes', menu=self.themesmenu)
		self.themechoice.set('Default White')
		for k in sorted(self.clrschemes):
			self.themesmenu.add_radiobutton(label=k, variable=self.themechoice, command=self.theme)

		self.helpmenu = tk.Menu(self.menubar, tearoff = 0)
		self.menubar.add_cascade(label='Help',menu=self.helpmenu)
		self.helpmenu.add_command(label='About', command=self.about)
		self.helpmenu.add_command(label='Help',command=self.help_box)

		#Labels
		self.shortcutbar =tk.Frame(top, height=25, bg='grey')
		icons = ['new_file', 'open_file', 'save_file', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find']
		for i, icon in enumerate(icons):
			tbicon = tk.PhotoImage(file='icons/32/'+icon+'.png')
			cmd = eval('self.'+icon)
			self.toolbar = tk.Button(self.shortcutbar, image=tbicon, command=cmd)
			self.toolbar.image = tbicon
			self.toolbar.pack(side=tk.LEFT)
		self.shortcutbar.pack(expand='no',fill=tk.X)
		self.lnlabel = tk.Label(top, width=3, bg = 'grey')
		self.lnlabel.pack(expand='no',side=tk.LEFT, anchor='nw', fill=tk.Y)
		#Text and scroll
		self.textpad = tk.Text(top, undo=True)
		self.textpad.pack(expand='yes',fill=tk.BOTH)
		self.scroll = tk.Scrollbar(self.textpad)
		self.textpad.configure(yscrollcommand=self.scroll.set)
		self.scroll.config(command=self.textpad.yview)
		self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
		#Info Bar
		self.infobar = tk.Label(self.textpad)
		self.infobar.pack(expand='no', fill=None, side=tk.RIGHT, anchor='se')
		self.theme()
		#context menu
		self.cmenu = tk.Menu(self.textpad, tearoff=0)
		for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
			cm = 'self.'+i
			cmd = eval(cm)
			self.cmenu.add_command(label=i, compound=tk.LEFT, command=cm)
		self.cmenu.add_separator()
		self.cmenu.add_command(label='Select All', underline=7, command=self.select_all)
		#Bindings
		self.textpad.bind('<Button-3>', self.popup)
		self.textpad.bind('<Any-KeyPress>', self.update_line_number)
		self.textpad.bind('<Control-N>',self.new_file)
		self.textpad.bind('<Control-n>', self.new_file)
		self.textpad.bind('<Control-o>', self.open_file)
		self.textpad.bind('<Control-O>', self.open_file)
		self.textpad.bind('<Control-S>', self.save_file)
		self.textpad.bind('<Control-s>', self.save_file)
		self.textpad.bind('<Control-A>', self.select_all)
		self.textpad.bind('<Control-a>', self.select_all)
		self.textpad.bind('<Control-f>', self.on_find)
		self.textpad.bind('<Control-F>', self.on_find)
		self.textpad.bind('<KeyPress-F1>', self.help_box)

	def about(self, event=None):
		global version
		msg = 'PyEdit '+str(version)+'\nby Vishwas K Singh\
				\ncontact:vishwasks32@gmail.com'
		tkmb.showinfo("About",msg)

	def exit_editor(self, event=None):
			#print len(self.textpad.get(1.0, tk.END))
			if len(self.textpad.get(1.0, tk.END)) > 1: 
				if tkmb.askquestion("Save", "Do you want to save?")=='yes':
					self.save_file()
					self.master.destroy()
				else:
					self.master.destroy()
			else:
				if tkmb.askokcancel("Quit", "Do you really want to quit?"):
					self.master.destroy()

	def update_line_number(self,event=None):
		txt = ''
		if self.showln.get():
			endline, endcolumn = self.textpad.index('end-1c').split('.')
			txt = '\n'.join(map(str, range(1, int(endline)+1)))

		else:	
			endline, endcolumn = self.textpad.index('end-1c').split('.')
			txt = ''
		self.lnlabel.config(text=txt, anchor='nw')

		if self.showinfo.get():
			currline, currcolumn = self.textpad.index("insert").split('.')
			self.infobar.config(text= 'Line: %s | column: %s' %(currline, currcolumn))
			self.infobar.pack(expand='no', fill=None, side=tk.RIGHT, anchor='se')

		else:
			self.infobar.pack_forget()

	

	def cut(self):
		self.textpad.event_generate("<<Cut>>")
		self.update_line_number()

	def copy(self):
		self.textpad.event_generate("<<Copy>>")
		self.update_line_number()

	def paste(self):
		self.textpad.event_generate("<<Paste>>")
		self.update_line_number()

	def undo(self):
		self.textpad.event_generate("<<Undo>>")
		self.update_line_number()

	def redo(self):
		self.textpad.event_generate("<<Redo>>")
		self.update_line_number()

	def select_all(self,event=None):
		self.textpad.tag_add('sel', 1.0, 'end')
		

        def on_find(self,event=None):
		self.t2 = tk.Toplevel(self)
                self.t2.title('Find & Replace')
                self.t2.transient(self)
		v = tk.StringVar()

                tk.Label(self.t2, text="Find:").grid(row=0, column=0, sticky='e')
                e = tk.Entry(self.t2, textvariable=v).grid(row=0, column=1, columnspan=9, padx=2, pady=2, sticky='we')

                tk.Button(self.t2, text="Find").grid(row=0, column=10, sticky='ew', padx=2, pady=2)
                c =tk.BooleanVar()
		tk.Checkbutton(self.t2, text='Ignore case',variable=c).grid(row=3, column=1, columnspan=4, sticky='w')
                tk.Button(self.t2, text="Find All",command=lambda:self.search_for(v.get(), c.get(),self.textpad,self.t2,e)).grid(row=0, column=10, sticky='ew', padx=2, pady=2)
		

	        def close_search():
			self.textpad.tag_remove('match', 1.0, tk.END)
		        self.t2.destroy()

	        self.t2.protocol('WM_DELETE_WINDOW', close_search)
	
	def search_for(self,needle,cssntv,textpad,t2,e):
		textpad.tag_remove('match', 1.0, tk.END)
		count=0
		if needle:
			pos = '1.0'
			while True:
				pos = textpad.search(needle, pos, nocase = cssntv, stopindex=tk.END)
				if not pos: break
				lastpos = '%s + %dc' %(pos, len(needle))
				textpad.tag_add('match', pos, lastpos)
				count += 1
				pos = lastpos

		textpad.tag_config('match', foreground='red', background='yellow')
		t2.title('%d matches found' %count)

	def open_file(self,event=None):
		global filename
		if len(self.textpad.get(1.0, tk.END)) > 1:
			if tkmb.askquestion("Save", "Do you want to save?"):
				self.save_file()
			
		
		filename = tkfd.askopenfilename(defaultextension=".txt", filetypes = [("All Files", "*.*"),("Text Documents", "*.txt"),('Python Files', '*.py')])
		if filename == "":
			filename = None
		else:
			self.master.title("PyEdit - "+os.path.basename(filename))
			self.textpad.delete(1.0, tk.END)
			fh = open(filename, "r")
			self.textpad.insert(1.0, fh.read())
			fh.close()
		self.update_line_number()


	def save_file(self,event=None):
		global filename
		try:
			f = open(filename, 'w')
			letter = self.textpad.get(1.0, 'end')
			f.write(letter)
			f.close()
		except:
			self.save_as()
		

	def save_as(self):
		try:
			f = tkfd.asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt", \
					filetypes = [("All Files", "*.*"), ("Text Documents", "*.txt"), ('Python Files', '*.py')])
			fh = open(f, 'w')
			textoutput = self.textpad.get(1.0, tk.END)
			fh.write(textoutput)
			fh.close()
			self.master.title("PyEdit - ",os.path.basename(f))
		except:
			pass
		

	def new_file(self,event=None):
		if len(self.textpad.get(1.0, tk. END)) > 1:
			self.save_file()

		self.master.title("PyEdit - Untitled")
		global filename
		filename = None
		self.textpad.delete(1.0, tk.END)
		self.update_line_number()

	def help_box(self, event=None):
		tkmb.showinfo("Help",' For help refer to book:\n\
				Tkinter GUI Application\n of Development', icon='question')

	def toggle_highlight(self,event=None):
		val = self.hltln.get()
		if val==1:
			self.textpad.tag_remove("active_line", 1.0, "end")
			self.textpad.tag_config('active_line', foreground='red', background='yellow')
			self.textpad.tag_add("active_line", "insert linestart", "insert lineend+1c")
			self.textpad.after(100,self.toggle_highlight)
		else:

			self.textpad.tag_config('active_line', foreground='', background='')
			self.textpad.tag_remove("active line", 'insert linestart', "insert lineend+1c")

	def theme(self, event=None):
		global bgc,fgc
		val = self.themechoice.get()
		clrs = self.clrschemes.get(val)
		fgc, bgc = clrs.split('.')
		fgc, bgc = '#'+fgc, '#'+bgc
		self.textpad.config(bg=bgc, fg=fgc)

	def popup(self, event=None):
		self.cmenu.tk_popup(event.x_root, event.y_root, 0)

	def highlight(self, event=None):
		endline, endcolumn = self.textpad.index('end-1c').split('.')





