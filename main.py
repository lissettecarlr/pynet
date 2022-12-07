import os,time,sys
import yaml
from loguru import logger
import mqttClient
import keyboard
import messageBox


def netStatusCb(sta):
    logger.info(sta)

def mqttTest():
    with open("./testConfig.yaml") as config:
        cfg = yaml.safe_load(config)
    netTask = mqttClient.mqttClient(
        cfg["mqtt"]["serverName"],
        cfg["mqtt"]["serverPassword"],
        cfg["mqtt"]["serverIp"],
        cfg["mqtt"]["serverPort"],
        cfg["mqtt"]["id"],
        cfg["mqtt"]["reciveTopic"],
    )
    box = messageBox.messageBox()
    netTask.setCallback(netStatusCb,box.input)
    netTask.start()

    try:
        while(1):
            if keyboard.is_pressed('q'): 
                netTask.close()
                break
            time.sleep(5)
    except:
        netTask.close()


if __name__ == "__main__":
    mqttTest()





# 测试
# qmdr/faceRecognition/test/fzj/faceLib/input
# {
#  "nameList":[{"group":"qmdr","name":"测试","url":"https://ldetapp-1253134232.cos.ap-chengdu.myqcloud.com/fba42b17-15e3-4493-8c49-ac74ca8d762atmp_146a6a001a73eb50366343780f672cb1131261c0bda140bc.jpg","id":"1"}], 
#  "msgId":"123123"
# }

# qmdr/faceRecognition/test/fzj/faceLib/delete/people
# {
#     "nameList":[{"group":"qmdr","name":"测试"}] ,
#     "msgId":"2"
# }

#  qmdr/faceRecognition/test/fzj/faceLib/delete/img
# {
#     "nameList":[{"group":"qmdr","name":"测试","id":"2"}] ,
#     "msgId":""
# }

# qmdr/faceRecognition/test/fzj/faceLib/getLib
# {
# 	"group":"all",
#   "msgId":"444"
# }

# qmdr/faceRecognition/test/fzj/faceLib/build
# {
#     "msgId":"555",
# 	"group":["qmdr"] 
# }

# qmdr/faceRecognition/test/fzj/faceLib/getFaceLibBin

# qmdr/faceRecognition/test/fzj/recognition/loadFaceLibBin 
# {
#     "msgId":"55",
#     "faceLibBin":"facelib.bin"
# }
# qmdr/faceRecognition/test/fzj/recognition/video
# {
#     "url":"https://web-printer.oss-cn-chengdu.aliyuncs.com/fr/test.mp4",
#     "msgId":"123",
# }


# 15:21:04
#    22:38

   