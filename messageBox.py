# 本文将仅解析传入的指令

from loguru import logger
import json
import os
import random
import utils


class messageBox:
    def __init__(self):
        self.taskList={
            "task1":"task1",
            "task2":"task2",
        }      
        self.downLoadPath = "./downloadTemp"
        if not os.path.isdir(self.downLoadPath):
            os.mkdir(self.downLoadPath)
    # 输入类别词与实际消息，类别词用于区分任务类型，实际消息为json格式    
    def input(self,key,msg):
        try:
            resp = json.loads(msg)
        except:
            logger.warning("格式错误")
            return None
        # 标准应答    
        res = {"result":"","contents":"","msgId":""} 

        # 根据任务分类处理，以下为示例
        if(key.find(self.taskList["task1"]) != -1):
            logger.debug("任务1")
            res["result"] = "fail"
            try:
                nameList = resp["nameList"]
                res["msgId"] = resp["msgId"]
            except:
                res["contents"]= "字段错误" 
                return res

            nameNum = len(nameList)
            logger.info("需要添加{}人".format(nameNum))
            if(nameNum == 0):
                res["result"] = "fail"
                res["contents"] = "no people"
                return res
           
            failList = ["123","456"]
      
            if(failList == []):
                res["result"] = "fail"
                res["contents"] = "input fail"
            else:
                logger.info("成功添加：{}".format(failList))
                res["result"] = "succeed"
                res["contents"] = str(failList)
            return res
        

        elif(key.find(self.taskList["task2"]) != -1):
            logger.info("识别图片")
            res["result"] = "fail"
            try:
                res["msgId"] = resp["msgId"]
                imgUrl = resp["url"]
            except:
                logger.warning("字段错误")
                res["contents"]= "json error" 
                return res
            # 首先检测url格式
            if((imgUrl.endswith(".jpg")==False and imgUrl.endswith(".png")==False)):
                logger.warning("url后缀错误")
                res["contents"]= "url error" 
                return res

            fileName = imgUrl[ imgUrl.rindex( '/' ) + 1 : len( imgUrl ) ]
            fileName = "downloadTask_" + str(random.randint(1000,9999)) + fileName
            #图片缓存本地，命名方式为url
            if(utils.download(imgUrl, self.downLoadPath, fileName) == False):
                res["contents"]= "download error"
                return res

            tempImg = os.path.join(self.downLoadPath,fileName)
            #inferName = self.rec.recognition(tempImg)
            inferName = ["123"]
            logger.info("识别结果：{}".format(inferName))
            if(inferName == False):
                res["result"] = "fail"
            else:
                res["result"] = "succeed"
                res["contents"]= inferName 
    
            os.remove(tempImg)
            return res
        else:
            logger.info("未设定主题")