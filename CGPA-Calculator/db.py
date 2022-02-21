from multiprocessing import connection
import sqlite3

class Database:
    def __init__(self,db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        squery = """
        create table if not exists grades(
            semester text,
            subject text,
            grade text
        )
        """
        self.cursor.execute(squery)
        self.connection.commit()
    
    def insert(self,semester,subject,grade):
        squery = "insert into grades values(?,?,?)"
        self.cursor.execute(squery,(semester,subject,grade))
        self.connection.commit()
    
    def fetch(self,semester):
        self.cursor.execute("select * from grades where semester=?",(semester,))
        result = self.cursor.fetchall()
        return result
    
    def update(self,subject,grade):
        squery = "update grades set grade=? where subject=?"
        self.cursor.execute(squery,(grade,subject))
        self.connection.commit()
    
        
        