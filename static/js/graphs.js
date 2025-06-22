function toggleGraphType() {
  let DivMenu = document.getElementById("menu");
  let GraphType = document.getElementById("graph_types").value;
  let DivBar = document.getElementById("bar");
  let DivLine = document.getElementById("line");
  let DivPie = document.getElementById("pie");

  DivMenu.style.display = "block";
  switch (GraphType) {
    case "bar":
      DivBar.style.display = "block";
      DivLine.style.display = "none";
      DivPie.style.display = "none";
      break;
    case "line":
      DivLine.style.display = "block";
      DivBar.style.display = "none";
      DivPie.style.display = "none";
      break;
    case "pie":
      DivPie.style.display = "block";
      DivBar.style.display = "none";
      DivLine.style.display = "none";
      break;
  }
}

function changeBarColumnOptions() {
  let input = document.getElementById("bar_data").value;

  if (input === "deck") {
    document.getElementById("bar_x").setAttribute("list","deck_bins_and_x_axis");
    document.getElementById("bar_y").setAttribute("list","deck_y_axis");
  } else {
    document.getElementById("bar_x").removeAttribute("list");
    document.getElementById("bar_y").removeAttribute("list");
  }
}

function changeLineColumnOptions() {
  let input = document.getElementById("line_data").value;
  let DivDeck = document.getElementById("deck_input");
  let DivPlayer = document.getElementById("player_input");

  if (input === "deck") {
    document.getElementById("line_x").setAttribute("list","line_x_axis");
    document.getElementById("line_y").setAttribute("list","line_y_axis");
    DivDeck.style.display = "block";
    DivPlayer.style.display = "none";
  } else if (input === "player") {
    document.getElementById("line_x").setAttribute("list","line_x_axis");
    document.getElementById("line_y").setAttribute("list","line_y_axis");
    DivPlayer.style.display = "block";
    DivDeck.style.display = "none";
  } else {
    document.getElementById("line_x").removeAttribute("list");
    document.getElementById("line_y").removeAttribute("list");
    DivDeck.style.display = "none";
    DivPlayer.style.display = "none";
  }
}

function changePieDivisionsOptions() {
  let input = document.getElementById("pie_data").value;

  if (input === "deck") {
    document.getElementById("pie_divisions").setAttribute("list","deck_bins_and_x_axis");
  } else {
    document.getElementById("pie_divisions").removeAttribute("list");
  }
}
