# 此文件只用于收发

import threading
from loguru import logger
import time
import json
import paho.mqtt.client as mqtt
import random

class mqttClient(threading.Thread):
    def __init__(self,serverName="",serverPassword="",serverIp="",serverPort=1884,mqttId="",TopicHead=""):
        threading.Thread.__init__(self)
        
        self.netChangeCb = None
        self.flag = True
        #当前连接状态
        self.connectStatus = False
        
        # 连接服务器参数设置
        self.mqttServerName = serverName
        self.mqttServerPassword = serverPassword
        if(serverIp == ""):
            logger.error("not input serverIp")
            return None
        else:
            self.mqttServerIp = serverIp
        self.mqttServerPort = serverPort
        if(mqttId == ""):
            self.mqttId = "kala" + str(random.randint(1000,9999))
            logger.warning("not input mqttId,id = {}".format(self.mqttId))
        else:
            self.mqttId = mqttId

        if(TopicHead == ""):
            self.reciveTopic = "qmdr/unkonwn/test/" + self.mqttId+ "/#"
        else:
            self.reciveTopic = TopicHead + self.mqttId+ "/#"

        self.netChangeCb = None
        self.reciveMsgCallback = None

        self.init()

    def init(self):
        self.client = mqtt.Client(client_id=self.mqttId,clean_session=False)
        self.client.on_connect = self.connectCb
        self.client.on_message = self.messageCb
        self.client.on_disconnect = self.disconnectCb
        self.client.on_publish = self.publishCb
        self.client.on_subscribe = self.subscribeCb
        # self.client.on_unsubscribe = self.on_unsubscribe

        # 如果MQTT有账号密码
        if(self.mqttServerName != ""):
            self.client.username_pw_set(self.mqttServerName, self.mqttServerPassword)
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)
 

    def connect(self):
        try:
            self.client.connect(self.mqttServerIp, self.mqttServerPort, 60)  # 60为keepalive的时间间隔
        except:
            #会自动重连
            logger.warning("mqtt连接失败")

    def run(self):
        logger.info("网络通讯线程启动")
        while 1:
            self.connect()
            try:
                self.client.loop_forever()
            except KeyboardInterrupt:
                self.client.disconnect()
                return None

            time.sleep(3)
            if(self.flag == False):
                break

    def close(self):
        self.client.disconnect()
        self.flag = False
        logger.info("网络通讯线程退出")

    def getNetStatus(self):
        return self.connectStatus

    # 连接回调
    def connectCb(self,client, userdata, flags, rc):
        if(rc == 0):
            logger.info("MQTT连接建立：{}".format(self.mqttId))
            self.connectStatus = True
            if(self.netChangeCb):
                self.netChangeCb(self.connectStatus)

            logger.info("订阅主题：{}".format(self.reciveTopic))    
            self.client.subscribe([
                (self.reciveTopic, 0),
                #("qmdr/faceRecognition/test/"+self.mqttId+"/#", 0),
               ])
        else:
            # 1协议版本不正确  2客户端标识符无效 3服务器不可用 4用户名或密码错误 5未授权
            logger.info("MQTT连接被拒绝 {}".format(rc))
            
        #print("Connected with result code: " + str(rc))
    #连接断开回调 rc参数表示断开状态
    def disconnectCb(self,client, userdata, rc):
        logger.info("MQTT连接断开 {}".format(rc))
        self.connectStatus = False
        if(self.netChangeCb):
            self.netChangeCb(self.connectStatus)

    def messageCb(self,client, userdata, message):
        print(message.topic)
        print(message.payload)
        if(message.topic.find("ack") != -1):
            return None
        #res = self.rtask.taskInput(message.topic,message.payload.decode('utf-8'))
        if(self.reciveMsgCallback != None):
            res = self.reciveMsgCallback(message.topic,message.payload.decode('utf-8'))
            if(res != None):
                ackJson = json.dumps(res, ensure_ascii=False)
                if(self.connectStatus == True):
                    self.client.publish(message.topic+"/ack",ackJson)
        else:
            logger.debug("接收消息：{}".format(message.topic,message.payload.decode('utf-8')))
     

    #消息发送成功后的回调
    #对于Qos级别为1和2的消息，这意味着已经完成了与代理的握手。
    #对于Qos级别为0的消息，这只意味着消息离开了客户端。
    #mid变量与从相应的publish()返回的mid变量匹配
    def publishCb(self,client, userdata, mid):
        pass

    # 发送客户端状态
    def publishStatus(self,sta):
        # qmdr/faceRecognition/prod/xxx/status
        pass

    #网络状态变化回调、数据接收回调
    def setCallback(self,netChange=None,reciveMsgCallback=None):
        self.netChangeCb = netChange
        self.reciveMsgCallback = reciveMsgCallback
        
    #订阅主题后的回调
    #mid变量匹配从相应的subscri be()返回的mid变量
    def subscribeCb(self,client, userdata, mid, granted_qos):
        logger.debug("Subscribed: {} , {}".format(str(mid),str(granted_qos)))


