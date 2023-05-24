
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





class Customer:
    def __init__(self, id, username, password,email,birthdate, flightId=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.birthdate = birthdate
        self.flightId = flightId
    
    

class CustomerDB:
    customernum = 1
    def __init__(self):
        self.customers = []
        try:
            cursor.execute("""IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CustomerDB')
                                CREATE TABLE CustomerDB (
                                    id INT PRIMARY KEY,
                                    username VARCHAR(50),
                                    password VARCHAR(50),
                                    email VARCHAR(50),
                                    birthdate DATE,
                                    flightId INT FOREIGN KEY REFERENCES FlightDB(id) ON DELETE SET NULL
                                );     
                            """)
        except pyodbc.Error as e:
            print(f"Error Creating CustomerDB Table: {e}")

        self.refreshDB()

    def refreshDB(self):
        self.customers.clear()
        try:
            cursor.execute("SELECT id, username, password, email, birthdate, flightId FROM CustomerDB")
            rows = cursor.fetchall()
            for row in rows:
                customer = Customer(row.id, row.username, row.password, row.email, row.birthdate, row.flightId)
                self.customers.append(customer)
        except pyodbc.Error as e:
            print(f"Error Refreshing CustomerDB: {e}")

    def addCustomer(self,username, password,email,birthdate):
        flag = True
        id = self.__class__.customernum
        if self.customers:
            for c in self.customers:
                if c.id == id:
                    flag = False
                    break

        if flag:
            try:
                customer = Customer(id, username, password, email, birthdate)
                cursor.execute(f"INSERT INTO CustomerDB(id, username, password, email, birthdate, flightId) VALUES (?,?,?,?,?,?)",(id, username, password, email, birthdate, None))
                conn.commit()
                self.customers.append(customer)
                print("Customer Added Successfully")
                self.__class__.customernum+=1
                return True
            except pyodbc.Error as e:
                print(f"Error Adding Customer: {e}")
                return False
        else:
            print(f"Customer With the ID {id} Already Exists")
            return False

    def updateCustomer(self, id, attribute, value):
        flag = False
        for c in self.customers:
            if c.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute(
                    f"""UPDATE CustomerDB SET {attribute} = ?
                                WHERE ID = ?
                                """,(value, id))
                conn.commit()
                self.refreshDB()
                print(f"Customer {attribute} updated successfully.")
            except pyodbc.Error as e:
                print(f"Error updating customer: {e}")
        else:
            print(f"Customer with ID {id} does not exist.")

    def removeCustomer(self, id):
        flag = False
        for c in self.customers:
            if c.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute("DELETE FROM CustomerDB WHERE id = ?", (id,))
                conn.commit()
                
                self.customers.remove(c)
                self.__class__.customernum -=1
                print("Customer deleted successfully.")
            except pyodbc.Error as e:
                print(f"Error deleting customer: {e}")
        else:
            print(f"Customer with ID {id} does not exist.")

    def displayCustomers(self):
        if not self.customers:
            print("Customers Database is Empty")
        else:
            print(f"{'ID':<10}{'Username':^30}{'Booked Flight ID':^30}{'Email':^30}{'Birthdate':^30}")
            for c in self.customers:
                print(f"{c.id:<10}{c.username:^30}{str(c.flightId):^30}{c.email:^30}{c.birthdate:^30}")

    
    def checkCustomerlogin(self,name, password):
        for c in self.customers:
            if c.username.lower() == name.lower() and c.password == password:
                return True
        return False

    def getCustomerId(self,name):
        for c in self.customers:
            if c.username.lower() == name.lower():
                return c.id
        return None
    
    
    def clearDB(self):
        try:
            cursor.execute(f"DELETE FROM CustomerDB")
            self.customers.clear()
            print("Customer Database Cleared Successfully")
        except pyodbc.Error as e:
            print(f"Error Clearing Customer Database: {e}")
   
   
    def getCustomerQuantity(self):
        cursor.execute('SELECT COUNT(*) FROM CustomerDB')
        count = cursor.fetchone()[0]
        return count        
            
# customerDB = CustomerDB()
# customerDB.displayCustomers()
