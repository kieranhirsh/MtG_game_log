function toggleDataType() {
  let DataType = document.getElementById("data_types").value;
  let DivColourIdentity = document.getElementById("colour_identity");
  let DivDeck = document.getElementById("deck");
  let DivPlayer = document.getElementById("player");

  switch (DataType) {
    case "colour_identity":
      DivColourIdentity.style.display = "block";
      DivDeck.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "deck":
      DivDeck.style.display = "block";
      DivColourIdentity.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "player":
      DivPlayer.style.display = "block";
      DivColourIdentity.style.display = "none";
      DivDeck.style.display = "none";
      break;
  }
}
