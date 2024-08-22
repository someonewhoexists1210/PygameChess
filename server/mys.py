import mysql.connector
class MYSQL:
    
    def __init__(self, path, host, user, password, database):
        self.path = path
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database)
        
        self.mycursor = self.mydb.cursor(buffered=True)

    def select(self, table, condition, value, condition2='', value2='', operator=''):
        try:
            if condition2 == '':
                command = (f"SELECT * FROM {table} WHERE {condition} = '{value}'")
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                return results
            
            else:
                command = (f"SELECT * FROM {table} WHERE {condition} = '{value}' {operator} {condition2} = '{value2}'")
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                if results == []:
                    return ['No results']
                return results
            
        except mysql.connector.errors.Error as e:
            return "Error", e
        
        
    
    def selectall(self, table, order=False, orderby='', ordering='DESC'):
        try:
            if not order:
                command = f'SELECT * from {table}'
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                return results
            else:
                command = f'SELECT * from {table} ORDER BY {orderby} {ordering}'
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                return results
        except mysql.connector.errors.Error as e:
            return "Error", e

   
    def selectexists(self, table, condition, value, condition2='', value2='', operator=''):
        try:
            if condition2 == '':
                command = (f"SELECT EXISTS(SELECT * FROM {table} WHERE {condition} = '{value}')")
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                return results
        
            else:
            
                command = (f"SELECT EXISTS(SELECT * FROM {table} WHERE {condition} = '{value}' {operator} {condition2} = '{value2}')")
                self.mycursor.execute(command)
                results = self.mycursor.fetchall()
                return results
        except mysql.connector.errors.Error as e:
            return "Error", e
    
    def insert(self, table, column, values):
        try:
            command = f"INSERT into {table}({column[0]},{column[1]}) VALUES ('{values[0]}','{values[1]}')"
            self.mycursor.execute(command)
            self.mydb.commit()

        except mysql.connector.errors.Error as e:
            return str(e)
        
    
    def update(self, table, columns, values):
        try:
            command = f"UPDATE {table} SET {columns[0]}='{values[0]}' WHERE {columns[1]}='{values[1]}'"
            self.mycursor.execute(command)
            self.mydb.commit()
            return self.select(table, columns[1], values[1])
        except mysql.connector.errors.Error as e:
            print(e)

    def runncommand(self, command):
        try:
            self.mycursor.execute(command)
            self.mydb.commit()
            
        except mysql.connector.errors.Error as e:
            print(e)


