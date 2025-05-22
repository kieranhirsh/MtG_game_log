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

function uncheckColours() {
  let colouredCheck = Array.from(document.getElementsByClassName('ci_coloured'))
  let colourlessCheck = document.getElementById('colourless')

  colouredCheck.forEach(element => {
      element.onchange = () => {
        colourlessCheck.checked = false;
      }
  })

  colourlessCheck.onchange = () => {
      if (colourlessCheck.checked) {
        colouredCheck.forEach(element => {
              element.checked = false;
          })
      }
  }
}
