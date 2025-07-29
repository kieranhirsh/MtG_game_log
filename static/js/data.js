function toggleDataType() {
  let DivMenu = document.getElementById("menu");
  let DataType = document.getElementById("data_types").value;
  let DivColourIdentity = document.getElementById("colour_identity");
  let DivDeck = document.getElementById("deck");
  let DivGame = document.getElementById("game");
  let DivPlayer = document.getElementById("player");

  DivMenu.style.display = "block";
  switch (DataType) {
    case "colour_identity":
      DivColourIdentity.style.display = "block";
      DivDeck.style.display = "none";
      DivGame.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "deck":
      DivDeck.style.display = "block";
      DivColourIdentity.style.display = "none";
      DivGame.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "game":
      DivGame.style.display = "block";
      DivDeck.style.display = "none";
      DivColourIdentity.style.display = "none";
      DivPlayer.style.display = "none";
      break;
    case "player":
      DivPlayer.style.display = "block";
      DivColourIdentity.style.display = "none";
      DivDeck.style.display = "none";
      DivGame.style.display = "none";
      break;
  }
}

function sortTable(n) {
  var table, rows, switching, noswitch, i, x, y, header, shouldSwitch, dir, switchcount = 0;
  table = document.getElementsByClassName("data_table");
  switching = true;
  noswitch = true;
  header = table[0].rows[0].getElementsByTagName("th")[n].innerHTML;
  // If the row is "Win Rate", we need to remove the trailing % to be able to convert to a int
  if (header === "Win Rate") {
    for (i = 1; i < (table[0].rows.length); i++) {
      x = table[0].rows[i].getElementsByTagName("td")[n];
      x.innerHTML = x.innerHTML.slice(0, -1);
    }
  }
  // If the row is "Popularity", we need to remove the trailing % to be able to convert to a int
  if (header === "Popularity") {
    for (i = 1; i < (table[0].rows.length); i++) {
      x = table[0].rows[i].getElementsByTagName("td")[n];
      x.innerHTML = x.innerHTML.slice(1);
    }
  }
  // Set the sorting direction:
  if (
    header === "# Decks" ||
    header === "Games Played" ||
    header === "Games Won" ||
    header === "Win Rate" ||
    header === "Date" ||
    header === "Start Time" ||
    header === "Game Length (Time)" ||
    header === "Game Length (Turns)" ||
    header === "Ave Game Time" ||
    header === "# EDHrec Decks"
  ) {
    dir = "desc";
  } else {
    dir = "asc";
  }
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table[0].rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("td")[n];
      y = rows[i + 1].getElementsByTagName("td")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (y.innerHTML.toLowerCase() == 0) {
          // If the second element is zero, we don't want to switch, but we also want to keep the loop going:
          if (i == (rows.length - 2)) {
            // If we've reached the end of the list, however, we do want to break the loop:
            switching = false;
            break;
          }
          switching = true;
          continue;
        }
        // Check whether the data is a number or a string
        if (
          header === "# Decks" ||
          header === "Games Played" ||
          header === "Games Won" ||
          header === "Win Rate" ||
          header === "Game Length (Turns)" ||
          header === "# EDHrec Decks" ||
          header === "Popularity"
        ) {
          if (parseInt(x.innerHTML) > parseInt(y.innerHTML) || parseInt(x.innerHTML) == 0 || isNaN(parseInt(x.innerHTML))) {
            // If we want to switch, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase() || x.innerHTML.toLowerCase() == 0) {
            // If we want to switch, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      } else if (dir == "desc") {
        // Check whether the data is a number or a string
        if (
          header === "# Decks" ||
          header === "Games Played" ||
          header === "Games Won" ||
          header === "Win Rate" ||
          header === "Game Length (Turns)" ||
          header === "# EDHrec Decks" ||
          header === "Popularity"
        ) {
          if (isNaN(parseInt(y.innerHTML))) {
            // skip this case
            continue;
          }
          if (parseInt(x.innerHTML) < parseInt(y.innerHTML) || isNaN(parseInt(x.innerHTML))) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done, swap the direction and run the while loop again.
         noswitch is here to ensure we don't have an infinite loop. */
      if (switchcount == 0 && noswitch) {
        if (dir == "asc") {
          dir = "desc";
          switching = true;
          noswitch = false;
        } else if (dir == "desc") {
          dir = "asc";
          switching = true;
          noswitch = false;
        }
      }
    }
  }
  // If the row is "Win Rate", we need to add the trailing % back
  if (header === "Win Rate") {
    for (i = 1; i < (table[0].rows.length); i++) {
      x = table[0].rows[i].getElementsByTagName("td")[n];
      x.innerHTML = x.innerHTML + "%";
    }
  }
  // If the row is "Popularity", we need to add the leading # back
  if (header === "Popularity") {
    for (i = 1; i < (table[0].rows.length); i++) {
      x = table[0].rows[i].getElementsByTagName("td")[n];
      if (x.innerHTML) {
        x.innerHTML = "#" + x.innerHTML;
      }
    }
  }
}

function sortColourTables(col) {
  var table, rows, switching, noswitch, header, i, x, y, shouldSwitch, dir, switchcount;
  for (var tab = 1; tab < 5; tab++) {
    table = document.getElementById(tab + "_colours_table");
    switching = true;
    noswitch = true;
    header = table.rows[0].getElementsByTagName("th")[col].innerHTML;
    // If the row is "Win Rate", we need to remove the trailing % to be able to convert to a int
    if (header === "Win Rate") {
      for (i = 2; i < (table.rows.length); i++) {
        x = table.rows[i].getElementsByTagName("td")[col];
        x.innerHTML = x.innerHTML.slice(0, -1);
      }
    }
    // Initialise some values:
    if (
      header === "# Decks" ||
      header === "Games Played" ||
      header === "Games Won" ||
      header === "Win Rate" ||
      header === "Ave Game Time"
    ) {
      dir = "desc";
    } else {
      dir = "asc";
    }
    switchcount = 0;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 2; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[i].getElementsByTagName("td")[col];
        y = rows[i + 1].getElementsByTagName("td")[col];
        /* Check if the two rows should switch place,
        based on the direction, asc or desc: */
        if (dir == "asc") {
          if (y.innerHTML.toLowerCase() == 0) {
            // If the second element is zero, we don't want to switch, but we also want to keep the loop going:
            if (i == (rows.length - 2)) {
              // If we've reached the end of the list, however, we do want to break the loop:
              switching = false;
              break;
            }
            switching = true;
            continue;
          }
          // Check whether the data is a number or a string
          if (
            header === "# Decks" ||
            header === "Games Played" ||
            header === "Games Won" ||
            header === "Win Rate"
          ) {
            if (parseInt(x.innerHTML) > parseInt(y.innerHTML) || parseInt(x.innerHTML) == 0) {
              // If we want to switch, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          } else {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase() || x.innerHTML.toLowerCase() == 0) {
              // If we want to switch, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
        } else if (dir == "desc") {
          // Check whether the data is a number or a string
          if (
            header === "# Decks" ||
            header === "Games Played" ||
            header === "Games Won" ||
            header === "Win Rate"
          ) {
            if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          } else {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        // Each time a switch is done, increase this count by 1:
        switchcount++;
      } else {
        /* If no switching has been done, swap the direction and run the while loop again.
           noswitch is here to ensure we don't have an infinite loop. */
        if (switchcount == 0 && noswitch) {
          if (dir == "asc") {
            dir = "desc";
            switching = true;
            noswitch = false;
          } else if (dir == "desc") {
            dir = "asc";
            switching = true;
            noswitch = false;
          }
        }
      }
    }
    // If the row is "Win Rate", we need to add the trailing % back
    if (header === "Win Rate") {
      for (i = 2; i < (table.rows.length); i++) {
        x = table.rows[i].getElementsByTagName("td")[col];
        x.innerHTML = x.innerHTML + "%";
      }
    }
  }
}

function toggleColumn(col) {
  let checkbox = document.getElementById(col);
  let rows = document.getElementsByClassName(col);

  for (let row of rows) {
    if (checkbox.checked) {
      row.style.display = "table-cell";
    }
    else {
      row.style.display = "none";
    }
  }
}
