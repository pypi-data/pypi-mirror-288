import json
import os
defaultConfig = {
    "userdataDir": "",#数据目录
    "path": "", #浏览器路径
    "extensions": [], #默认插件列表
    "httpport": 6211,  #http端口
    "jscode": "console.log(1)", #默认js代码
}

def setJscode(jscode):
    defaultConfig["jscode"] = jscode
    saveFile()

def saveFile():
    with open("config.json", "w") as f:
        json.dump(defaultConfig, f)

def setUserdataDir(path):
    defaultConfig["userdataDir"] = path
    saveFile()

def setPath(path):
    # 判断路径是否存在,不存在就创建
    if not os.path.exists(path):
        os.makedirs(path)
        print("创建目录:", path)
    defaultConfig["path"] = path
    saveFile()

def setExtensions(extensions):
    defaultConfig["extensions"] = extensions
    saveFile()

def setHttpport(port):
    defaultConfig["httpport"] = port
    saveFile()

def getConfig():
    return defaultConfig

