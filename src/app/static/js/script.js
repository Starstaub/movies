function openCategory(categoryName) {
  var i;
  var x = document.getElementsByClassName("category");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(categoryName).style.display = "block";
}