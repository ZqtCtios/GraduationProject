import json
import time

import pymysql
import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'zqt1997',
            'db': 'GProject',
            'charset': 'utf8mb4'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def connectToDb(self):
        db = pymysql.connect()
        cursor = db.cursor()
        return db, cursor

    def getBookmsg(self):
        msg = 0
        return msg

    def getMsgById(self, bookId):
        bookMsg = {}
        bookUrl = 'https://book.douban.com/subject/' + str(bookId)
        html = requests.get(bookUrl, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.find_all('a', attrs={'class': 'tag'})
        bookTags = []
        for item in tags:
            tag = item.text
            bookTags.append((tag))
        bookMsg['bookTags'] = bookTags
        msg_json = soup.find(
            'script', attrs={
                'type': "application/ld+json"}).text
        msg_dict = json.loads(msg_json)
        bookMsg['bookName'] = msg_dict['name']
        bookMsg['author'] = msg_dict['author'][0]['name']
        bookMsg['bookId'] = bookId
        bookMsg['bookUrl'] = bookUrl
        try:
            bookMsg['ratingPoint'] = soup.find(
                'strong', attrs={
                    'class': 'rating_num'}).text.replace(
                ' ', '')
            bookMsg['ratingPeople'] = soup.find(
                'a', attrs={'class': 'rating_people'}).text[:-3]
        except:
            bookMsg['ratingPoint'] = 0
            bookMsg['ratingPeople'] = 0
        bookMsg['bookImg'] = soup.find('a', attrs={'class': 'nbg'})['href']

        return bookMsg

    def work(self):
        self.cursor.execute(
            "select id,bookId from bookIdForSpider where hasdone=0 ")
        data = self.cursor.fetchall()
        count = 0
        for line in data:
            pid = line[0]
            bookid = line[1]
            try:
                msg = self.getMsgById(bookid)
                self.cursor.execute(
                    "insert into bookMsg values(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (pid,
                        bookid,
                        msg['bookName'],
                        msg['author'],
                        msg['bookUrl'],
                        msg['bookImg'],
                        msg['ratingPoint'],
                        msg['ratingPeople']))
                for tag in msg['bookTags']:
                    self.cursor.execute(
                        "insert into bookToTag(bookId,TagName) values(%s,%s)", (pid, tag))
                self.cursor.execute(
                    'update bookIdForSpider set hasdone=1 where id =%s', (pid))
                self.db.commit()
                count += 1
                print(pid, " hasdone")
                time.sleep(1)
            except BaseException:
                self.cursor.execute(
                    'update bookIdForSpider set hasdone=2 where id =%s', (pid))
                self.db.commit()
                print(pid, " fail")
                time.sleep(1)


if __name__ == '__main__':
    sp = Spider()
    sp.work()
