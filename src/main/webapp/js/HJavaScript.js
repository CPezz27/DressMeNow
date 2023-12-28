function toggleMenu() {
    console.log("ciao");
    var dropdownMenu = document.getElementById("dropdownContent");

    if(dropdownMenu.style.display === "none"){
      dropdownMenu.style.display = "flex";
    }else if(dropdownMenu.style.display === "flex" || screen.width >= "480"){
      dropdownMenu.style.display = "none";
    }else{
      dropdownMenu.style.display = "flex";
    }
  }