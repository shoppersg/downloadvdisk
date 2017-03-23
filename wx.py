
import urllib2
import os, sys, re
from bs4 import BeautifulSoup
import codecs


class WeipanDownloader:
    def __init__(self, link, dest):
        self.link = link
        self.dest = dest
        self.files = dict()



    def download(self, destdir, name, link):


        destname = "%s/%s" % (destdir, name)
        if os.path.exists(destname) and os.path.isfile(destname) and os.path.getsize(destname) > 0:
            print name + '   exists, skip...'
            

        html = ""
        done = -1
        
        try:
            print "Downloading 2 %s" % name
            print link


            req = urllib2.Request(link, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
            resp = urllib2.urlopen(req)
            resp.encoding = 'utf8'
            html = resp.read()

            txt2 =''
            soup = BeautifulSoup(html,"html.parser")
            
            #print soup.original_encoding
            txt = soup.findAll("div", {"itemprop":"articleBody"})
            for line in txt:
                txt2 = txt2 + line.prettify()
                 
                 
            
            pretxt = '---\nlayout: post\ntitle:  "'+ title + '"\ncategories: rmji\n---\n'
            lf = codecs.open(destname, "w", encoding="utf-8")

            #print type(txt)
            #print type(unicode(txt))
            #print type(lf)
            
            lf.write(unicode(txt2))
            lf.close()
            filename = '2015-11-11-'+ title + '.markdown'
            txt3 = pretxt + open("tempfile").read()
            
            txt4 = re.sub(r'(http://www.wuxiaworld.com/rmji-index/rmji-chapter-\d+)' , r'\1.html' , txt3)
            txt5 = re.sub(r'http://www.wuxiaworld.com/rmji-index/' , r'' , txt4)
            print ''
            print type(txt4)
            
            open(filename, "w").write(txt5)

            
 
                
            

        except Exception, e:
            done += 1
            print str(done) + ' tries 1st '
            print str(e) + '1st'
        #print "Downloaded  2 %s" % name
        print "Downloaded :" + title


        #pa = '"download_list":\["(.+?)"'
if __name__ == "__main__":
    for chapnumber in range(1, 12):
        
        title = 'rmji-chapter-' + str(chapnumber)
        link = 'http://www.wuxiaworld.com/rmji-index/' + title
        dest = '.'
        wpd = WeipanDownloader(link, dest)
        wpd.download(dest,'tempfile',link)




        
