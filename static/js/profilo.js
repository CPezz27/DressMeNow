// Funzione per gestire il clic sulle icone nella barra laterale
document.querySelectorAll('.nav-profilo a').forEach((link, index) => {
  link.addEventListener('click', () => {
    // Nascondi tutti i contenuti
    document.querySelectorAll('.profile, .addresses, .subscription, .privacy, .settings')
      .forEach(content => {
        content.classList.add('noshow');
      });

      //reindirizza alle pagine html desiderate
      switch (index) {
        case 0:
          window.location.href = '/p/profilo';
          break;
        case 1:
          window.location.href = '/p/indirizzi';
          break;
        case 2:
          window.location.href = '/p/ordini';
          break;
        case 3:
          window.location.href = '/p/modifica_avatar';
          break;
        case 4:
          window.location.href = '/p/impostazioni';
          break;
      }

    // Aggiungi la classe 'active' all'icona cliccata
    document.querySelectorAll('nav a').forEach(navLink => {
      navLink.classList.remove('active');
    });
    link.classList.add('active');
  });
});