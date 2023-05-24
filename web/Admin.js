 


let customerId = localStorage.getItem('customerId') 
 
 //Changes the Navbar When You Start Scrolling 
window.addEventListener('scroll', function () {
    let header = document.querySelector('nav');
    let windowPosition = window.scrollY > 50;
    header.classList.toggle('scrolled-nav', windowPosition);
})



//Blures the Image if You Scrolled Far Enough
window.addEventListener('scroll', () => {
    let img = document.querySelector('.background')
    let text = document.querySelector('.main-text')
    let scrollPos = window.scrollY > 250;
    img.classList.toggle('background-blurred',scrollPos);
    text.classList.toggle('background-blurred',scrollPos);
});



function showAircraftContainer(){
    
    document.querySelector(".add-aircraft-container").style.opacity = 1;
    document.querySelector(".add-aircraft-container").style.top = '160%';
    hideSearchTable()
    hideStatisticsContainer()
    hideAircraftUpdateContainer()
    hideFlightContainer()

    consol.log(document.querySelector('.success-message'))
}


function showAircraftUpdateContainer(){
    
    document.querySelector(".update-aircraft-container").style.opacity = 1
    document.querySelector(".update-aircraft-container").style.top = '160%';
    hideSearchTable()
    hideStatisticsContainer()
    hideAircraftContainer()
    hideFlightContainer()
}

function showFlightContainer(){
    document.querySelector(".add-flight-container").style.opacity = 1;
    document.querySelector(".add-flight-container").style.top = '160%';
    hideSearchTable()
    hideStatisticsContainer()
    hideAircraftUpdateContainer()
    hideAircraftContainer()
}

hideAircraftContainer()
hideAircraftUpdateContainer()
hideFlightContainer()
hideStatisticsContainer()
hideSearchTable()

function hideAircraftContainer(){

    document.querySelector(".add-aircraft-container").style.opacity = 0;
    document.querySelector(".add-aircraft-container").style.top = '0';

}

function hideAircraftUpdateContainer(){
    document.querySelector(".update-aircraft-container").style.opacity = 0;
    document.querySelector(".update-aircraft-container").style.top = '0';

}

function hideFlightContainer(){
    document.querySelector(".add-flight-container").style.opacity = 0;
    document.querySelector(".add-flight-container").style.top = '0'

}

function hideStatisticsContainer(){
    document.querySelector(".statistics-table-container").style.opacity = 0;
    document.querySelector(".statistics-table-container").style.top = '0';

}

function hideSearchTable(){
    document.querySelector(".search-table").style.opacity = 0;
    document.querySelector(".search-table").style.top = '0';

}





// async function getFlights(from, to) {
//     let f = await eel.getFlights(from, to)();
//     return f
// }


async function getAllFlightData() {
    let f = await eel.getAllFlightData()();
    return f
}

async function adminGetFlights(from,to) {
    let f = await eel.adminGetFlights(from,to)();
    return f
}




//Displays Search Results In Table
button = document.querySelector('.search-btn');
button.addEventListener("click", async (event) => {
    event.preventDefault();
    form = document.querySelector('.search');
    let formdata = new FormData(form);
    let from = formdata.get("from");
    let to = formdata.get("to");
    let flights
    console.log(from)
    console.log(to)
    if(from == "" && to == "" ){
        flights = await getAllFlightData()
    }else{
        flights = await adminGetFlights(from,to);
    }
    let table = document.querySelector(".search-table");
    let tbody = table.getElementsByTagName("tbody")[0];
    let error = document.querySelector('.search-error');

    
    //to clear the table from the past searches
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    //adds info if it exists
    if(flights.length > 0){
        for (let i = 0; i < flights.length; i++) {
            let flight = flights[i];
            let row = document.createElement("tr");
            row.innerHTML = "<td>" + flight.flightid + "</td>" +
                            "<td>" + flight.source + "</td>" +
                            "<td>" + flight.destination + "</td>" +
                            "<td>" + flight.departureDate + "</td>" +
                            "<td>" + flight.arrivalDate + "</td>" +
                            "<td>" + flight.price + "</td>" +
                            "<td>" + flight.aircraftId  + "</td>" +
                            "<td>" + flight.model + "</td>" +
                            "<td>" + flight.bussinesSeats + "</td>" +
                            "<td>" + flight.economySeats+ "</td>";
             tbody.appendChild(row);
            }
            error.style.opacity = 0;
            table.style.opacity = 1;    
            document.querySelector('.table-container').style.top = '115%';
    }else{
        error.style.opacity = 1; 
        hideSearchTable()
    }


});


