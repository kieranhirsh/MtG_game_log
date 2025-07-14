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
  let RemoveButton = document.getElementById("remove_player");
  let RemoveOnClick = RemoveButton.getAttribute("onclick");
  let AddButton = document.getElementById("add_player");
  let AddOnClick = AddButton.getAttribute("onclick");

  const newDiv = document.createElement("div");
  newDiv.id = "player_" + n;
  newDiv.innerHTML = `
    <br>Player ${n}: 
    <label for="game_decks">Deck: </label>
    <input type="search" id="game_decks" name="game_decks" list="decks" autocomplete="off" required>
    <label for="game_players">Player: </label>
    <input type="search" id="game_players" name="game_players" list="players" autocomplete="off" required>
    <label for="game_ko_turns">KO Turn (leave blank for winner): </label>
    <input type="text" id="game_ko_turns" name="game_ko_turns" autocomplete="off">
  `;
  DivSeats.insertBefore(newDiv, RemoveButton);

  RemoveButton.textContent = RemoveButton.textContent.replace(n - 1, n);
  RemoveButton.setAttribute("onclick", RemoveOnClick.replace(n - 1, n));

  AddButton.textContent = AddButton.textContent.replace(n, n + 1);
  AddButton.setAttribute("onclick", AddOnClick.replace(n, n + 1));
}

function removePlayer(n) {
  if (n > 0) {
    let DivPlayer = document.getElementById("player_" + String(n));
    let RemoveButton = document.getElementById("remove_player");
    let RemoveOnClick = RemoveButton.getAttribute("onclick");
    let AddButton = document.getElementById("add_player");
    let AddOnClick = AddButton.getAttribute("onclick");

    DivPlayer.remove();

    RemoveButton.textContent = RemoveButton.textContent.replace(n, n - 1);
    RemoveButton.setAttribute("onclick", RemoveOnClick.replace(n, n - 1));

    AddButton.textContent = AddButton.textContent.replace(n + 1, n);
    AddButton.setAttribute("onclick", AddOnClick.replace(n + 1, n));
  }
}
