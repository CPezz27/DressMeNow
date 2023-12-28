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