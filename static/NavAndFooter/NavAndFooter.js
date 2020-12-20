// nav animation
const navActive = () => {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");
    const navList = document.querySelectorAll(".nav-links li");
  
    burger.addEventListener("click", () => {
      console.log(1);
      if (nav.style.animation) {
        nav.style.animation = "";
        nav.classList.add("nav-deactivate");
        // nav.style.animation = `navslideDeactivate 0.6s ease-in forwards`;
      } else {
        nav.classList.remove("nav-deactivate");
        nav.style.animation = `navslideActive 0.6s ease-in forwards`;
      }
  
      navList.forEach((link, index) => {
        if (link.style.animation) {
          link.style.animation = "";
        } else {
          link.style.animation = `navLinkFade 0.6s ease-in forwards ${
            index / 7 + 0.5
          }s`;
        }
      });
    });
  };
  
navActive();
  
// scroll animation

window.addEventListener("scroll", () => {
    var navLinks = document.querySelector("nav");
    navLinks.classList.toggle("sticky-nav", window.scrollY > 0);
});

const userImage = document.querySelector(".image");
const dropdown = document.querySelector(".dropdown");

// dropdown animation
userImage.addEventListener("click", () => {
    dropdown.classList.toggle("dropdownactive");
});