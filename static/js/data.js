function toggleDataType() {
  let DivMenu = document.getElementById("menu");
  let DataType = document.getElementById("data_types").value;
  let DivColourIdentity = document.getElementById("colour_identity");
  let DivDeck = document.getElementById("deck");
  let DivPlayer = document.getElementById("player");

  DivMenu.style.display = "block";
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

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementsByClassName("data_table");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
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
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase() || x.innerHTML.toLowerCase() == 0) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
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
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function sortColourTables(col) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount;
  for (var tab = 1; tab < 5; tab++) {
    table = document.getElementById(tab + "_colours_table");
    switching = true;
    // Initialise some values:
    dir = "asc";
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
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase() || x.innerHTML.toLowerCase() == 0) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
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
        /* If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again. */
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }
}
