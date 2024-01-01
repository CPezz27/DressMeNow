
/*
function showSection(sectionId) {
    var sections = document.getElementsByClassName("profile-section");
    for (var i = 0; i < sections.length; i++) {
      sections[i].style.display = "none";
    }

    var selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
      selectedSection.style.display = "block";
    }
  }

  */

  // Funzione per gestire il clic sulle icone nella barra laterale
document.querySelectorAll('nav a').forEach((link, index) => {
  link.addEventListener('click', () => {
    // Nascondi tutti i contenuti
    document.querySelectorAll('.profile, .payment, .subscription, .privacy, .settings')
      .forEach(content => {
        content.classList.add('noshow');
      });

    if (index === 0) {
      // Se clicco sulla prima icona, visualizza nuovamente le info dell'utente
      document.querySelector('.profile').classList.remove('noshow');
    } else if (index === 1) {
      // Se clicco sulla seconda icona, mostra i due quadrati neri
      document.querySelector('.payment').classList.remove('noshow');
    } else if (index === 4) {
      // Se clicco sulla seconda icona, mostra i due quadrati neri
      document.querySelector('.settings').classList.remove('noshow');
    } 

    else {
      // Altrimenti, reindirizza alle pagine html desiderate
      switch (index) {
        case 2:
          window.location.href = 'pagina1.html';
          break;
        case 3:
          window.location.href = 'pagina2.html';
          break;
        // Aggiungi altri casi per altre pagine se necessario
        default:
          break;
      }
    }

    // Aggiungi la classe 'active' all'icona cliccata
    document.querySelectorAll('nav a').forEach(navLink => {
      navLink.classList.remove('active');
    });
    link.classList.add('active');
  });
});