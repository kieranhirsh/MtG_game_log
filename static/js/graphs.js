function toggleGraphType() {
  let DivMenu = document.getElementById("menu");
  let DataType = document.getElementById("data_types").value;
  let DivBar = document.getElementById("bar");
  let DivPie = document.getElementById("pie");

  DivMenu.style.display = "block";
  switch (DataType) {
    case "bar":
      DivBar.style.display = "block";
      DivPie.style.display = "none";
      break;
    case "pie":
      DivPie.style.display = "block";
      DivBar.style.display = "none";
      break;
  }
}
