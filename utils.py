import os
import requests
import pickle

def listSaveOrRead(path,mode="read",arg=None):
    if(mode == "save"):
        if(arg == None):
            return False
        with open(path, "wb") as f:
            pickle.dump(arg, f)
        return True

    elif(mode == "read"):
        if(os.path.isfile(path) ==False):
            print("此地址文件不存在{}".format(path)) 
            return False
        with open(path, "rb") as f:
            rdlist = pickle.load(f)
        return rdlist


def download(downloadURL,downloadPath,name):
    """ 进行下载请求 """
    try:
        headers = {'content-type': "application/octet-stream",}
        re = requests.get(downloadURL,headers = headers,timeout=10)
        with open(downloadPath +"\\"+ name , "wb") as code:
            code.write(re.content)
            code.close()
            #print("下载完成{}".format(name))
            return True
    except:
        print("下载请求失败")
        return False