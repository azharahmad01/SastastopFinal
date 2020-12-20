const signin = document.getElementById("signin");
const signup = document.getElementById("signup");
const container = document.querySelector(".container");
const formContainer = document.querySelector(".form-container");
const arrowsignin = document.getElementById("signinarrownav");
const arrowsignup = document.getElementById("signuparrownav");



// slide animation
width_adjustment();
window.addEventListener("resize", width_adjustment);

function width_adjustment() {
  container.classList.remove("right-panel-active");
  container.classList.remove("slide-registration");
}

// arrow transition

arrowsignin.addEventListener("click", () => {
  container.classList.add("slide-registration");
  localStorage.setItem('signup','false');
  localStorage.setItem('arrowsignin','true');
  console.log(localStorage);
});
arrowsignup.addEventListener("click", () => {
  container.classList.remove("slide-registration");
  localStorage.setItem('arrowsignin','false');
});

// signup and signin animation
signup.addEventListener("click", () => {
  localStorage.setItem('signup','true');
  localStorage.setItem('arrowsignin', 'false');
  console.log(localStorage);
  container.classList.add("right-panel-active");
});
signin.addEventListener("click", () => {
  localStorage.setItem('signup','false');
  console.log(localStorage);
  container.classList.remove("right-panel-active");
});

if(localStorage.getItem('signup') == 'true') {
  console.log(localStorage);
  container.classList.add("right-panel-active");
  
}
else {
  container.classList.remove("right-panel-active");
  
}
if(localStorage.getItem('arrowsignin') == 'true') {
  container.classList.add("slide-registration");
}
else {
  container.classList.remove("slide-registration");
}