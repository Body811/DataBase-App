
import pyodbc

driverName = "SQL Server"
server = "DESKTOP-BJI4RD5\SQLEXPRESS"
database = "Database_App"

conn_str = f""" DRIVER={{{driverName}}};
                SERVER={server};
                DATABASE={database};
                Trust_Connection=yes;
            """


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


class Admin:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class AdminDB:
    def __init__(self):
        self.admins = []
        try:
            cursor.execute("""IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AdminDB')
                                CREATE TABLE AdminDB (
                                    id INT PRIMARY KEY,
                                    username VARCHAR(50),
                                    password VARCHAR(50)
                                );     
                            """)
        except pyodbc.Error as e:
            print(f"Error Creating AdminDB Table: {e}")

        self.refreshDB()
        
        
        
        
        
    def refreshDB(self):
        self.admins.clear()
        try:
            cursor.execute("SELECT id, username, password FROM AdminDB")
            rows = cursor.fetchall()
            for row in rows:
                admin = Admin(row.id, row.username, row.password)
                self.admins.append(admin)
        except pyodbc.Error as e:
            print(f"Error Refreshing AdminDB: {e}")



    def addAdmin(self, username, password):
        flag = True
        id = len(self.admins) + 1
        if self.admins:
            for a in self.admins:
                if a.id == id:
                    flag = False
                    break
        if flag:
            try:
                admin = Admin(id, username, password)
                cursor.execute(f"INSERT INTO AdminDB(id, username, password) VALUES (?,?,?)", (id, username, password))
                conn.commit()
                self.admins.append(admin)
                print("Admin Added Successfully")
                return True
            except pyodbc.Error as e:
                print(f"Error Adding Admin: {e}")
                return False
        else:
            print(f"Admin With ID {id} Already Exists")
            return False
        
        
    def removeAdmin(self, id):
        flag = False
        for a in self.admins:
            if a.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute("DELETE FROM AdminDB WHERE id = ?", (id,))
                conn.commit()
                
                self.admins.remove(a)
                print("Admin deleted successfully.")
            except pyodbc.Error as e:
                print(f"Error deleting Admin: {e}")
        else:
            print(f"Admin with ID {id} does not exist.")
            
            
            
    def displayAdmins(self):
        if not self.admins:
            print("Admin Database is Empty")
        else:
            print(f"{'ID':<10}{'Username':^30}")
            for a in self.admins:
                print(f"{a.id:<10}{a.username:^30}")
                
                
                
    def checkAdminLogin(self, username, password):
        for a in self.admins:
            if a.username.lower() == username.lower() and a.password == password:
                return True
        return False
    
    
    def getAdminQuantity(self):
        cursor.execute('SELECT COUNT(*) FROM AdminDB')
        count = cursor.fetchone()[0]
        return count
    
    
admidDB = AdminDB()

# admidDB.addAdmin("abdo",123)

# admidDB.addAdmin('mohanned',123)