// test login
const loginAs = (role) => {
  usernameField = document.querySelector('input[name="username"]');
  passwordField = document.querySelector('input[name="password"]');

  if (role === "admin") {
    usernameField.value = "admin";
    passwordField.value = "1234";
  }
  if (role === "organizer") {
    usernameField.value = "organizer";
    passwordField.value = "testUser@12";
  }
  if (role === "user") {
    usernameField.value = "user";
    passwordField.value = "testUser@12";
  }

  document.querySelector("form").submit();
};

// get the current year
document.getElementById("year").textContent = new Date().getFullYear();

// navbar background color changed in details page
const navbar = document.getElementById("main-navbar");
// scroll to top function
const scrollTopButton = document.getElementById("scrollTopButton");

if (window.location.pathname.includes("/event-details/")) {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      // Navbar style on scroll
      navbar.classList.add("bg-white", "text-black", "shadow-sm");
      navbar.classList.remove("bg-transparent", "text-white");
    } else {
      // Reset to transparent
      navbar.classList.remove("bg-white", "text-black", "shadow-sm");
      navbar.classList.add("bg-transparent", "text-white");
    }
  });
}
window.addEventListener("scroll", () => {
  if (window.scrollY > 50) {
    scrollTopButton.classList.remove("opacity-0", "invisible", "bottom-0");
    scrollTopButton.classList.add("opacity-100", "visible", "bottom-8");
  } else {
    scrollTopButton.classList.remove("opacity-100", "visible", "bottom-8");
    scrollTopButton.classList.add("opacity-0", "invisible", "bottom-0");
  }
});

// initialize swiper
const swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 25,
  autoplay: {
    delay: 2000, // 2 seconds
    disableOnInteraction: false,
  },
  breakpoints: {
    620: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
