import urllib.request
import urllib.parse
import codecs
from clr import *

class yunyinyue:
    url = None
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    def playlist(self,id):
        self.url = 'https://music.163.com/playlist?id='+str(id)
        namepath = '//*[@class="f-hide"]//text()'
        listnamepath = '//*[@class ="f-ff2 f-brk"]/text()'
        request = urllib.request.Request(self.url,headers = self.headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        data = data.decode('utf-8')
        tree = html.fromstring(data)
        songnames = tree.xpath(namepath)
        self.listname = tree.xpath(listnamepath)
        filename = self.listname[0] + '.txt'
        rcd = codecs.open(filename, 'w', encoding='utf-8')
        for i in range(0,len(songnames)):
            rcd.write(songnames[i]+'\n')
            print(songnames[i])
        rcd.close()

    def search(self,name):
        bytename = urllib.parse.quote(name, safe='~()*!.\'')
        self.url = 'http://sou.kuwo.cn/ws/NSearch?type=all&catalog=yueku20177&key='+ bytename
        firstchoice = '// *[ @ class = "m_name"] // @ href'
        realname = '// *[ @ class = "m_name"] // @ title'
        request = urllib.request.Request(self.url,headers = self.headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        data = data.decode('utf-8')
        tree = html.fromstring(data)
        songpath = tree.xpath(firstchoice)
        realn = tree.xpath(realname)
        filename = '酷我路径.txt'
        fl = "酷我路径纯.txt"
        rcd = codecs.open(filename, 'a', encoding='utf-8')
        rcd.write(name + '\r\n')
        rcd.write(realn[0] + '\r\n')
        rcd.write(songpath[0] + '\r\n')
        print(name + '\n' + realn[0] + '\n' + songpath[0] + '\n')
        rcd.close()
        rcd = codecs.open(fl, 'a', encoding='utf-8')
        rcd.write(songpath[0] + '\n')
        rcd.close()


gedan = yunyinyue()

gedan.playlist(518125293)

songlist = codecs.open(gedan.listname[0] + '.txt', 'r', encoding='utf-8')

i=0
while True:
    name = songlist.readline()
    if name == '' :
        break
    try:
        gedan.search(name)
    except:
        print("error with song No." + str(i))
    i=i+1
    print(i)

