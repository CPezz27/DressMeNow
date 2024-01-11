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
          window.location.href = '/p/personalizzazioneAvatar';
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

function abilitaModifica(button, e) {
  e.preventDefault();
  var form = button.closest('form');
  var inputs = form.querySelectorAll('.input-text');
  inputs.forEach(function (input) {
    input.readOnly = false;
  });
  var selects = form.querySelectorAll('select');
  selects.forEach(function (select) {
    select.disabled = false;
  });
  button.style.display = 'none';
}
