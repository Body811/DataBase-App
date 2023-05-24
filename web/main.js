 


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



// Makes Sure the Seat Number Input is not Negative or Decimal
let input = document.querySelector('.seat-num')
input.addEventListener('input', () => {
    let value = input.value.toString();
    console.log(value)
    if (value.includes('.'))  {
        alert('Number of Seats Cant be Decimal')
        input.value = 0;
    }else if(value.includes('-')){
        alert('Number of Seats Cant be Negative')
        input.value = 0;
    }
});



async function getFlights(from, to, classtype, seatNum) {
    let f = await eel.getFlights(from, to, classtype, seatNum)();
    return f
}

//Displays Search Results In Table
form = document.querySelector('.search');
button = document.querySelector('.search-btn');
button.addEventListener("click", async (event) => {
    event.preventDefault();
    let formdata = new FormData(form);
    let from = formdata.get("from");
    let to = formdata.get("to");
    let seatNum = formdata.get("seat-num");
    let classType = formdata.get("class");
    document.querySelector('.seats').innerHTML = "Available "+classType+" Seats";
    let flights = await getFlights(from, to, classType,seatNum);
    let table = document.querySelector(".search-table");
    let tbody = table.getElementsByTagName("tbody")[0];
    let error = document.querySelector('.search-error');
    let booking = document.querySelector('.book-container')
    
    

    //to clear the table from the past searches
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    //adds info if it exists
    if(flights.length > 0){
        for (let i = 0; i < flights.length; i++) {
            let flight = flights[i];
            let row = document.createElement("tr");
            row.innerHTML = "<td>" + flight.id + "</td>" +
                            "<td>" + flight.departureDate + "</td>" +
                            "<td>" + flight.arrivalDate + "</td>" +
                            "<td>" + flight.source + "</td>" +
                            "<td>" + flight.destination + "</td>" +
                            "<td>" + flight.availableSeats + "</td>" +
                            "<td>" + flight.price + "</td>";
            error.style.opacity = 0;
            table.style.opacity = 1;
            booking.style.opacity = 1;
            tbody.appendChild(row);
        }
    }else{
        error.style.opacity = 1; 
        table.style.opacity = 0;
        booking.style.opacity = 0;
    }


});




let fidInput = document.querySelector('.flight-id')
fidInput.addEventListener('input', () => {
    let value = fidInput.value;
    
    let isNumeric = /^\d+$/.test(value);
    if (!isNumeric)  {
        alert('Flight ID Can Only Contains Digits')
        fidInput.value = null;
    }
});




async function bookFlight(flightId,customerId, classType, requiredSeats) { 
   return await eel.getFlights(flightId,customerId, classType, requiredSeats)();
}


bookbtn = document.querySelector('.book-btn');
bookbtn.addEventListener("click", async (event) => {
    event.preventDefault();
    let formdata = new FormData(form);
    let seatNum = formdata.get("seat-num");
    let classType = formdata.get("class");
    let flightId = fidInput.value;
    console.log(flightId);
    console.log(customerId);
    console.log(classType);
    console.log(seatNum);
    await bookFlight(flightId,customerId,classType,seatNum);
    setTimeout(() => {document.querySelector('.success-message').style.opacity = 1;}, 3000);
    document.querySelector('.success-message').style.opacity = 0;
    
});



async function getSeats(){
    console.log("started")
  let seats =  await eel.getSeats(customerId)() 
  console.log(seats)
  let table = document.querySelector(".myflight-table");
  let tbody = table.getElementsByTagName("tbody")[0];
  let editerror = document.querySelector(".edit-error")
  let editContainer = document.querySelector(".edit-container")
  while (tbody.firstChild) {
    tbody.removeChild(tbody.firstChild);
  }


  if(seats.length > 0){
    for (let i = 0; i < seats.length; i++) {
        let seat = seats[i];
        let [flightId] = seat.seatid.split("#")
        let row = document.createElement("tr");
        row.innerHTML = "<td>" + flightId + "</td>" +
                        "<td>" + seat.seatid + "</td>" +
                        "<td>" + seat.classType + "</td>"
                        
        tbody.appendChild(row);
        editerror.style.opacity = 0;
        table.style.opacity = 1;
        editContainer.style.opacity = 1;
    }
}else{
    editerror.style.opacity = 1; 
    table.style.opacity = 0;
    editContainer.style.opacity = 0;
}
}


async function updateCustomer(id,username,password,email,birthdate){
    return await eel.updateCustomer(id,username,password,email,birthdate)();
 }
 


form = document.querySelector('.update-customer-form')
updateCustBtn = document.querySelector('.update-customer-btn')

updateCustBtn.addEventListener("click", async () => {

    let formdata = new FormData(form);
    let username = formdata.get("username");
    let password = formdata.get("password");
    let email = formdata.get("email");
    let birthdate = formdata.get("birthdate");
    
    await updateCustomer(customerId ,username,password,email,birthdate);
    document.querySelector('.success-message').style.opacity = 1;
    setTimeout(() => {document.querySelector('.success-message').style.opacity = 0}, 3000);

})


function showUpdateCustomerContainer(){
    document.querySelector('.update-customer-container').style.opacity = 1
    document.querySelector('.success-message').style.opacity = 0;
    document.querySelector(".search-table").style.opacity = 0;
    document.querySelector('.search-error').style.opacity = 0;
    document.querySelector('.book-container').style.opacity = 0;

}








// window.addEventListener('scroll',() =>{

//   console.log(window.scrollY)

// })