async function addAircraft(aircraftId,model,bussinesSeatNum,economySeatNum) {
   return await eel.addAircraft(aircraftId,model,bussinesSeatNum,economySeatNum)();

}

aircraftbtn = document.querySelector('.add-aircraft-btn')
aircraftbtn.addEventListener("click",  async () => {
    let form = document.querySelector(".add-aircraft-form")
    let formdata = new FormData(form);
    let aircraftId = formdata.get("aircraftId");
    let model = formdata.get("model");
    let bussinesSeatNum = formdata.get("buss-seat-num");
    let economySeatNum = formdata.get("eco-seat-num");
    console.log(aircraftId)
    let isSuccess = await addAircraft(aircraftId,model,bussinesSeatNum,economySeatNum);
        if (isSuccess) {
            document.querySelector('.success-message').style.opacity = 1;
            setTimeout(() => {document.querySelector('.success-message').style.opacity = 0}, 3000);
            

        } else {
            console.log("Error: could not add aircraft")
        }

})


async function updateAircraft(id,attribute,value) {
    return await eel.updateAircraft(id,attribute,value)();
}
 
form = document.querySelector('.update-aircraft-form')
aircraftUpdatebtn = document.querySelector('.update-aircraft-btn')
aircraftUpdatebtn.addEventListener('click', async () => {

    let formdata = new FormData(form);
    let aircraftId = formdata.get("update-aircraft-id");
    let attribute = formdata.get("attribute");
    let value = formdata.get("value");
    console.log(formdata)
    console.log(aircraftId)
    console.log(attribute)
    console.log(value)
    let isSuccess = await updateAircraft(aircraftId,attribute,value);
    if (isSuccess) {
        document.querySelector('.success-message').style.opacity = 1;
        setTimeout(() => {document.querySelector('.success-message').style.opacity = 0}, 3000);

    } else {
        console.log("Error: could not add aircraft")
    }
})


async function addFlight(id, aircraftId, departureDate, arrivalDate, source, destination,price) {
    return await eel.addFlight(id, aircraftId, departureDate, arrivalDate, source, destination,price)();
 
 }
 
 flightbtn = document.querySelector('.add-flight-btn')
 flightbtn.addEventListener("click",  async () => {
     let form = document.querySelector(".add-flight-form")
     let formdata = new FormData(form);
     let id = formdata.get("flightid");
     let aircraftId = formdata.get("aircraftid");
     let departureDate= formdata.get("departuredate").toString();
     let arrivalDate = formdata.get("arrivaldate").toString();
     let source = formdata.get("source");
     let destination = formdata.get("destination");
     let price = formdata.get("price");
     console.log(id)
     console.log(aircraftId)
     console.log(departureDate)
     console.log(arrivalDate)
     console.log(source)
     console.log(destination)
     console.log(price)
     let isSuccess = await addFlight(id, aircraftId, departureDate, arrivalDate, source, destination,price);
     if (isSuccess) {
        document.querySelector('.success-message').style.opacity = 1;
        setTimeout(() => {document.querySelector('.success-message').style.opacity = 0}, 3000);
        

    } else {
        console.log("Error: could not add aircraft")
    }
 })







async function getStatistics(){


    hideFlightContainer()
    hideAircraftUpdateContainer()
    hideAircraftContainer()
    hideSearchTable()



    let flights = await eel.getstatistics()();
    let test = await eel.getMaxSeat()();
    let table = document.querySelector('.statistics-table')
    let tbody = table.querySelector(".ttbody");

    //adds info if it exists
    console.log(flights)
    console.log(test)

    let row = document.createElement("tr");
    row.innerHTML = "<td>" + flights.aircrafts + "</td>" +
                    "<td>" + flights.flights + "</td>" +
                    "<td>" +flights.customers + "</td>"+
                    "<td>"+flights.admins + "</td>" +
                    "<td>" +flights.seats + "</td>" +
                    "<td>"  +test.amount   + "</td>" +
                    "<td>" +test.name+"</td>";

    tbody.appendChild(row); 
   

    document.querySelector(".statistics-table-container").style.opacity = 1;
    document.querySelector(".statistics-table-container").style.top = '130%';

}

