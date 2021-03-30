import tkinter.filedialog as filedialog

class keygen:

    def genkey(self,number):
        count=1
        if count <= 2:
            for num in range(number+100,number+200):  
                if num > 1:  
                    for i in range(2,num):  
                        if (num % i) == 0:  
                            break  
                    else:
                        if count == 1:
                            self.p = num
                        if count == 2:
                            self.q = num
                        count += 1
        p=self.p
        q=self.q
        n=p*q
        # print("N is",n)
        phi = (p-1)*(q-1)



        def gcd(p,q):
            while q != 0:
                p, q = q, p%q
            return p
        def is_coprime(x, y):
            if gcd(x, y) == 1:
                return x
        list=[]
        for i in range (2,phi):
            if is_coprime(i,phi) != None:
                list.append(is_coprime(i,phi))
        e=list[len(list)-2]



        for k in range (0,e):
            d=(1+(k*phi))/e
            if d.is_integer():
                self.d=int(d)
                self.e=e
                self.n=n


def encrypt(input_string,number):
    obj = keygen()
    obj.genkey(number)
    n=obj.n
    e=obj.e
    str1=''
    ASCII_values = []
    cypher_list = []
    ASCII_values.clear()
    cypher_list.clear()
    
    for character in input_string:
        ASCII_values.append(ord(character))
    for m in ASCII_values:
        c=(m**e)%n
        cypher_list.append(c)
    for i in cypher_list:
        str1=str1+chr(i)
    # print(str1)
    return(str1)

def decrypt(input_string,number):
    obj = keygen()
    obj.genkey(number)
    d=obj.d
    n=obj.n
    str=''
    ASCII_values = []
    message_list = []
    ASCII_values.clear()
    message_list.clear()
    for character in input_string:
        ASCII_values.append(ord(character))
    for m in ASCII_values:
        message=(m**d)%n
        message_list.append(message)
    for i in message_list:
        str=str+chr(i)
    # print(str)
    return(str)