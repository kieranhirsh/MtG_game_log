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
    document.getElementById("bar_x").setAttribute("list", "deck_bins_and_x_axis");
    document.getElementById("bar_y").setAttribute("list", "deck_y_axis");
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
    document.getElementById("line_x").setAttribute("list", "line_x_axis");
    document.getElementById("line_y").setAttribute("list", "line_y_axis");
    DivDeck.style.display = "block";
    DivPlayer.style.display = "none";
  } else if (input === "player") {
    document.getElementById("line_x").setAttribute("list", "line_x_axis");
    document.getElementById("line_y").setAttribute("list", "line_y_axis");
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
    document.getElementById("pie_divisions").setAttribute("list", "deck_bins_and_x_axis");
  } else {
    document.getElementById("pie_divisions").removeAttribute("list");
  }
}

function addDeck() {
  let DivDeckInput = document.getElementById("deck_input");
  let AddButton = document.getElementById("add_deck");
  let RemoveButton = document.getElementById("remove_deck");

  const newLabel = document.createElement("label");
  newLabel.setAttribute("for", "line_deck");
  newLabel.innerHTML = "Deck: ";

  const newInput = document.createElement("input");
  newInput.id = "line_deck";
  newInput.setAttribute("type", "search");
  newInput.setAttribute("name", "line_deck");
  newInput.setAttribute("list", "decks");
  newInput.setAttribute("autocomplete", "off");

  DivDeckInput.insertBefore(newInput, AddButton);
  DivDeckInput.insertBefore(newLabel, newInput);
  DivDeckInput.insertBefore(document.createElement("br"), newLabel);

  if (RemoveButton === null) {
    const NewRemoveButton = document.createElement("button");
    NewRemoveButton.setAttribute("type", "button");
    NewRemoveButton.setAttribute("id", "remove_deck");
    NewRemoveButton.setAttribute("onclick", "removeDeck()");
    NewRemoveButton.innerHTML = "-";
    DivDeckInput.insertAdjacentElement('beforeend', NewRemoveButton);
  }
}

function removeDeck() {
  let Label = document.querySelector("[for='line_deck']");
  let Input = document.getElementById("line_deck");
  let DivInput = document.getElementById("deck_input");
  let Break = DivInput.getElementsByTagName("br");
  let RemoveButton = document.getElementById("remove_deck");

  Label.remove();
  Input.remove();
  Break[0].remove();
  if (Break.length === 0) {
    RemoveButton.remove();
  }
}

function addPlayer() {
  let DivPlayerInput = document.getElementById("player_input");
  let AddButton = document.getElementById("add_player");
  let RemoveButton = document.getElementById("remove_player");

  const newLabel = document.createElement("label");
  newLabel.setAttribute("for", "line_player");
  newLabel.innerHTML = "Player: ";

  const newInput = document.createElement("input");
  newInput.id = "line_player";
  newInput.setAttribute("type", "search");
  newInput.setAttribute("name", "line_player");
  newInput.setAttribute("list", "players");
  newInput.setAttribute("autocomplete", "off");

  DivPlayerInput.insertBefore(newInput, AddButton);
  DivPlayerInput.insertBefore(newLabel, newInput);
  DivPlayerInput.insertBefore(document.createElement("br"), newLabel);

  if (RemoveButton === null) {
    const NewRemoveButton = document.createElement("button");
    NewRemoveButton.setAttribute("type", "button");
    NewRemoveButton.setAttribute("id", "remove_player");
    NewRemoveButton.setAttribute("onclick", "removePlayer()");
    NewRemoveButton.innerHTML = "-";
    DivPlayerInput.insertAdjacentElement('beforeend', NewRemoveButton);
  }
}

function removePlayer() {
  let Label = document.querySelector("[for='line_player']");
  let Input = document.getElementById("line_player");
  let DivInput = document.getElementById("player_input");
  let Break = DivInput.getElementsByTagName("br");
  let RemoveButton = document.getElementById("remove_player");

  Label.remove();
  Input.remove();
  Break[0].remove();
  if (Break.length === 0) {
    RemoveButton.remove();
  }
}
