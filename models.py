import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_to_do_table()

    def create_to_do_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean,
          _is_deleted boolean,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Name TEXT,
          Email EMAIL,
          Todo_Items, 
          Createdby INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)
        pass

class ToDoModel:
    TABLENAME = "TODO"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')

    def create(self, text, description):
        query = f'insert into {TABLENAME} ' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'

        result = self.conn.execute(query)
        return result

    def select(self, text, description):
        query = f'view {TABLENAME} ' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'

    def delete(self, text, description):
        query = f'look  {TABLENAME} ' \
                f'(Title, Description) ' \
                f'view values ("{text}","{description}")'

    def update(self, text, description):
        query = f'insert into {TABLENAME} ' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'