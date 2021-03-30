from tkinter import Tk, Text, BOTH, W, N, E, S, ttk
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter.ttk import Frame, Button, Style
import tkinter.filedialog as filedialog
import filetype_module
import encryption_module
import sqlite3
import shutil
import os


class Example(Frame):

    def __init__(self,uid):
        super().__init__()
        self.uid=uid
        self.initUI()
        


    def initUI(self):
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        
        self.master.geometry(f'{680}x{800}')
        self.master.resizable(False,False)
        self.master.title("Vault")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        # 
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
     
        # area = Text(self)
        # area.grid(row=1, column=0, columnspan=2, rowspan=4,
        #     padx=5, sticky=E+W+S+N)

        lbl = Label(self, text="Encrypted")
        lbl.grid(row = 0,column = 0,sticky=W, pady=10, padx=5)

        


        self.treev_encrypt = ttk.Treeview(self,height = 15, selectmode = "browse")
        self.treev_encrypt.grid(row = 1, column = 0,columnspan=2, rowspan=4,padx=5,pady=5,sticky=E+W+S+N)

        lbl = Label(self, text="Decrypted")
        lbl.grid(row = 5,column = 0,sticky=W, pady=4, padx=5)

        self.treev_decrypt = ttk.Treeview(self,height = 15, selectmode = "browse")
        self.treev_decrypt.grid(row = 6, column = 0,columnspan=2, rowspan=4,padx=5,pady=5,sticky=E+W+S+N)

        btn_addfile = Button(self, text="Add File",command = self.addfile)
        btn_addfile.grid(row=1, column=5, pady=5,padx = 10)

        abtn = Button(self, text="Encrypt",command = self.encrypt)
        abtn.grid(row=2, column=5, pady=10,padx = 10)

        btn_decrypt = Button(self, text="Decrypt",command = self.decrypt)
        btn_decrypt.grid(row=3, column=5, pady=10,padx = 10,sticky=N)

        btn_export = Button(self, text="Export",command = self.export)
        btn_export.grid(row=4, column=5, pady=10,padx = 10)
        
            
        hbtn = Button(self, text="Refresh",command = self.refresh)
        hbtn.grid(row=10, column=0, pady=10,padx = 2)

        obtn = Button(self, text="View",command = self.view)
        obtn.grid(row=10, column=5, pady=10,padx = 10)


        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT name FROM user WHERE uid=(:uid)",
        {
            'uid': self.uid
        })
        local_name = c.fetchone()
        conn.commit()
        conn.close()
        lbl = Label(self, text="USER:")
        lbl.grid(sticky=W)
        lbl_user = Label(self, text="USERNAME",font=(25),fg="green")
        lbl_user.configure(text=local_name[0])
        lbl_user.grid(sticky=W)

        self.refresh_decrypt()
        self.refresh_encrypt()
        # self.refresh()

    def view(self):
        try:
            Item = self.treev_decrypt.focus()
            localval = self.treev_decrypt.item(Item, 'values')
        except IndexError:
            print("Please select Decrypt")
        
        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT path FROM vault_data WHERE fileid=(:fileid)",{
            'fileid':localval[0]
        })
        path = c.fetchone()
        c.execute("SELECT filetype FROM vault_data WHERE fileid=(:fileid)",{
            'fileid':localval[0]
        })
        filetype = c.fetchone()
        conn.commit()
        conn.close()

        view_window = Toplevel(self)
        # label = Label(view_window, text = "").pack()
        if (filetype[0] == "Image"):
            file = open(path[0],"rb")
            self.Img = ImageTk.PhotoImage(PIL.Image.open(file))
            label = Label(view_window, image = self.Img)
            label.pack()
        else:
            file = open(path[0],"r")
            self.textval = file.read()
            label = Label(view_window,text="Text")
            label.configure(text=self.textval)
            label.pack()

    def refresh(self):
        self.refresh_decrypt()
        self.refresh_encrypt()

    def decrypt(self):
        
        try:
            Item = self.treev_encrypt.focus()
            localval = self.treev_encrypt.item(Item, 'values')
        except IndexError:
            print("Please select something")

        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT algo FROM vault_data where fileid=(:fileid)",{
            'fileid' : localval[0]
        })
        algorithm=c.fetchone()
        
        local_state = "Decrypted"
        algo = "none"
        c.execute("UPDATE vault_data SET state=(:local_state),algo=(:algo) WHERE fileid=(:fileid)",{
            'local_state': local_state,
            'algo' : algo,
            'fileid' : localval[0]
        })
        c.execute("SELECT path FROM vault_data where fileid=(:fileid)",{
            'fileid' : localval[0]
        })
        path=c.fetchone()
        encryption_module.passcontroldecrypt(localval[0],self.uid,algorithm[0],path[0])
        conn.commit()
        conn.close()

        self.refresh_decrypt()
        self.refresh_encrypt()

    def refresh_decrypt(self):
        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()

        # To avoid duplicate values in treeview
        for record in self.treev_decrypt.get_children():
            self.treev_decrypt.delete(record)

        self.treev_decrypt["columns"] = ("1", "2", "3","4")
        self.treev_decrypt['show'] = 'headings'

        self.treev_decrypt.column("1", width = 70, anchor='c')
        self.treev_decrypt.column("2", width = 355)
        self.treev_decrypt.column("3", width = 80)
        self.treev_decrypt.column("4", width = 80,anchor='c')

        self.treev_decrypt.heading("1", text ="File ID") 
        self.treev_decrypt.heading("2", text ="File") 
        self.treev_decrypt.heading("3", text ="Size (KB)")
        self.treev_decrypt.heading("4", text ="Type")

        state="Decrypted"

        c.execute("SELECT fileid FROM vault_data where uid=(:uid)  AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        fileid=c.fetchall()
        c.execute("SELECT filename FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filename=c.fetchall()
        c.execute("SELECT filesize FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filesize=c.fetchall()
        c.execute("SELECT filetype FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filetype=c.fetchall()
        c.execute("SELECT COUNT(*) FROM vault_data where state=(:state) AND uid=(:uid)",{
            'state' : state,
            'uid' : self.uid
        })
        count=c.fetchone()

        for i in range(0,count[0]):
            local_filename = filename[i]
            dummy_filesize = filesize[i]
            local_filesize = dummy_filesize[0]/1024
            self.treev_decrypt.insert("", 'end', text ="L1",  
                    values =(fileid[i], local_filename[0],  round(local_filesize,2), filetype[i]))

        conn.commit()
        conn.close()

    def addfile(self):
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        #-----Moving File-----------
        c.execute("SELECT path FROM vault_path")
        dest_path = c.fetchone()
        #---------------------------
        self.addfilename = filedialog.askopenfilename()

        filetype=filetype_module.checkfile(self.addfilename)
        filename=filetype_module.filename(self.addfilename)
        filesize=filetype_module.filesize(self.addfilename)


        shutil.move(self.addfilename,dest_path[0])
        filepath = os.path.join(dest_path[0],filename)

        state="Decrypted"
        algo="none"
        c.execute("INSERT INTO vault_data (uid, state, algo, filename, filesize, path, filetype) VALUES (:uid,:state,:algo,:filename,:filesize,:path,:filetype)",{
            'uid' : self.uid,
            'state' : state,
            'algo' : algo,
            'filename' : filename,
            'filesize' : filesize,
            'path' : filepath,
            'filetype' : filetype
        })

        conn.commit()
        conn.close()

        self.refresh_decrypt()

    def encrypt(self):
        encrypt_window = Toplevel(self)
        encrypt_window.geometry("270x200")
        encrypt_window.title("Encrypt")
        label = Label(encrypt_window,text="Note: Only XOR encryption is available for Images").grid()
        # list = ["AES-128","AES-192","AES-256","RSA"]
        self.value=StringVar()
        combobox = ttk.Combobox(encrypt_window,textvariable=self.value,state='readonly')
        combobox['values'] = ('XOR','RSA','DES')
        combobox.current(0)
        combobox.grid(pady = 10,padx = 10)
        button=Button(encrypt_window,text="OK",command=self.enable_encrypt).grid()
        
    def enable_encrypt(self):
        algorithm = self.value.get()
        try:
            Item = self.treev_decrypt.focus()
            localval = self.treev_decrypt.item(Item, 'values')
        except IndexError:
            print("Please select something")

        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()
        local_state = "Encrypted"
        c.execute("UPDATE vault_data SET state=(:local_state),algo=(:algo) WHERE fileid=(:fileid)",{
            'local_state': local_state,
            'algo' : algorithm,
            'fileid' : localval[0]
        })
        c.execute("SELECT path FROM vault_data where fileid=(:fileid)",{
            'fileid' : localval[0]
        })
        path=c.fetchone()
        encryption_module.passcontrolencrypt(localval[0],self.uid,algorithm,path[0])
        conn.commit()
        conn.close()

        self.refresh_decrypt()
        self.refresh_encrypt()

    def refresh_encrypt(self):
        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()

        # To avoid duplicate values in treeview
        for record in self.treev_encrypt.get_children():
            self.treev_encrypt.delete(record)

        self.treev_encrypt["columns"] = ("1", "2", "3","4","5")
        self.treev_encrypt['show'] = 'headings'

        self.treev_encrypt.column("1", width = 70, anchor='c')
        self.treev_encrypt.column("2", width = 300)
        self.treev_encrypt.column("3", width = 70)
        self.treev_encrypt.column("4", width = 70)
        self.treev_encrypt.column("5", width = 70,anchor='c')

        self.treev_encrypt.heading("1", text ="File ID") 
        self.treev_encrypt.heading("2", text ="File") 
        self.treev_encrypt.heading("3", text ="Size (KB)")
        self.treev_encrypt.heading("4", text ="Type")
        self.treev_encrypt.heading("5", text ="Algorithm")

        # self.treev_encrypt.column("1", anchor='c')
        

        state="Encrypted"

        c.execute("SELECT fileid FROM vault_data where uid=(:uid)  AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        fileid=c.fetchall()
        c.execute("SELECT filename FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filename=c.fetchall()
        c.execute("SELECT filesize FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filesize=c.fetchall()
        c.execute("SELECT filetype FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        filetype=c.fetchall()
        c.execute("SELECT algo FROM vault_data where uid=(:uid) AND state=(:state)",{
            'uid' : self.uid,
            'state' : state
        })
        algo=c.fetchall()
        
        c.execute("SELECT COUNT(*) FROM vault_data where state=(:state)",{
            'state' : state
        })
        count=c.fetchone()

        for i in range(0,count[0]):
            local_filename = filename[i]
            dummy_filesize = filesize[i]
            local_filesize = dummy_filesize[0]/1024
            self.treev_encrypt.insert("", 'end', text ="L1",  
                    values =(fileid[i], local_filename[0],  round(local_filesize,2), filetype[i], algo[i]))

        conn.commit()
        conn.close()

    def export(self):
        try:
            Item = self.treev_decrypt.focus()
            localval = self.treev_decrypt.item(Item, 'values')
        except IndexError:
            print("Please select something")

        conn=sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("SELECT path FROM vault_data WHERE fileid=(:fileid)",{
            'fileid' : localval[0]
        })
        path = c.fetchone()
        

        dest_path = filedialog.askdirectory()
        shutil.move(path[0],dest_path)

        c.execute("DELETE FROM vault_data WHERE fileid=(:fileid)",{
            'fileid' : localval[0]
        })
        conn.commit()
        conn.close()
        
        self.refresh()


def start(uid):

    root = Tk()
    app = Example(uid)
    root.mainloop()

# start(1)