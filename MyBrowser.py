import os.path
import sys
import time
import requests
import random
import json

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtNetwork import QNetworkProxy
from PySide2.QtWebEngineCore import *
from adblockparser import AdblockRules

class MyWebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """ This is the url interceptor class to intercept the requests before they reach network """

    def __init(self):
        super().__init__()

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if MyBrowser.rules.should_block(url):
            info.block(True)

class MyBrowser(QWidget):
    """ This basic widget class have a webview to browse internet using random anonymous proxies """

    rules = None

    def __init__(self):
        """ Constructor """

        super().__init__()
        self.setWindowTitle('My Browser')
        self.resize(800,600)
        self.proxy = QNetworkProxy()
        self.proxy.setType(QNetworkProxy.HttpProxy)

        #Get random proxy IP and port
        self.proxies = self.getProxies()
        self.getAdBlockList()       

        #Layout the widgets
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.textbox = QLineEdit('')
        self.textbox.setPlaceholderText('Enter url')
        self.button = QPushButton('&Go')
        self.button.setAutoDefault(True)
        self.comboBox = QComboBox()
        self.comboBox.addItems(self.proxies)
        self.view = QWebEngineView()

        self.webEnginePage = self.view.page()
        self.webEngineProfile = self.webEnginePage.profile()
        self.urlInterceptor = MyWebEngineUrlRequestInterceptor()
        self.webEngineProfile.setUrlRequestInterceptor(self.urlInterceptor)

        self.hbox.addWidget(self.textbox)
        self.hbox.addWidget(self.comboBox)
        self.hbox.addWidget(self.button)        
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.view)
        self.setLayout(self.vbox)

        #Set the first page
        self.view.load(QUrl('about:blank'))
        self.view.show()

        self.button.clicked.connect(self.browse)
        self.textbox.returnPressed.connect(self.browse)
        self.comboBox.currentTextChanged.connect(self.setProxy)
        
        self.setProxy(random.choice(self.proxies))
    def setProxy(self, ipport):
        ip, port = ipport.split(':')
        self.proxy.setHostName(ip)
        self.proxy.setPort(int(port))
        QNetworkProxy.setApplicationProxy(self.proxy)
        self.setWindowTitle(f"My Browser : {ipport}")
        
    def browse(self):
        """ This function load the url from the user input """

        self.view.stop();
        url = self.textbox.text()
        if url.strip() == "":
            return

        if not url.startswith('http'):
            url = 'https://' + url
        self.view.load(QUrl(url))

    def getProxies(self):
        """ Get a list of free anonymous proxies and choose a random one """

        if os.path.exists('proxy.json') and ((time.time() - os.path.getmtime('proxy.json'))/3600 < 1):
            with open('proxy.json') as proxyfile:
                flist = json.load(proxyfile)['data']
        else:
            req = requests.get('http://pubproxy.com/api/proxy?format=json&https=true&type=http&limit=5&speed=10&level=anonymous')
            with open('proxy.json', 'w') as proxyfile:
                proxyfile.write(req.text)
                flist = json.loads(req.text)['data']        
        
        mylist = []
        for item in flist:
            mylist.append(item.get('ipPort'))
        return mylist

    def getAdBlockList(self):
        """ Pull the AdBlockRules from cloude and then cache it for future processing """
        
        if os.path.exists('easylist.txt') and ((time.time() - os.path.getmtime('easylist.txt'))/3600 < 1):
            with open('easylist.txt', 'r') as easylist:
                MyBrowser.rules = AdblockRules([line.strip() for line in easylist])
        else:
            req = requests.get('https://easylist.to/easylist/easylist.txt')
            lines = req.text.split('\n')[16:]
            MyBrowser.rules = AdblockRules(lines)
            with open('easylist.txt', 'w') as easylist:
                for line in lines:
                    easylist.write(line + '\n')

if __name__ == '__main__':

    app = QApplication([])
    app.setStyle('fusion')
    browser = MyBrowser()
    browser.show()
    sys.exit(app.exec_())
