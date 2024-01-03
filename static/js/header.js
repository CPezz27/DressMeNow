function toggleMenu() {
    var dropdownMenu = document.getElementById("dropdownContent");

    if(dropdownMenu.style.display === "none"){
      dropdownMenu.style.display = "flex";
    }else if(dropdownMenu.style.display === "flex" || screen.width >= "480"){
      dropdownMenu.style.display = "none";
    }else{
      dropdownMenu.style.display = "flex";
    }
  }

// Aggiungi event listeners agli elementi per gestire i click
document.addEventListener('DOMContentLoaded', function () {
  const cartIcon = document.querySelector('.icons a[href="#"]');
  const otherCartIcon = document.querySelector('.dropdown-content .cart-link');
  const profileIcon = document.querySelector('.icons a[href="profilo.html"]');
  const otherProfileIcon = document.querySelector('.dropdown-content .profile-link');
  
  if (cartIcon) {
      cartIcon.addEventListener('click', function (event) {
          event.preventDefault();
          goToCartPage();
      });
  }

  if (otherCartIcon) {
    otherCartIcon.addEventListener('click', function (event) {
        event.preventDefault();
        goToCartPage();
    });
}

  if (profileIcon) {
    profileIcon.addEventListener('click', function (event) {
          event.preventDefault();
          goToProfilePage();
      });
  }
  if (otherProfileIcon) {
    otherProfileIcon.addEventListener('click', function (event) {
          event.preventDefault();
          goToProfilePage();
      });
  }
});

  // Funzione per reindirizzare alla pagina del Carrello
  function goToCartPage() {
    window.location.href = "/carrello";
  }
  
  // Funzione per reindirizzare alla pagina del Profilo Utente
  function goToProfilePage() {
    window.location.href = "/p/profilo";
  }