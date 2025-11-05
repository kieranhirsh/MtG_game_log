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

function sortTableBins(n) {
  var table, bodies, switching, noswitch, i, x, y, header, shouldSwitch, dir, switchcount = 0;
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
  // If the row is "Popularity", we need to remove the leading # to be able to convert to a int
  if (header === "Popularity") {
    for (i = 1; i < (table[0].rows.length); i++) {
      x = table[0].rows[i].getElementsByTagName("td")[n];
      x.innerHTML = x.innerHTML.slice(1);
    }
  }
  // Set the sorting direction:
  if (
    header === "# Decks" ||
    header === "Last Played" ||
    header === "Games Played" ||
    header === "Games Won" ||
    header === "Win Rate" ||
    header === "Date" ||
    header === "Start Time" ||
    header === "Game Length (Time)" ||
    header === "Game Length (Turns)" ||
    header === "First KO" ||
    header === "Ave Game Time" ||
    header === "Ave Game Length" ||
    header === "Ave First KO" ||
    header === "# EDHrec Decks" ||
    header === "Ave # EDHrec Decks"
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
    bodies = table[0].tBodies;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (bodies.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = bodies[i].rows[0].getElementsByTagName("td")[n];
      y = bodies[i + 1].rows[0].getElementsByTagName("td")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (y.innerHTML.toLowerCase() == 0) {
          // If the second element is zero, we don't want to switch, but we also want to keep the loop going:
          if (i == (bodies.length - 2)) {
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
          header === "Last Played" ||
          header === "Games Played" ||
          header === "Games Won" ||
          header === "Win Rate" ||
          header === "Ave Game Length" ||
          header === "First KO" ||
          header === "Game Length (Turns)" ||
          header === "Ave First KO" ||
          header === "# EDHrec Decks" ||
          header === "Popularity" ||
          header === "Ave # EDHrec Decks"
        ) {
          if (header === "Last Played") {
            if (y.innerHTML == "never") {
              continue
            }
            if (x.innerHTML == "never") {
              // If we want to switch, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML) || parseFloat(x.innerHTML) == 0 || isNaN(parseFloat(x.innerHTML))) {
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
          header === "Last Played" ||
          header === "Games Played" ||
          header === "Games Won" ||
          header === "Win Rate" ||
          header === "Game Length (Turns)" ||
          header === "First KO" ||
          header === "Ave Game Length" ||
          header === "Ave First KO" ||
          header === "# EDHrec Decks" ||
          header === "Popularity" ||
          header === "Ave # EDHrec Decks"
        ) {
          if (isNaN(parseFloat(y.innerHTML))) {
            // skip this case
            continue;
          }
          if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML) || isNaN(parseFloat(x.innerHTML))) {
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
      bodies[i].parentNode.insertBefore(bodies[i + 1], bodies[i]);
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

function sortTableRows(n) {
  var table, bodies, rows, switching, noswitch, i, x, y, header, shouldSwitch, globalDir, dirSet, dir, switchcount = 0;
  table = document.getElementsByClassName("data_table");
  header = table[0].rows[0].getElementsByTagName("th")[n].innerHTML;
  dirSet = false;
  // Set the global sorting direction:
  if (
    header === "# Decks" ||
    header === "Last Played" ||
    header === "Games Played" ||
    header === "Games Won" ||
    header === "Win Rate" ||
    header === "Date" ||
    header === "Start Time" ||
    header === "Game Length (Time)" ||
    header === "Game Length (Turns)" ||
    header === "First KO" ||
    header === "Ave Game Time" ||
    header === "Ave Game Length" ||
    header === "Ave First KO" ||
    header === "# EDHrec Decks" ||
    header === "Ave # EDHrec Decks"
  ) {
    globalDir = "desc";
  } else {
    globalDir = "asc";
  }
  bodies = table[0].tBodies;
  for (i = 1; i < bodies.length; i++) {
    /* Make a loop that will continue until
    no switching has been done: */
    rows = bodies[i].rows;
    if (rows.length === 2) {
      continue;
    }
    // Set the global sorting direction:
    dir = globalDir;
    // initialise some loop variables
    switching = true;
    noswitch = true;
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (j = 1; j < (rows.length - 1); j++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[j].getElementsByTagName("td")[n];
        innerX = x.innerHTML;
        if (innerX.includes("minute games") || innerX.includes("turn games") || innerX.includes("player games")) {
          innerX = innerX.trim().split(" ")[0];
        } else if (innerX.includes("%")) {
          innerX = innerX.slice(0, -1);
        } else if (innerX.includes("#")) {
          innerX = innerX.slice(1);
        } else if (innerX.includes("untimed games")) {
          innerX = String(Number.MAX_SAFE_INTEGER);
        } else if (innerX.includes("KO'd on turn")) {
          innerX = innerX.trim().split(" ")[3];
        } else if (innerX.includes("turn ") && innerX.includes(" KO")) {
          innerX = innerX.trim().split(" ")[1];
        } else if (innerX.includes("Won the game")) {
          innerX = String(Number.MIN_SAFE_INTEGER);
        } else if (innerX.includes("Sunday")) {
          innerX = 1;
        } else if (innerX.includes("Monday")) {
          innerX = 2;
        } else if (innerX.includes("Tuesday")) {
          innerX = 3;
        } else if (innerX.includes("Wednesday")) {
          innerX = 4;
        } else if (innerX.includes("Thursday")) {
          innerX = 5;
        } else if (innerX.includes("Friday")) {
          innerX = 6;
        } else if (innerX.includes("Saturday")) {
          innerX = 7;
        } else if (innerX.includes("January")) {
          innerX = 1;
        } else if (innerX.includes("February")) {
          innerX = 2;
        } else if (innerX.includes("March")) {
          innerX = 3;
        } else if (innerX.includes("April")) {
          innerX = 4;
        } else if (innerX.includes("May")) {
          innerX = 5;
        } else if (innerX.includes("June")) {
          innerX = 6;
        } else if (innerX.includes("July")) {
          innerX = 7;
        } else if (innerX.includes("August")) {
          innerX = 8;
        } else if (innerX.includes("September")) {
          innerX = 9;
        } else if (innerX.includes("October")) {
          innerX = 10;
        } else if (innerX.includes("November")) {
          innerX = 11;
        } else if (innerX.includes("December")) {
          innerX = 12;
        }
        y = rows[j + 1].getElementsByTagName("td")[n];
        innerY = y.innerHTML;
        if (innerY.includes("minute games") || innerY.includes("turn games") || innerY.includes("player games")) {
          innerY = innerY.trim().split(" ")[0];
        } else if (innerY.includes("%")) {
          innerY = innerY.slice(0, -1);
        } else if (innerY.includes("#")) {
          innerY = innerY.slice(1);
        } else if (innerY.includes("untimed games")) {
          innerY = String(Number.MAX_SAFE_INTEGER);
        } else if (innerY.includes("KO'd on turn")) {
          innerY = innerY.trim().split(" ")[3];
        } else if (innerY.includes("turn ") && innerY.includes(" KO")) {
          innerY = innerY.trim().split(" ")[1];
        } else if (innerY.includes("Won the game")) {
          innerY = String(Number.MIN_SAFE_INTEGER);
        } else if (innerY.includes("Sunday")) {
          innerY = 1;
        } else if (innerY.includes("Monday")) {
          innerY = 2;
        } else if (innerY.includes("Tuesday")) {
          innerY = 3;
        } else if (innerY.includes("Wednesday")) {
          innerY = 4;
        } else if (innerY.includes("Thursday")) {
          innerY = 5;
        } else if (innerY.includes("Friday")) {
          innerY = 6;
        } else if (innerY.includes("Saturday")) {
          innerY = 7;
        } else if (innerY.includes("January")) {
          innerY = 1;
        } else if (innerY.includes("February")) {
          innerY = 2;
        } else if (innerY.includes("March")) {
          innerY = 3;
        } else if (innerY.includes("April")) {
          innerY = 4;
        } else if (innerY.includes("May")) {
          innerY = 5;
        } else if (innerY.includes("June")) {
          innerY = 6;
        } else if (innerY.includes("July")) {
          innerY = 7;
        } else if (innerY.includes("August")) {
          innerY = 8;
        } else if (innerY.includes("September")) {
          innerY = 9;
        } else if (innerY.includes("October")) {
          innerY = 10;
        } else if (innerY.includes("November")) {
          innerY = 11;
        } else if (innerY.includes("December")) {
          innerY = 12;
        }
        // Make sure the values are of the correct type
        if (typeof (innerX) === "string") {
          if (!isNaN(parseFloat(innerX)) && !innerX.includes(":")) {
            innerX = parseFloat(innerX);
          } else {
            innerX = innerX.toLowerCase();
          }
        }
        if (typeof (innerY) === "string") {
          if (!isNaN(parseFloat(innerY)) && !innerY.includes(":")) {
            innerY = parseFloat(innerY);
          } else {
            innerY = innerY.toLowerCase();
          }
        }
        /* Check if the two rows should switch place,
        based on the direction, asc or desc: */
        if (dir == "asc") {
          if (header === "Last Played") {
            if (y.innerHTML == "never") {
              continue
            }
            if (x.innerHTML == "never") {
              // If we want to switch, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
          if (innerX > innerY) {
            // If we want to switch, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (innerX < innerY) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[j].parentNode.insertBefore(rows[j + 1], rows[j]);
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
    if (dirSet === false) {
      dirSet = true;
      globalDir = dir;
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
      header === "Ave Game Time" ||
      header === "Ave Game Length" ||
      header === "Ave First KO" ||
      header === "Ave # EDHrec Decks"
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
            header === "Win Rate" ||
            header === "Ave Game Length" ||
            header === "Ave First KO" ||
            header === "Ave # EDHrec Decks"
          ) {
            if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML) || parseFloat(x.innerHTML) == 0) {
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
            header === "Ave Game Length" ||
            header === "Ave First KO" ||
            header === "Ave # EDHrec Decks"
          ) {
            if (isNaN(parseFloat(y.innerHTML))) {
              // skip this case
              continue;
            }
            if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML) || isNaN(parseFloat(x.innerHTML))) {
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
