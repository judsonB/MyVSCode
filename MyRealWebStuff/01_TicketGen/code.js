function generateTicket(e)
{
    let name = nameInput.value;
    let email = emailInput.value;
    let dates = datesInput.value;
    let numTickets = Number(numTicketsInput.value);
    showOutput.innerHTML = dates;
    emailOutput.innerHTML = email;
    nameOutput.innerHTML = name;
    numTicketsOutput.innerHTML = numTickets;
    formDiv.style.display = "none";
    ticketDiv.style.display = "block";
    rowOutput.innerHTML = random_range(1, 20);
    let seatNum = random_range(1, 30-numTickets);
    if(numTickets > 1)
        seatOutput.innerHTML = seatNum+"-"+(seatNum+numTickets-1);
    else
        seatOutput.innerHTML = seatNum;
    JsBarcode("#barcode", generateBarcodeNumber(), {
        format: "CODE128",
        background: "rgb(255, 255, 231)",
        lineColor: "#000",
        width: 4,
        height: 50,
        displayValue: true
        });
}
function generateBarcodeNumber()
{
    let num="";
    for (var i = 0; i < 10; i++)
        num += random_range(0,9);
    return num;
}
function random_range(low, high)
{
    let size = high - low + 1;
    return Math.floor(Math.random() * size)+low;
}
let nameInput = document.getElementById("name");
let emailInput = document.getElementById("email");
let datesInput = document.getElementById("dates");
let numTicketsInput = document.getElementById("numTickets");
let btn = document.getElementById("order");
let showOutput = document.getElementById("showOutput");
let nameOutput = document.getElementById("nameOutput");
let emailOutput = document.getElementById("emailOutput");
let numTicketsOutput = document.getElementById("numTicketsOutput");
let rowOutput = document.getElementById("rowOutput");
let seatOutput = document.getElementById("seatOutput");

let formDiv = document.getElementById("form");
let ticketDiv = document.getElementById("ticket");

btn.addEventListener("click", generateTicket)
ticketDiv.style.display = "none";