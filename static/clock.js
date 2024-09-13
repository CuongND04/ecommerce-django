let time = document.querySelector("#clock");
setInterval(() => {
  let date = new Date(); // this is date utility is a default code that is used to time ie years, months, days etc
  let hour =String (date.getHours()%12||12).padStart(2, "0");
    let minute = String(date.getMinutes()).padStart(2, "0");
    let seconds =String (date.getSeconds()).padStart(2, "0");

  time.innerHTML = `${hour}:${minute}:${seconds}`;
}, 1000);

// assignment 
// make hours , minute and sec show 2 digits all  the time


