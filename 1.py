import urllib2
import os, sys, re

class WeipanDownloader:
    def __init__(self, link, dest):
        self.link = link
        self.dest = dest
        self.files = dict()

    def get_page(self, i=0):
        if i == 0:
            link = self.link
        else:
            link = "%s?page=%d" % (self.link, i)

        html = ""
        done = -1
        while done < 2:
            try:
                resp = urllib2.urlopen(link)
                html = resp.read()
                done = 2
                #print html
            except Exception, e:
                done += 1
                print str(e)

        return html

    def parse_page_num(self, html):
        pa = '<a href="\?page=(\d+)">(\d+)</a><a class="vd_bt_v2 vd_page_btn"'
        m = re.search(pa, html)
        page_num = int(m.group(1))
        print page_num
        return page_num

    def parse_pages(self, html):
        pa = '<div class="sort_name_detail"><a target="_blank" href="(.+?)" title="(.+?)">(.+?)</a></div>'
        m = re.findall(pa, html)
        if m != None:
            for _m in m:
                self.files[_m[1]] = _m[0]
                print _m[1].decode('utf8')

    def parse_pages2(self, html):
        pa = '<div class="sort_name_detail"><a href="(.+?)" title="(.+?)" class="short_name">(.+?)</a></div>'
        m = re.findall(pa, html)
        files = dict()
        if m != None:
            for _m in m:
                files[_m[1]] = _m[0]
                #print _m[1]
                #print _m[0]
        #print files.keys().decode('utf8')
        return files

    def parse(self):
        html = self.get_page()
        pn = self.parse_page_num(html)
        self.parse_pages(html)
        #print self.files
        #for i in range(1, pn + 1):
        for i in range(70, 80):
            html = self.get_page(i)
            self.parse_pages(html)
            print i
        #print self.files

    def download(self, destdir, name, link):
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        destname = "%s/%s" % (destdir, name)
        if os.path.exists(destname) and os.path.isfile(destname) and os.path.getsize(destname) > 0:
            print name + '   exists, skip...'
            return

        html = ""
        done = -1
        while done < 2:
            try:
                print "Downloading 2 %s" % name
                resp = urllib2.urlopen(link,timeout=600)
                html = resp.read()
                done = 4
            except Exception, e:
                done += 1
                print str(done) + ' tries 1st '
                print str(e) + '1st'
            print "Downloaded  2 %s" % name

        files = self.parse_pages2(html)
        if len(files) > 0:
            new_dest_dir = "%s/%s" % (destdir, name)
            for nn in files.keys():
                self.download(new_dest_dir, nn.decode('utf8'), files[nn])
        else:
            pa = '"download_list":\["(.+?)"'
            m = re.search(pa, html)
            if m != None:
                fl = m.group(1).replace('\\', '')

                done = -1
                while done < 2:
                    try:
                        print "Downloading 3 %s" % name
                        f = urllib2.urlopen(fl,timeout=600)
                        lf = open(destname, "wb")
                        lf.write(f.read())
                        done = 4
                        lf.close()
                    except Exception, e:
                        done += 1
                        print str(done) + ' tries 2nd'
                        print str(e) + '2nd'
                print "Downloaded  3 %s" % name

    def downloadAll(self):
        for name in self.files.keys():
            self.download(self.dest, name.decode('utf8'), self.files[name])

if __name__ == "__main__":
    args = sys.argv
    print args
    if len(args) >= 3:
        wpd = WeipanDownloader(args[1], args[2])
        wpd.parse()
        wpd.downloadAll()
