function toggleDataType() {
  let DataType = document.getElementById("data_types").value;
  let DivDeck = document.getElementById("deck");
  let DivGame = document.getElementById("game");
  let DivPlayer = document.getElementById("player");

  if (DataType === "deck") {
    DivDeck.style.display = "block";
    DivGame.style.display = "none";
    DivPlayer.style.display = "none";
  }
  else if (DataType === "game") {
    DivGame.style.display = "block";
    DivDeck.style.display = "none";
    DivPlayer.style.display = "none";
  }
  else if (DataType === "player") {
    DivPlayer.style.display = "block";
    DivDeck.style.display = "none";
    DivGame.style.display = "none";
  }
}
