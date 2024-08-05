import time
from config import setHttpport,getConfig,setUserdataDir,setPath,setExtensions,setJscode
from browser import createBrowser,browsers
from httpserver import startHttpServer
import threading
import os
import json
forcerun = False 
def doTask(name   ):
    new_thread = None
    def task(): 
        page = None
        browser = createBrowser(name=name)
        run = True
   
        while run:
            try:
                time.sleep(2)
                 
    
                page = browser.page

                page.run_js('window.__ping__ = (Date.now())')
                
            except Exception as e:
                if forcerun == False:
                    os._exit(0)
                browser = createBrowser(name=name)
                if browser:
                    page = browser.page
                    print(e)

                    
    new_thread = threading.Thread(target=task) 
    new_thread.start()
    return True


 

def init(**args):
    # 判断zuds目录是否存在
    if args.get('path', None) is not None:
        print('设置路径', args.get('path', None))
        setPath(args.get('path'))
    if args.get('userdataDir', None) is not None:
        setUserdataDir(args.get('userdataDir'))
    if args.get('extensions', None) is not None:
        setExtensions(args.get('extensions'))
    if args.get('httpport', None) is not None:
        setHttpport(args.get('httpport'))
    if args.get('forcerun', None) is not None:
        forcerun = args.get('forcerun')
        if forcerun == True:
            print('自动运行')
    # jscode
    jscode = args.get('jscode', None)
    if jscode is not None:
        setJscode(jscode)

def start(startCount = 1):
    for i in range(startCount):
        name = 'browser_'+str(i+1) 
        doTask(name)
    startHttpServer()

    