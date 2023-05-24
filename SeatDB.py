
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



class Seat:
    def __init__(self, id, classType, aircraftId, customerId):
        self.id = id
        self.classType = classType
        self.aircraftId = aircraftId
        self.customerId = customerId





class SeatDB:
    def __init__(self):
        self.seats = []
        try:
            cursor.execute("""IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SeatDB')
                                CREATE TABLE SeatDB (
                                    id VARCHAR(20) PRIMARY KEY,
                                    classtype VARCHAR(20),
                                    customerID INT,
                                    AircraftID INT,
                                    FOREIGN KEY (AircraftID) REFERENCES AircraftDB(id) ON DELETE SET NULL,
                                    FOREIGN KEY (customerID) REFERENCES CustomerDB(id) ON DELETE SET NULL
                                );     
                            """)
        except pyodbc.Error as e:
            print(f"Error Creating SeatDB Table: {e}")

        self.refreshDB()

    def refreshDB(self):
        self.seats.clear()
        try:
            cursor.execute("SELECT id, classtype, customerID, AircraftID  from SeatDB")
            rows = cursor.fetchall()
            for row in rows:
                seat = Seat(row.id, row.classtype, row.AircraftID, row.customerID)
                self.seats.append(seat)
        except pyodbc.Error as e:
            print(f"Error Refreshing SeatDB: {e}")

    def addSeats(self,flightid , aircraftid, bussinesSeatNum, economySeatNum):
        for i in range(1, int(bussinesSeatNum) + 1):
            seat = Seat(f"{flightid}#{i}", "Business", aircraftid, None)
            cursor.execute(f"INSERT INTO SeatDB(id, classtype, AircraftID, customerID) VALUES (?,?,?,?)",(f"{aircraftid}#{i}", "Business", aircraftid, None))
            conn.commit()
            self.seats.append(seat)
        for i in range(int(bussinesSeatNum) + 1, int(bussinesSeatNum) + int(economySeatNum) + 1):
            seat = Seat(f"{flightid}#{i}", "Economy", aircraftid, None)
            cursor.execute(f"INSERT INTO SeatDB(id, classtype, AircraftID, customerID) VALUES (?,?,?,?)",(f"{aircraftid}#{i}", "Economy", aircraftid, None))
            conn.commit()
            self.seats.append(seat)

    def removeSeat(self, id):
        flag = False
        for s in self.seats:
            if s.id == id:
                flag = True
                break
        if flag:
            try:
                cursor.execute("DELETE FROM SeatDB WHERE id = ?", (id,))
                conn.commit()
                self.seats.remove(s)
                print("Seat deleted successfully.")
            except pyodbc.Error as e:
                print(f"Error Deleting SEAT: {e}")
        else:
            print(f"Seat with ID {id} does not exist.")

    def removeSeatsByAircraftId(self, aircraftId):
        flag = False
        for s in self.seats:
            if s.aircraftId == aircraftId:
                flag = True
                break
        if flag:
            try:
                cursor.execute("DELETE FROM SeatDB WHERE AircraftId = ?", (aircraftId,))
                conn.commit()
                print("Seats deleted successfully.")
                self.refreshDB()
            except pyodbc.Error as e:
                print(f"Error Deleting SEAT: {e}")
        else:
            print(f"Seats with Aircraft ID {aircraftId} does not exist.")

    def displaySeats(self):
        self.seats.sort(key=lambda seat: int(seat.id.split("#")[1]))
        if not self.seats:
            print("Seats Database is Empty")
        else:
            print(f"{'ID':<10}{'Class':^30}{'Aircraft ID':^30}{'Customer ID':^30}")
            for a in self.seats:
                print(f"{a.id:<10}{a.classType:^30}{str(a.aircraftId):^30}{str(a.customerId):^30}")

    def bookSeat(self,aircraftid,custId,classType, seatnum):
        while(seatnum > 0):
            flag = False
            for s in self.seats:
                if s.aircraftId == aircraftid and s.classType.lower() == classType.lower() and s.customerId is None:
                    print("test1")
                    
                    flag = True
                    break

            if flag:
                try:
                    print("test2")
                    cursor.execute(f"""UPDATE SeatDB SET CustomerId = ?
                                    WHERE AircraftID = ?
                                    """,(custId, aircraftid))
                    conn.commit()
                    self.refreshDB()
                    print("Seat Booked Successfully.")
                    seatnum -= 1
                except pyodbc.Error as e:
                    print(f"Error Booking Seat: {e}")
            else:
                print(f"The Plane's {classType} Seats are Full")
                return
        
    def getAvailableSeats(self, aircraftId,classType):
        count = 0
        for s in self.seats:
            if s.aircraftId == aircraftId and s.classType.lower() == classType.lower() and s.customerId is None:
                count+=1
    
        return count
        
    def getSeats(self, customerid):
        result = []
        for s in self.seats:
            if str(s.customerId) == str(customerid):
                result.append({
                    'seatid': s.id, 
                    'classType': s.classType})
        return result
    
    
    def getSeatQuantity(self):
        cursor.execute('SELECT COUNT(*) FROM SeatDB')
        count = cursor.fetchone()[0]
        return count
    
    def getMaxSeat(self):
        cursor.execute('''SELECT TOP 1 c.username, COUNT(*) as seat_count FROM 
                       SeatDB s JOIN CustomerDB c 
                       ON s.customerID = c.id 
                       GROUP BY c.username 
                       ORDER BY seat_count DESC;''')
        
        person = cursor.fetchone()
        list = {'name':person[0],'amount':person[1]}
        return list
    
# seatDB = SeatDB()


# seatDB.displaySeats()