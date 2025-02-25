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

function changeBarColumnOptions() {
  let input = document.getElementById("bar_data").value;

  if (input === "deck") {
    document.getElementById("bar_x").setAttribute("list","deck_bins_and_x_axis");
    document.getElementById("bar_y").setAttribute("list","deck_y_axis");
  }
  else {
    document.getElementById("bar_x").removeAttribute("list");
    document.getElementById("bar_y").removeAttribute("list");
  }
}

function changePieDivisionsOptions() {
  let input = document.getElementById("pie_data").value;

  if (input === "deck") {
    document.getElementById("pie_divisions").setAttribute("list","deck_bins_and_x_axis");
  }
  else {
    document.getElementById("pie_divisions").removeAttribute("list");
  }
}
