import xor_module
import rsa_text
import des_text
from tkinter import filedialog

def passcontrolencrypt(fileid,uid,algo,path):
    # print(fileid,uid,algo,path)
    if algo == "XOR":
        xor_module.encrypt(path,int(uid)+int(fileid))
    if algo == "RSA":
        inputmsg=open(path,"r",encoding='utf-8')
        stringinput=inputmsg.read()
        cipher=rsa_text.encrypt(stringinput,int(fileid)+int(uid))
        filewrite=open(path,"w",encoding="utf-8")
        filewrite.write(cipher)
    if algo == "DES":
        inputmsg=open(path,"r",encoding='utf-8')
        stringinput=inputmsg.read()
        cipher=des_text.des_encrypyt(stringinput,int(fileid)+int(uid))
        filewrite=open(path,"w",encoding="utf-8")
        filewrite.write(cipher)
    
def passcontroldecrypt(fileid,uid,algo,path):
    if algo == "XOR":
        xor_module.decrypt(path,int(uid)+int(fileid))
    if algo == "RSA":
        inputmsg=open(path,"r",encoding='utf-8')
        stringinput=inputmsg.read()
        plaintext=rsa_text.decrypt(stringinput,int(fileid)+int(uid))
        filewrite=open(path,"w",encoding="utf-8")
        filewrite.write(plaintext)
    if algo == "DES":
        inputmsg=open(path,"r",encoding='utf-8')
        stringinput=inputmsg.read()
        plaintext=des_text.des_decrypyt(stringinput,int(fileid)+int(uid))
        filewrite=open(path,"w",encoding="utf-8")
        filewrite.write(plaintext)