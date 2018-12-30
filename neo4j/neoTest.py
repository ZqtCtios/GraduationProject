import pymysql
from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property


gragp=Graph(password="zqt1997")
class Book(GraphObject):
    __primarykey__ = 'name'
    name = Property()
# config = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'password': 'zqt1997',
#     'db': 'GProject',
#     'charset': 'utf8mb4'
# }
# db=pymysql.connect(**config)
# cursor=db.cursor()
# cursor.execute("select TagName from ")
# cursor.execute("select * from bookMsg limit 100")
# data=cursor.fetchall()
# for line in data:
#     book={}
#     book['bookId']=line[1]
#     book['name']=line[2]
#     book['bookUrl']=line[4]
#     book['bookImg']=line[5]
#     book['ratingPoint']=line[6]
#     book['ratingPeople']=line[7]
#     print(book)
#     a=Node('Book',**book)
#     gragp.create(a)

def test1():
    a=Node('Book',name='dsds')
    b=Node('Tag',name='小说')
    r=Relationship(a,'belong',b)
    s=a|b|r
    gragp.create(s)
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
        #gragp.create(tag)
        cursor.execute('select bookId from bookToTag where TagName=%s limit 100',(tagname))
        books=cursor.fetchall()
        for book in books:
            bookId=book[0]
            cursor.execute('select bookName from bookMsg where  id=%s',(bookId))
            bookName=cursor.fetchall()[0][0]
            book=Book.select(gragp).where(name=bookName).first()
            print(book)
            input()
            # if len(book)==0:
            #     book=Node('Book',name=bookName)
            # else:
            #     book=book[0]
            # r=Relationship(book,'To',tag)
            # gragp.create(r)

if __name__ == "__main__":
    test2()

# # from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
 
 
# # class Movie(GraphObject):
# #     __primarykey__ = 'title'
 
# #     title = Property()
# #     released = Property()
# #     actors = RelatedFrom('Person', 'ACTED_IN')
# #     directors = RelatedFrom('Person', 'DIRECTED')
# #     producers = RelatedFrom('Person', 'PRODUCED')
 
# # class Person(GraphObject):
# #     __primarykey__ = 'name'
 
# #     name = Property()
# #     born = Property()
# #     acted_in = RelatedTo('Movie')
# #     directed = RelatedTo('Movie')
# #     produced = RelatedTo('Movie')
# from py2neo.ogm import GraphObject, Property
# from py2neo import Graph, Node, Relationship
# graph = Graph(password='zqt1997')


# class Person(GraphObject):
#     __primarykey__ = 'name'

#     name = Property()
#     age = Property()
#     location = Property()
# a = Node('Person', name='Alice', age=21, location='广州')
# b = Node('Person', name='Bob', age=22, location='上海')
# c = Node('Person', name='Mike', age=21, location='北京')
# r1 = Relationship(a, 'KNOWS', b)
# r2 = Relationship(b, 'KNOWS', c)
# graph.create(a)
# graph.create(r1)
# graph.create(r2)
# person = Person.select(graph).where(age=21).first()
# print(person)
# print(person.name)
# print(person.age)
