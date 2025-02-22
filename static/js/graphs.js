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

function changeBarXColumnOptions() {
  let input = document.getElementById("bar_x_data").value;

  if (input === "colour identity") {
    document.getElementById("bar_x_type").setAttribute("list","colour_identity_type");
  }
  else {
    document.getElementById("bar_x_type").setAttribute("list",input.concat("_type"));
  }
}

function changeBarYColumnOptions() {
  let input = document.getElementById("bar_y_data").value;

  if (input === "colour identity") {
    document.getElementById("bar_y_type").setAttribute("list","colour_identity_type");
  }
  else {
    document.getElementById("bar_y_type").setAttribute("list",input.concat("_type"));
  }
}

function changePieDivisionsOptions() {
  let input = document.getElementById("pie_data").value;

  if (input === "colour identity") {
    document.getElementById("pie_divisions").setAttribute("list","colour_identity_type");
  }
  else {
    document.getElementById("pie_divisions").setAttribute("list",input.concat("_type"));
  }
}
