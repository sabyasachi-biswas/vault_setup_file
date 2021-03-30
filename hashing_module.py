import bcrypt

def hashpwd(password):
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash

def checkpwd(entered_pwd,password):
    if bcrypt.checkpw(entered_pwd,password):
        return True
    else:
        return False