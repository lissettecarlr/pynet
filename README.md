# pynet
python的网络通信模板，V010

## 环境
```
pip install pyyaml
pip loguru
pip install paho-mqtt
```

## 测试
修改config.yaml，设置自己的mqtt服务器
启动
```
python main.py
```
然后使用mqtt客户端发送
主题：unknown/test/test/task2
```
"url":"https://123.jpg",
"msgId":"123"
```

## 使用
* 将pynet扔进工程中，修改config.yaml服务器配置。
* 修改messageBox.py，作为接收命令处理，例如引入
```
sys.path.append("..") 
from app.actionDetection import actionDetection
from net.utils import download
```
* 主函数
```
from net.mqttClient import mqttClient
from net.messageBox import messageBox

netTask = mqttClient.mqttClient()
box = messageBox.messageBox()
netTask.setCallback(netStatusCb,box.input)
netTask.start()
```

## 其他

### yaml
* 大小写敏感
* 使用缩进表示层级关系
* 缩进时不允许使用Tab键，只允许使用空格。
* 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
* #表示注释，从这个字符一直到行尾，都会被解析器忽略，这个和python的注释一样
