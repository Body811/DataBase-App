
import pyodbc
from SeatDB import SeatDB
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


seats = SeatDB()

class Aircraft:
    def __init__(self, id, model, bussinesSeatNum, economySeatNum):
        self.id = id
        self.model = model
        self.bussinesSeatNum = bussinesSeatNum
        self.economySeatNum = economySeatNum



class AircraftDB:
    def __init__(self):
        self.aircrafts = []
        try:
            cursor.execute("""IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'AircraftDB')
                                CREATE TABLE AircraftDB (
                                    id INT PRIMARY KEY,
                                    model VARCHAR(20),
                                    bussinesSeatNum int,
                                    economySeatNum int
                                );     
                            """)
        except pyodbc.Error as e:
            print(f"Error Creating AircraftDB Table: {e}")

        self.refreshDB()

    def refreshDB(self):
        self.aircrafts.clear()
        try:
            cursor.execute("SELECT id, model, bussinesSeatNum, economySeatNum  from AircraftDB")
            rows = cursor.fetchall()
            for row in rows:
                aircraft = Aircraft(row.id, row.model, row.bussinesSeatNum, row.economySeatNum)
                self.aircrafts.append(aircraft)
        except pyodbc.Error as e:
            print(f"Error Refreshing AircraftDB: {e}")

    def addAircraft(self, id, model, bussinesSeatNum, economySeatNum):
        flag = True
        if self.aircrafts:
            for a in self.aircrafts:
                if a.id == id:
                    flag = False
                    break

        if flag:
            try:
                aircraft = Aircraft(id, model, bussinesSeatNum, economySeatNum)
                cursor.execute(f"INSERT INTO AircraftDB(id, model, bussinesSeatNum,economySeatNum) VALUES (?,?,?,?)",(id, model, bussinesSeatNum, economySeatNum))
                conn.commit()
                self.aircrafts.append(aircraft)
                print("test1")
                print("Aircraft Added Successfully")
                return True
            except pyodbc.Error as e:
                print(f"Error Adding Aircraft: {e}")
                return False
        else:
            print(f"Aircraft With the ID {id} Already Exists")
            return False

    def updateAircraft(self, id, attribute, value):
        flag = False
        for a in self.aircrafts:
            if a.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute(
                    f"""UPDATE AircraftDB SET {attribute} = ?
                                WHERE ID = ?
                                """,(value, id))
                conn.commit()
                self.refreshDB()
                print(f"Aircraft {attribute} updated successfully.")
                return True
            except pyodbc.Error as e:
                print(f"Error updating aircraft: {e}")
                return False
        else:   
            print(f"Aircraft with ID {id} does not exist.")
            return False
        
        
        
    def removeAircraft(self, id):
        flag = False
        for a in self.aircrafts:
            if a.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute("DELETE FROM AircraftDB WHERE id = ?", (id,))
                conn.commit()
                self.aircrafts.remove(a)
                seats.removeSeatsByAircraftId(id)
                print("Aircraft deleted successfully.")
            except pyodbc.Error as e:
                print(f"Error Deleting Aircraft: {e}")
        else:
            print(f"Aircraft with ID {id} does not exist.")

    def displayAircrafts(self):
        if not self.aircrafts:
            print("Aircrafts Database is Empty")
        else:
            print(
                f"{'ID':<10}{'Model':^30}{'No. of Business Seats':^30}{'No. of Economy Seats':^30}{'Total Number of Seats':^25}"
            )
            for a in self.aircrafts:
                print(
                    f"{a.id:<10}{a.model:^30}{a.bussinesSeatNum:^30}{a.economySeatNum:^30}{a.bussinesSeatNum+a.economySeatNum:^25}"
                )

    def checkAircraftExist(self, id):
        flag = False
        for a in self.aircrafts:
            if a.id == id:
                flag = True
                break
        return flag

    def getBussinesSeatNum(self,id):
        for a in self.aircrafts:
            if a.id == id:
                return a.bussinesSeatNum
                
    def getEconomySeatNum(self,id):
        for a in self.aircrafts:
            if a.id == id:
                return a.economySeatNum         

    
    def getAircraftQuantity(self):
        return len(self.aircrafts)
    
    def clearDB(self):
        try:
            cursor.execute(f"DELETE FROM AircraftDB")
            self.aircrafts.clear()
            print("Aircraft Database Cleared Successfully")
        except pyodbc.Error as e:
            print(f"Error Clearing Aircraft Database: {e}")
            
    
        
        
# aircraftdb = AircraftDB()
# aircraftdb.displayAircrafts()
