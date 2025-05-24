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
