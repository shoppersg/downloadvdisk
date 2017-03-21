import urllib2
import os, sys, re
from bs4 import BeautifulSoup
import codecs
import markdown

class WeipanDownloader:
    def __init__(self, link, dest):
        self.link = link
        self.dest = dest
        self.files = dict()



    def download(self, destdir, name, link):


        destname = "%s/%s" % (destdir, name)
        if os.path.exists(destname) and os.path.isfile(destname) and os.path.getsize(destname) > 0:
            print name + '   exists, skip...'
            return

        html = ""
        done = -1
        
        try:
            print "Downloading 2 %s" % name
            print link

            #opener = urllib2.build_opener()
            #opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            #response = opener.open(link)

            #resp = opener.open(link,timeout=600)
            
            #resp = urllib2.urlopen(link,timeout=600,headers={ 'User-Agent': 'Mozilla/5.0' })
            req = urllib2.Request(link, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
            resp = urllib2.urlopen(req)
            html = resp.read()


            soup = BeautifulSoup(html,"html.parser")
            
            txt = soup.findAll("div", {"itemprop":"articleBody"})
            txt2 = ''
           # txt = join('\n',txt))
            pretxt = '---\nlayout: post\ntitle:  "chap1"\ndate:   2015-11-17 16:16:01 -0600\ncategories: rmji\n---\n'
            lf = codecs.open(destname, "w", "utf-8")
            #txt2 = txt.strip('[').strip(']')
            #txt3 = txt2.replace('\\n','')
            #txt4 = decode(
            #lf.write(pretxt + txt3)
            #txt2 = pretxt 
            i = 1
            for line in txt:
                 
                 txt2 = txt2 + line

                 
            md = markdown.markdown(txt2)
            
            lf.write(pretxt + md)
            lf.close()
            

        except Exception, e:
            done += 1
            print str(done) + ' tries 1st '
            print str(e) + '1st'
        print "Downloaded  2 %s" % name


        #pa = '"download_list":\["(.+?)"'
if __name__ == "__main__":
 #   args = sys.argv
 #   print args
 #   if len(args) >= 3:
    link = 'http://www.wuxiaworld.com/rmji-index/rmji-chapter-2/'
    dest = '.'
    wpd = WeipanDownloader(link, dest)
 #   wpd.parse()
 #   wpd.downloadAll()
    wpd.download(dest,'2012-09-12-rmji-chapter-1.markdown',link)
