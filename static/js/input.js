function toggleDataType() {
  let DataType = document.getElementById("data_types").value;
  let DivDeck = document.getElementById("deck");
  let DivGame = document.getElementById("game");
  let DivPlayer = document.getElementById("player");

  switch (DataType) {
    case "deck":
      DivDeck.style.display = "block";
      DivGame.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "game":
      DivGame.style.display = "block";
      DivDeck.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "player":
      DivPlayer.style.display = "block";
      DivDeck.style.display = "none";
      DivGame.style.display = "none";
      break;
  }
}

function addPlayer(n) {
  let DivSeats = document.getElementById("seats");
  let DivPlayer = document.getElementById("player_" + String(n - 1));
  let AddButton = document.getElementById("add_player");
  let AddOnClick = AddButton.getAttribute("onclick");

  const newDiv = document.createElement("div");
  newDiv.id = "player_" + n;
  newDiv.innerHTML = DivPlayer.innerHTML.replace(n - 1, n);

  if (n === 2) {
    DivSeats.insertBefore(newDiv, AddButton);

    const newButton = document.createElement("button");
    newButton.setAttribute("type", "button");
    newButton.setAttribute("id", "remove_player");
    newButton.setAttribute("onclick", `removePlayer(${n})`);
    newButton.innerHTML = `Remove Player ${n}`;

    DivSeats.insertBefore(newButton, AddButton);
    DivSeats.insertBefore(document.createElement("br"), AddButton);
  } else {
    let RemoveButton = document.getElementById("remove_player");
    let RemoveOnClick = RemoveButton.getAttribute("onclick");

    DivSeats.insertBefore(newDiv, RemoveButton);

    RemoveButton.textContent = RemoveButton.textContent.replace(n - 1, n);
    RemoveButton.setAttribute("onclick", RemoveOnClick.replace(n - 1, n));
  }

  AddButton.textContent = AddButton.textContent.replace(n, n + 1);
  AddButton.setAttribute("onclick", AddOnClick.replace(n, n + 1));
}

function removePlayer(n) {
  let DivPlayer = document.getElementById("player_" + String(n));
  let RemoveButton = document.getElementById("remove_player");
  let RemoveOnClick = RemoveButton.getAttribute("onclick");
  let AddButton = document.getElementById("add_player");
  let AddOnClick = AddButton.getAttribute("onclick");

  DivPlayer.remove();

  if (n === 2) {
    if (AddButton.previousSibling.nodeName === "BR") {
      AddButton.previousSibling.remove();
    }
    RemoveButton.remove();
  } else {
    RemoveButton.textContent = RemoveButton.textContent.replace(n, n - 1);
    RemoveButton.setAttribute("onclick", RemoveOnClick.replace(n, n - 1));
  }

  AddButton.textContent = AddButton.textContent.replace(n + 1, n);
  AddButton.setAttribute("onclick", AddOnClick.replace(n + 1, n));
}
