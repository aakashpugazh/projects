from multiprocessing import connection
import sqlite3
from unittest import result

class Database:
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        # squery = """
        # create table if not exists grades(
        #     semester text,
        #     subject text,
        #     grade text
        # )
        # """
        # self.cursor.execute(squery)
        # self.connection.commit()
    
    def insert(self,semester,subject,grade,username=None):
        squery = "insert into %s values('%s','%s','%s')"%(username,semester,subject,grade)
        self.cursor.execute(squery)
        self.connection.commit()
    
    def fetch(self,semester,username):
        self.cursor.execute("select * from %s where semester='%s'"%(username,semester))
        result = self.cursor.fetchall()
        return result
    
    def update(self,subject,grade,username=None):
        squery = "update %s set grade='%s' where subject='%s'"%(username,grade,subject)
        self.cursor.execute(squery)
        self.connection.commit()
    
    def create(self,username):
        users = self.fetchusers()
        if username in users:
            return -1
        squery = """
        create table if not exists %s(
            semester text,
            subject text,
            grade text
        )
        """%(username)
        self.cursor.execute(squery)
        self.connection.commit()
        return 1
        
    def fetchusers(self):
        self.cursor.execute("select name from sqlite_master where type='table'")
        result = self.cursor.fetchall()
        result = [i[0] for i in result]
        return result
    
    def deleteuser(self,username):
        self.cursor.execute("drop table %s"%(username))
        self.connection.commit()
    
        
        