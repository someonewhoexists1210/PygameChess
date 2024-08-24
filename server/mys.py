import psycopg2
from psycopg2 import sql, Error
import os

class PostgreSQL:
    def __init__(self, database):
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        self.mydb = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )
        self.mycursor = self.mydb.cursor()

    def select(self, table, condition, value, condition2='', value2='', operator=''):
        try:
            if not condition2:
                command = sql.SQL("SELECT * FROM {table} WHERE {condition} = %s").format(
                    table=sql.Identifier(table),
                    condition=sql.Identifier(condition)
                )
                self.mycursor.execute(command, (value,))
            else:
                command = sql.SQL("SELECT * FROM {table} WHERE {condition} = %s {operator} {condition2} = %s").format(
                    table=sql.Identifier(table),
                    condition=sql.Identifier(condition),
                    operator=sql.SQL(operator),
                    condition2=sql.Identifier(condition2)
                )
                self.mycursor.execute(command, (value, value2))

            results = self.mycursor.fetchall()
            return results if results else ['No results']

        except Error as e:
            return f"Error: {e}"
    
    def selectall(self, table, order=False, orderby='', ordering='DESC'):
        try:
            if not order:
                command = sql.SQL("SELECT * FROM {table}").format(
                    table=sql.Identifier(table)
                )
            else:
                command = sql.SQL("SELECT * FROM {table} ORDER BY {orderby} {ordering}").format(
                    table=sql.Identifier(table),
                    orderby=sql.Identifier(orderby),
                    ordering=sql.SQL(ordering)
                )
            self.mycursor.execute(command)
            return self.mycursor.fetchall()

        except Error as e:
            return f"Error: {e}"

    def selectexists(self, table, condition, value, condition2='', value2='', operator=''):
        try:
            if not condition2:
                command = sql.SQL("SELECT EXISTS(SELECT 1 FROM {table} WHERE {condition} = %s)").format(
                    table=sql.Identifier(table),
                    condition=sql.Identifier(condition)
                )
                self.mycursor.execute(command, (value,))
            else:
                command = sql.SQL("SELECT EXISTS(SELECT 1 FROM {table} WHERE {condition} = %s {operator} {condition2} = %s)").format(
                    table=sql.Identifier(table),
                    condition=sql.Identifier(condition),
                    operator=sql.SQL(operator),
                    condition2=sql.Identifier(condition2)
                )
                self.mycursor.execute(command, (value, value2))

            return self.mycursor.fetchone()[0]

        except Error as e:
            return f"Error: {e}"
    
    def insert(self, table, columns, values):
        try:
            command = sql.SQL("INSERT INTO {table} ({cols}) VALUES ({vals})").format(
                table=sql.Identifier(table),
                cols=sql.SQL(', ').join(map(sql.Identifier, columns)),
                vals=sql.SQL(', ').join(sql.Placeholder() for _ in values)
            )
            self.mycursor.execute(command, values)
            self.mydb.commit()

        except Error as e:
            return f"Error: {e}"
        
    def update(self, table, columns, values):
        try:
            command = sql.SQL("UPDATE {table} SET {col1} = %s WHERE {col2} = %s").format(
                table=sql.Identifier(table),
                col1=sql.Identifier(columns[0]),
                col2=sql.Identifier(columns[1])
            )
            self.mycursor.execute(command, (values[0], values[1]))
            self.mydb.commit()
            return self.select(table, columns[1], values[1])

        except Error as e:
            return f"Error: {e}"

    def runcommand(self, command):
        try:
            self.mycursor.execute(command)
            self.mydb.commit()

        except Error as e:
            return f"Error: {e}"

