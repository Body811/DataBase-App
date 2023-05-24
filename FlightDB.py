
import pyodbc
from SeatDB import SeatDB
from AircraftDB import AircraftDB

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

seatDB = SeatDB()
aircraftdb = AircraftDB()

class Flight:
    def __init__(self, id, aircraftId, departureDate ,arrivalDate , source, destination, price):
        self.id = id
        self.aircraftId = aircraftId
        self.departureDate = departureDate
        self.arrivalDate = arrivalDate
        self.source = source
        self.destination = destination
        self.price = price




class FlightDB:
    def __init__(self):
        self.flights = []
        try:
            cursor.execute("""IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'FlightDB')
                                    CREATE TABLE FlightDB (
                                    id INT PRIMARY KEY,
                                    aircraftId INT,
                                    departureDate datetime,
                                    arrivalDate datetime,
                                    source VARCHAR(50),
                                    price INT,
                                    destination VARCHAR(50),
                                    FOREIGN KEY (aircraftId) REFERENCES AircraftDB(id) ON DELETE SET NULL
                                );     
                            """)

        except pyodbc.Error as e:
            print(f"Error Creating FlightDB Table: {e}")

        self.refreshDB()

    def refreshDB(self):
        self.flights.clear()
        try:
            cursor.execute("SELECT id, aircraftId, departureDate, arrivalDate,  source, destination, price FROM FlightDB")
            rows = cursor.fetchall()
            for row in rows:
                flight = Flight(row.id,row.aircraftId,row.departureDate,row.arrivalDate,row.source,row.destination,row.price)
                self.flights.append(flight)
        except pyodbc.Error as e:
            print(f"Error Refreshing FlightDB: {e}")

    def addFlight(self, id, aircraftId, departureDate, arrivalDate, source, destination, price):
        flag = True
        if self.flights:
            for f in self.flights:
                if f.id == id:
                    flag = False
                    break

        if flag:
            try:
                flight = Flight(id, aircraftId, departureDate, arrivalDate, source, destination,price)
                print(f"2 {id}, {aircraftId}, {departureDate}, {arrivalDate}, {source}, {destination},{price}")
                cursor.execute("INSERT INTO FlightDB(id, aircraftId, departureDate, arrivalDate, source, destination,price) VALUES (?, ?, ?, ?, ?, ?, ?)",(flight.id,flight.aircraftId,flight.departureDate,flight.arrivalDate,flight.source,flight.destination,flight.price))
                conn.commit()
                self.flights.append(flight)
                bussinesSeatNum = aircraftdb.getBussinesSeatNum(int(aircraftId))
                economySeatNum = aircraftdb.getEconomySeatNum(int(aircraftId))
                print(f"3 {bussinesSeatNum}  {economySeatNum}")
                seatDB.addSeats(id, aircraftId, bussinesSeatNum, economySeatNum)
                print("Flight added successfully")
                return True
            except pyodbc.Error as e:
                print(f"Error Adding Flight: {e}")
                return False
        else:
            print(f"Flight with ID {id} already exists")
            return False

    def updateFlight(self, id, attribute, value):
        flag = False
        for f in self.flights:
            if f.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute(
                    f"""UPDATE FlightDB SET {attribute} = ?
                                WHERE id = ?
                                """,(value, id))
                conn.commit()

                self.refreshDB()
                print(f"Flight {attribute} updated successfully.")
            except pyodbc.Error as e:
                print(f"Error updating flight: {e}")
        else:
            print(f"Flight with ID {id} does not exist.")

    def removeFlight(self, id):
        flag = False
        for f in self.flights:
            if f.id == id:
                flag = True
                break

        if flag:
            try:
                cursor.execute("DELETE FROM FlightDB WHERE id = ?", (id,))
                conn.commit()

                self.flights.remove(f)

                print("Flight deleted successfully.")
            except pyodbc.Error as e:
                print(f"Error deleting flight: {e}")
        else:
            print(f"Flight with ID {id} does not exist.")

    def displayFlights(self):
        if not self.flights:
            print("Flights database is empty.")
        else:
            print(f"{'ID':<10}{'Aircraft ID':^20}{'Departure Date':^20}{'Arrival Date':^20}{'Source':^20}{'Destination':^20}{'Price':^20}")
            for f in self.flights:
                print(f"{f.id:<10}{str(f.aircraftId):^20}{str(f.departureDate):^20}{str(f.arrivalDate):^20}{f.source:^20}{f.destination:^20}{f.price:^20}")

    def checkFlightExists(self, id):
        for f in self.flights:
            if f.id == id:
                return True
        return False
    
    def getFlights(self, source, destination, classType, requiredSeats):
        
        result = []
        for f in self.flights:
            availableSeats = seatDB.getAvailableSeats(f.aircraftId, classType)
            if f.source.lower() == source.lower() and f.destination.lower() == destination.lower() and int(availableSeats) >= int(requiredSeats):
                result.append({
                    'id': f.id, 
                    'departureDate': str(f.departureDate), 
                    'arrivalDate': str(f.arrivalDate), 
                    'source': f.source, 
                    'destination': f.destination,
                    'availableSeats': availableSeats, 
                    'price': f.price})
        return result

    
    def adminGetFlights(self,source,destination):
        result = []
        print(source)
        print(destination)
        try:
            cursor.execute("""SELECT FlightDB.id, FlightDB.aircraftId, FlightDB.departureDate, FlightDB.arrivalDate, FlightDB.source, FlightDB.destination,FlightDB.price,
                            AircraftDB.model, AircraftDB.bussinesSeatNum ,AircraftDB.economySeatNum
                           FROM FlightDB 
                           FULL JOIN AircraftDB
                           ON FlightDB.aircraftId = AircraftDB.id
                           """)
            rows = cursor.fetchall()
            for d in rows:
                if str(d.source).lower() == source.lower() and str(d.destination).lower() == destination.lower():
                    result.append({
                        'flightid': str(d.id), 
                        'departureDate': str(d.departureDate), 
                        'arrivalDate': str(d.arrivalDate), 
                        'source': d.source, 
                        'destination': d.destination,
                        'price': d.price,
                        'aircraftId': str(d.aircraftId), 
                        'model': d.model, 
                        'bussinesSeats': d.bussinesSeatNum, 
                        'economySeats': d.economySeatNum, 
                        })
                    
            return result
        except pyodbc.Error as e:
            print(f"Error Collecting Data: {e}")
    
    
    
    
    def getAllFlightData(self):
        result = []

        try:
            cursor.execute("""SELECT FlightDB.id, FlightDB.aircraftId, FlightDB.departureDate, FlightDB.arrivalDate, FlightDB.source, FlightDB.destination,FlightDB.price,
                           AircraftDB.model, AircraftDB.bussinesSeatNum ,AircraftDB.economySeatNum
                           FROM FlightDB 
                           FULL JOIN AircraftDB
                           ON FlightDB.aircraftId = AircraftDB.id
                           """)
            rows = cursor.fetchall()
            for d in rows:
                result.append({
                    'flightid': d.id, 
                    'departureDate': str(d.departureDate), 
                    'arrivalDate': str(d.arrivalDate), 
                    'source': d.source, 
                    'destination': d.destination,
                    'price': d.price,
                    'aircraftId': d.aircraftId, 
                    'model': d.model, 
                    'bussinesSeats': d.bussinesSeatNum, 
                    'economySeats': d.economySeatNum, 
                    })
            return result
        except pyodbc.Error as e:
            print(f"Error Collecting Data: {e}")

       
    
    def getAircraftId(self, flightId):
        for f in self.flights:
            if f.id == flightId:
                return f.aircraftId

    
    def clearDB(self):
        try:
            cursor.execute(f"DELETE FROM FlightDB")
            self.flights.clear()
            print("Flights database cleared successfully.")
        except pyodbc.Error as e:
            print(f"Error clearing flights database: {e}")
            
    def getFlightQuantity(self):
        cursor.execute('SELECT COUNT(*) FROM FlightDB')
        count = cursor.fetchone()[0]
        return count

# flightdb = FlightDB() 

# flightdb.addFlight(0,0,'2022-05-10 09:00:00','2022-05-10 12:00:00','Egypt','Colombia',69)

# flightdb.refreshDB()
# flightdb.removeFlight(0)
# flightdb.displayFlights()

