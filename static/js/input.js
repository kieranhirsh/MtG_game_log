function toggleDataType() {
  let DataType = document.getElementById("data_types").value;
  let DivPlayer = document.getElementById("player");
  let DivDeck = document.getElementById("deck");
  

  if (DataType === "player") {
    DivPlayer.style.display = "block";
    DivDeck.style.display = "none";
  }
  else if (DataType === "deck") {
    DivDeck.style.display = "block";
    DivPlayer.style.display = "none";
  }

}