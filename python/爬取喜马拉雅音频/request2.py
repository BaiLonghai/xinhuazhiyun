import requests
import bs4
import json
import os
import openpyxl


class Ximalaya():
    def __init__(self):
        self.url = 'https://www.ximalaya.com'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    def search(self, kw):
        res = requests.get(self.url + "/search/" + kw, headers=self.headers)
        bs = bs4.BeautifulSoup(res.text, "html.parser")
        bs1 = bs.find_all('a', class_="xm-album-title ellipsis-2")
        bs2 = bs.find_all('a', class_="xm-album-cover")
        ls = []
        for i in range(len(bs1)):
            d = dict.fromkeys(("title", "albumId", "src", 'count'))
            d['title'] = bs1[i]['title']
            d['albumId'] = bs1[i]['href'].split('/')[-2]
            d['src'] = "https:" + bs2[i].img['src']
            d['count'] = bs2[i].find('div', class_='listen-count').span.text  # 播放量
            ls.append(d)

        return ls

    def get_album(self, albumId):
        res = requests.get(f"{self.url}/revision/album/v1/getTracksList?albumId={albumId}&pageNum=1&sort=0&pageSize=30",
                           headers=self.headers)
        js = json.loads(res.text)
        pageSize = 1000
        totalRecord = int(js['data']['trackTotalCount'])
        totalPageNum = int((totalRecord + pageSize - 1) / pageSize)
        ls = []
        for i in range(totalPageNum):
            res = requests.get(
                f"{self.url}/revision/album/v1/getTracksList?albumId={albumId}&pageNum={i + 1}&sort=0&pageSize={pageSize}",
                headers=self.headers)
            js1 = json.loads(res.text)
            js1 = js1['data']['tracks']
            for item in js1:
                d = dict.fromkeys(('title', 'trackId', 'playCount'))
                d["title"] = item['title']
                d["playCount"] = item['playCount']
                d["trackId"] = item['trackId']
                ls.append(d)
        return ls

    def donwn(self, section, sname):
        try:
            if os.path.isdir(sname) == False:
                os.makedirs(sname)
            sname = sname + r"/"
            res = requests.get(f"https://www.ximalaya.com/revision/play/v1/audio?id={section['trackId']}&ptype=1",
                               headers=self.headers)
            js = json.loads(res.text)
            res = requests.get(js['data']['src'], headers=self.headers).content
            with open(sname + section['title'] + ".m4a", 'wb') as file:
                file.write(res)
            print(section['title'] + " 下载成功!")
        except:
            print(section['title'] + " 下载失败!")

    def to_excel(self, sections, sname):
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.freeze_panes = 'B2'
            ws.row_dimensions[1].height = 25
            ws.column_dimensions['A'].width = 50
            ws.column_dimensions['B'].width = 90
            ws.column_dimensions['C'].width = 20
            ws.append(['title', 'm4aUrl', 'playCount'])

            sname = sname + ".xlsx"
            for item in sections:
                res = requests.get(f"https://www.ximalaya.com/revision/play/v1/audio?id={item['trackId']}&ptype=1",
                                   headers=self.headers)
                js = json.loads(res.text)
                print(item['title'], js['data']['src'], item['playCount'])
                ws.append([item['title'], js['data']['src'], item['playCount']])
            wb.save(sname)
            print(f"保存到 {sname} 成功!")
        except:
            print(f"保存到 {sname} 失败!")


if __name__ == "__main__":
    while True:
        xmly = Ximalaya()
        while True:
            try:
                kw = input("请输入您想搜索的关键字:(书名或者作者)\r\n")
                ls = xmly.search(kw)
                for i, item in enumerate(ls):
                    txt = f"{i + 1}-{item['title']}-{item['count']}"
                    print(txt)
                xh = input(f"请输入您想要下载的专辑的序号:1-{len(ls)}  返回上一步请输入'#'键\r\n")
                if xh != '#':
                    try:
                        xh = int(xh) - 1
                        break
                    except:
                        print("输入有误!回到开始位置")

            except:
                print("关键字有误,或者没找到!")
        print("正在遍历所有的章节,这需要些时间.......")
        sections = xmly.get_album(ls[xh]["albumId"])
        for i, item in enumerate(sections):
            print(i + 1, item['title'])
        ts = input(
            f"           有几种交互方式,请参考!\r\n1.请输入需要下载的章节序号:1-{len(sections)} 支持范围下载 例如输入:10-100\r\n2.如果您要全部都下载,请输入'#'键\r\n3.如果您要全部打印到excel表格里请输入'e'键\r\n4.退出按x键\r\n")
        name = ls[xh]["title"]
        if ts == "#":
            for item in sections:
                xmly.donwn(item, name)
        else:
            if '-' in ts:
                min, max = ts.split('-')
                for i in range(int(min), int(max) + 1):
                    xmly.donwn(sections[i], name)
            elif ts == 'e':
                xmly.to_excel(sections, name)
            elif ts == 'x':
                break
            else:
                xmly.donwn(sections[int(ts) - 1], name)
        ts = input("还要继续输入'j'键,退出输入任意键")
        if ts != 'j':
            break
