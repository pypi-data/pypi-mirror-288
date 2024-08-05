import random
from DrissionPage import ChromiumPage, ChromiumOptions,errors # type: ignore
from DrissionPage.common import Actions, Keys  # type: ignore
from config import defaultConfig
import os
import random
import string
ports = {}
class Browser:

    def __init__(self,**kwargs):
        self.path = kwargs.get('path','')
        print('Browser path:',self.path)
        if len(self.path) == 0:
            self.path = defaultConfig['path']
            
        # 如果没有name生成随机字符串
        self.name  = kwargs.get('name', ''.join(random.choices('abcdefghijklmnopqrstuvwxyz',k=10)))
        print('Browser name:',self.name)
        # 数据目录
        userdata = defaultConfig['userdataDir'] + '/' + kwargs.get('userdata', 'userdata' + self.name)
 
        port = ports.get(self.name, random.randint(1024, 65535))
        ports[self.name] = port
        print('Browser port:',port)
        co = ChromiumOptions().set_browser_path(self.path).set_local_port(port).set_user_data_path(userdata)
        # co = ChromiumOptions().set_browser_path(self.path).set_user_data_path(userdata) 
        print('Browser userdata:',userdata)
         #加载插件
        extensions = kwargs.get('extensions', [])
        print('Browser extensions:', extensions)
        for extension in extensions:
            if not os.path.exists(extension):
                continue
            co.add_extension(extension)
        #加载默认插件
        for extension in defaultConfig['extensions']:
            if not os.path.exists(extension):
                continue
            co.add_extension(extension)

        self.page = ChromiumPage(co)
        cookies = {'BT': self.name , 'domain': '.douyin.com'}
        self.page.set.cookies(cookies)
        cookies1 = {'PT': defaultConfig['httpport'] , 'domain': '.douyin.com'}
        self.page.set.cookies(cookies1)
 
      
    def oncommand(self, post_data):
        url = post_data.get('url', '')
        try:
            
            if post_data['action'] == 'move_to_click': 
                print('move_to_click')
                tab = self.page.get_tab(url=url)
                ac = Actions(tab) 
                ac.move_to(post_data['selector'])
                ele = self.page.ele(post_data['selector'])
                ele .click(by_js=False) #强制模拟
                return tab
            elif post_data['action'] == 'move_to_input': 
                print('move_to_input 动作')
                tab = self.page.get_tab(url=url)
                ac = Actions(tab)
                ac.move_to(post_data['selector']).click().type(post_data['text'])
                print('move_to_input 动作完成')
                return tab
            elif post_data['action'] == 'move_to': 
                print('move_to 动作')
                tab = self.page.get_tab(url=url)
                ac = Actions(tab)
                ac.move_to(post_data['selector']) 
                print('move_to  动作完成')
                return tab
            elif post_data['action'] == 'clear': 
                print('clear 动作') 
                ele = self.page.ele(post_data['selector'])
                ele.clear()
                return ele
            elif post_data['action'] == 'goto': 
                print('goto')
                self.page.get(post_data['goto'],timeout=10)
                return tab
            elif post_data['action'] == 'test': 
                print('test')
                self.page.get()
                return true
            elif post_data['action'] == 'exit': 
                print('exit')
                os._exit(0)
                return true

        except  errors.PageDisconnectedError as e:
            del browsers[self.name]
            print('Browser is closed:',e )
        except Exception as e:
            print('Browser get error:',e)

browsers = {}

def createBrowser(**args):
    try:
 
        #如果不存在就随机生成名字
        name = args['name'] if 'name' in args else ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        if name in browsers:
            tmp = browsers[name]
            del browsers[name]
            try:
                tmp.disconnect()
            except:
                pass
        path = args['path'] if 'path' in args else defaultConfig['path']
        extensions = args['extensions'] if 'extensions' in args else defaultConfig['extensions']
        browser = Browser(path=path, name=name, extensions=extensions)
        browsers[name] = browser
        return browser
    except Exception as e:
        print('Browser create error:',e)



def releaseBrowser(name):
    if name in browsers:
        del browsers[name]
 