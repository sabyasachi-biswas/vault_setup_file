import tkinter.filedialog as filedialog

def encrypt(file,key):
    try:

        path = file
        fin = open(path, 'rb')
        file_array = fin.read()
        fin.close()
        file_array = bytearray(file_array)
    
        for index, values in enumerate(file_array):
            file_array[index] = values ^ key
    
        fin = open(path, 'wb')
        fin.write(file_array)
        fin.close()

        print("Encryption Done")
        
    except Exception:
        print('Error caught : ', Exception.__name__)

def decrypt(file,key):
    try:
        path = file
        fin = open(path, 'rb')
        file_array = fin.read()
        fin.close()
        file_array = bytearray(file_array)

        for index, values in enumerate(file_array):
            file_array[index] = values ^ key

        fin = open(path, 'wb')
        fin.write(file_array)
        fin.close()
        print("Decryption done")
        
    except Exception:
        print('Error caught : ', Exception.__name__)

