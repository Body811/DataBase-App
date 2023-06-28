import eel
import datetime
from AdminDB import AdminDB
from AircraftDB import AircraftDB
from FlightDB import FlightDB
from CustomerDB import CustomerDB
from SeatDB import SeatDB
eel.init('web')


aircraftDB = AircraftDB()
flightDB = FlightDB()
customerDB = CustomerDB()
seatDB = SeatDB()
adminDB = AdminDB()
# aircraftDB.addAircraft(1,"Airjet 69",10,20)
# aircraftDB.addAircraft(0,"boeing 717",50,100)
# aircraftDB.displayAircrafts()
# flightDB.addFlight(0,0,'2022-05-10 09:00:00','2022-05-10 12:00:00','Egypt','Colombia',69)
# flightDB.addFlight(1,0,'2022-05-20 09:00:00','2022-05-20 12:00:00','Egypt','Colombia',69)
# flightDB.addFlight(2,0,'2022-05-30 09:00:00','2022-05-30 12:00:00','Egypt','Colombia',690)
# flightDB.addFlight(3,1,'2022-06-10 09:00:00','2022-06-10 12:00:00','Egypt','Colombia',6900)
# flightDB.addFlight(4,1,'2022-06-11 09:00:00','2022-06-11 12:00:00','Egypt','Colombia',69000)
# flightDB.displayFlights()
# customerDB.addCustomer(0,'Abdo',123,"abdo@gmail.com","2020-10-5")
# customerDB.displayCustomers()
# seatDB.displaySeats()

@eel.expose
def login(name,password):
    return customerDB.checkCustomerlogin(name,password)

@eel.expose
def getCustomerId(name):
    return customerDB.getCustomerId(name)

@eel.expose
def getFlights(source, destination, classType, requiredSeats):
    print(f"{source, destination, classType, requiredSeats}")
    test = flightDB.getFlights(source, destination, classType, requiredSeats)
    print(test)
    return test

@eel.expose
def bookFlight(flightId, customerId, classType, seatNum):
    aircraftId = flightDB.getAircraftId(int(flightId))
    
    print(f"{aircraftId,int(customerId),classType,int(seatNum)}")
    seatDB.bookSeat(aircraftId,int(customerId),classType,int(seatNum))
    
@eel.expose
def getSeats(customerId):
    return seatDB.getSeats(int(customerId))
    
@eel.expose
def addcustomer(name, password, email, birthdate):
    print(f'{name}, {password}, {email}, {birthdate}')
    return customerDB.addCustomer(name, password, email, birthdate)

@eel.expose
def isadmin(username,password):
    # print(username+ " " + password)
    return adminDB.checkAdminLogin(username,password)

@eel.expose
def addAircraft(aircraftId,model,bussinesSeatnum,economySeatNum):
    # print(aircraftId)
    return aircraftDB.addAircraft(int(aircraftId),model,int(bussinesSeatnum),int(economySeatNum))

@eel.expose
def getAllFlightData():
    f = flightDB.getAllFlightData()
    # print(f)
    return f


@eel.expose
def adminGetFlights(source,destination):
    f = flightDB.adminGetFlights(source,destination)
    # print(f)
    return f


@eel.expose
def updateAircraft(id,attribute,value):
    print(f"{id},{attribute},{value}")
    return aircraftDB.updateAircraft(int(id),attribute,value)

@eel.expose
def addFlight(id, aircraftId, departureDate, arrivalDate, source, destination,price):
    # Create a datetime object from the string value
    newdepartureDate = datetime.datetime.fromisoformat(departureDate)
    newarrivalDate = datetime.datetime.fromisoformat(arrivalDate)
    # Format the datetime object as a string
    finaldeparturedate = newdepartureDate.strftime('%Y-%m-%d %H:%M:%S')    
    finalarrivaldate = newarrivalDate.strftime('%Y-%m-%d %H:%M:%S')    
    # print(f"1 {id}, {aircraftId}, {departureDate}, {arrivalDate}, {source}, {destination},{price}")
    return flightDB.addFlight(int(id), int(aircraftId), finaldeparturedate,  finalarrivaldate, source, destination,int(price))

@eel.expose
def updateCustomer(id,username,password,email,birthdate):
    
    if username != "":
        customerDB.updateCustomer(int(id),'username',username)
    if password != "":
        customerDB.updateCustomer(int(id),'password',password)
    if email != "":
        customerDB.updateCustomer(int(id),'email',email)
    if birthdate != "":
        customerDB.updateCustomer(int(id),'birthdate',birthdate)
    return

@eel.expose
def getstatistics():
    stat = {'aircrafts': aircraftDB.getAircraftQuantity(),
            'flights': flightDB.getFlightQuantity(),
            'customers': customerDB.getCustomerQuantity(),
            'admins':adminDB.getAdminQuantity(),
            'seats':seatDB.getSeatQuantity()}
    return stat


@eel.expose 
def getMaxSeat():
    return seatDB.getMaxSeat()            

eel.start('login.html',)


