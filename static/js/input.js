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
