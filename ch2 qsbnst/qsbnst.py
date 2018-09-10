import urllib.request
import codecs
import time
import urllib.error
from lxml import html
from retrying import retry




class book:
    url = "https://www.xklxsw.com/book/6242/"
    current = "chapter.txt"
    chapterpath = '/html/body/div[2]/div[5]//@href'           #chapter path
    chptnamepath = '/html/body/div[2]/div[5]/span//text()'    #chapter name path
    booknamepath = '/html/body/div[2]/div[2]/h1/text()'

    def info(self):
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        data = response.read()
        data = data.decode('gbk')
        tree = html.fromstring(data)
        self.paths = tree.xpath(self.chapterpath)
        self.chaptername = tree.xpath(self.chptnamepath)
        name = tree.xpath(self.booknamepath)
        self.bookname = name[0]
        self.filename = self.bookname + '.txt'
        print(self.filename)
        for i in range(0,len(self.paths)):
            self.paths[i] = self.url+self.paths[i]

    @retry
    def readchapter(self, filename, url):

        #contentpath = '//*[@id="htmlContent"]//text()'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        data = response.read()
        data = data.decode('gbk', 'ignore')
        tree = html.fromstring(data)
        result = tree.xpath(self.contentpath)
        for x in result:
            filename.write(x.strip())
            filename.write('\n\r')

    def holebook(self):
        self.info()
        shu = codecs.open(self.filename,'w',encoding = 'utf-8')
        shu.write('')
        shu.close()

        shu = codecs.open(self.filename,'a',encoding = 'utf-8')
        shu.write(self.bookname)
        shu.write('\n')
        i = 0

        for i in range(0,len(self.paths)):
            shu.write(self.chaptername[i])
            shu.write('\n\r')
            readchapter(shu, self.paths[i])
            i= i+1
            if i%100==0:
                time.sleep(2)
            print(i/len(self.paths))
        shu.close()
        cur = codecs.open(self.current, 'w', encoding='utf-8')
        cur.write(str(len(self.paths)))
        cur.close()


    def refresh(self):
        self.info()
        cur = codecs.open(self.current, 'r', encoding='utf-8')
        curser = int(cur.read())
        print(curser)
        cur.close()

        shu = codecs.open(self.bookname+'.txt', 'a', encoding='utf-8')

        for i in range(curser,len(self.paths)):
            shu.write(self.chaptername[i])
            shu.write('\n\r')
            self.readchapter(shu, self.paths[i])
            i= i+1
            if i%100==0:
                time.sleep(2)
            print(i/len(self.paths))
        cur = codecs.open(self.current, 'w', encoding='utf-8')
        cur.write(str(len(self.paths)))
        cur.close()
        shu.close()

class shuanshuwang(book):
    url = 'http://www.shuanshu.com/files/article/html/3/3252/'   
    chapterpath = '/html/body/div[8]//@href'
    chptnamepath = '/html/body/div[8]//a/text()'
    booknamepath = '//*[@id="bookname"]/span/text()'
    contentpath = '//*[@id="htmlContent"]//text()'

class kelexiaoshuo(book):
    url = "https://www.xklxsw.com/book/6242/"
    chapterpath = '/html/body/div[2]/div[5]//@href'           #chapter path
    chptnamepath = '/html/body/div[2]/div[5]/span//text()'    #chapter name path
    booknamepath = '/html/body/div[2]/div[2]/h1/text()'
    contentpath = '//*[@id="content"]//text()'

cydg = kelexiaoshuo()
cydg.url = 'https://www.xklxsw.com/book/33647/'
cydg.current = 'cydgchapter.txt'
cydg.refresh()
