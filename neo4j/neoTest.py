import pymysql
from py2neo import Graph, Node, Relationship,NodeSelector


graph=Graph(password="zqt1997")
selector = NodeSelector(graph)


def test2():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'zqt1997',
        'db': 'GProject',
        'charset': 'utf8mb4'
    }
    db=pymysql.connect(**config)
    cursor=db.cursor()
    cursor.execute('select TagName from bookToTag group by TagName order by count(TagName) desc limit 10')
    data=cursor.fetchall()
    for line in data:
        tagname=line[0]
        tag=Node('Tag',name=tagname)
        print("create ",tagname)
        graph.create(tag)
        cursor.execute('select bookId from bookToTag where TagName=%s limit 100',(tagname))
        books=cursor.fetchall()
        for book in books:
            bookId=book[0]
            cursor.execute('select bookName from bookMsg where  id=%s',(bookId))
            bookName=cursor.fetchall()[0][0]
            book=selector.select("Book").where(name=bookName).first()
            print(book)
            if book==None:
                book=Node('Book',name=bookName)
            r=Relationship(book,'To',tag)
            graph.create(r)

if __name__ == "__main__":
    test2()

