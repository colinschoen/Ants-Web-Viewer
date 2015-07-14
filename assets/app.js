var gui;
$.ajaxSetup({
        async: false,
        cache: false,
});

function GUI() {
    this.oldState;
    this.newState;
}

function drawControlPanel(food, places, ants) {
    tr = $('#antsTableRow');
    for (var id in ants) {
        ant = ants[id];
        if (ant["cost"] > food)
            tr.append('<td data-disabled="1" data-img="' + ant["img"] + '" data-name="' + ant["name"] + '" id="ant_' + ant["name"]  + '" class="ant-row ant-inactive"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
        else
            tr.append('<td data-disabled="0" data-img="' + ant["img"] + '" data-name="' + ant["name"] + '" id="ant_' + ant["name"] + '" class="ant-row"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
    }
    updateFoodCount();
    drawInitialPlaces();
}

function drawInitialPlaces() {
    pTable = $('.places-table');
    rows = gui.get_rows();
    places = gui.get_places();
    i = 0;
    tr = null;
    while (i <= rows) {
        pTable.append('<tr id="pRow' + i + '"></tr>');
        tr = pTable.find('#pRow' + i);
        for (col in places[i]) {
            random_sky = Math.floor(Math.random() * 3) + 1;
            random_ground = Math.floor(Math.random() * 3) + 1;
            if (places[i][col]["water"] == 1)
                random_ground = "water";
            tr.append('<td data-row="' + i  + '" data-col="' + col  + '" data-name="' + places[i][col]["name"]  + '" class="places-td" id="pCol' + col + '"><div class="tunnel-div"><div class="tunnel-img-container"></div><div style="background-image: url(\'assets/tiles/sky/' + random_sky + '.png\')"class="tunnel-goc-div"></div><div style="background-image: url(\'assets/tiles/ground/' + random_ground + '.png\')" class="tunnel-goc-div"></div></div></td>');
        }
        if (i == 0) {
            rowspan = rows + 1
            tr.append('<td id="hive-td" rowspan="' + rowspan + '" class="place-hive-td"></td>')
            td = tr.find('.place-hive-td');
            for (bee in places["Hive"]["insects"]) {
                td.append('<img class="bee-img" src="assets/insects/bee.gif">');
            }
            pTable.find('.place-hive-td').html()
        }
        i += 1;
    }
}


function updateFoodCount() {
    $('#foodCount').html(gui.get_food());
}

function startGame() {
    gui = new GUI();
    gui.get_gameState();
    drawControlPanel(gui.get_food(), gui.get_places(), gui.get_antTypes());
    gui.update();
}


function dump(obj) {
    var out = '';
    for (var i in obj) {
        out += i + ": " + obj[i] + "\n";
    }
    console.log(out);
}

GUI.prototype.get_gameState = function() {
    t = this;
    $.post("ajax/fetch/state", function(state) {
        t.updateState(state);
        return state;
    })
    .fail(function(xhr, tStatus, e) {
        swal({
            title: "Error",
            text: e,
            type: "error",
            showConfirmButton: false,
            });
    });
};

GUI.prototype.get_rows = function() {
    return this.newState["rows"];
}

GUI.prototype.updateState = function(s) {
    this.oldState = this.newState;
    this.newState = s;
}

GUI.prototype.get_antTypes = function() {
    return this.newState["ant_types"];
}

GUI.prototype.get_places = function() {
    return this.newState["places"];
}

GUI.prototype.get_food = function() {
    return this.newState["food"];
}
GUI.prototype.selectAnt = function(name, img) {
    this.selected_ant = { name: name, img: img };
}
GUI.prototype.deselectAnt = function() {
    currentSelected = this.get_selectedAnt();
    this.selected_ant = null;
    if (currentSelected) {
        $('#antsTableRow').find("[data-name = '" + currentSelected["name"] + "']").removeClass("ant-selected");
    }
}
GUI.prototype.get_selectedAnt = function() {
    return this.selected_ant;
}



$('#antsTableRow').on('click', ".ant-row", function() {
    if ($(this).attr('data-disabled') == 1) {
        swal({
            title: "Cannot Select " + $(this).attr('data-name') + " Ant",
            text: "You do not have enough food.",
            type: "error",
        });
        return false;
    }
    currentSelected = gui.get_selectedAnt();
    if (currentSelected) {
        $('#antsTableRow').find("[data-name = '" + currentSelected["name"] + "']").removeClass("ant-selected");
    }
    $(this).addClass('ant-selected');
    gui.selectAnt($(this).attr('data-name'), $(this).attr('data-img'));
});


$("#playBtn").on('click', function() {
    $(this).addClass('animated fadeOutLeft');
    $('#header-title').addClass('animated fadeOutUp');
    $('#hero-head').addClass('animated bounceOutDown').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
        $('#hero-head').hide();
        //Load the game wrapper and bg
        $('#gameWrapper').show().addClass('animated bounceInDown');
    });
    startGame();
});

$('#exitBtn').on('click', function() {
    swal({
        title: "Terminated",
        text: "The Web GUI has been killed.",
        type: "warning",
        showConfirmButton: false,
        });
    $.post("ajax/exit");
    $.post("ajax/exit");
});

$('.places-table').on('click', '.places-td', function() {
    //Check to see if an insect is selected
    t = this
    selectedAnt = gui.get_selectedAnt();
    //Deselect ant
    gui.deselectAnt();
    if (!selectedAnt) {
        swal({
            title: "Error",
            text: "You need to select an insect first.",
            type: "error",
        });
    }
    if (selectedAnt["food"] > gui.get_food()) {
        swal({
            title: "Error",
            text: "Not enough food remains to place " + selectedAnt["name"],
            type: "error",
        });
    }
    $.ajax({
        method: "POST",
        url: "ajax/deploy/ant",
        data: { pname: $(this).attr("data-name"), ant: selectedAnt["name"]},
    })
        .done(function(response) {
            if (response["error"]) {
                swal({
                    title: "Error",
                    text: response["error"],
                    type: "error",
                });
            }        
            else {
                $(t).find('.tunnel-img-container').html('<img class="active-ant" src="' + selectedAnt["img"]  + '">');
                gui.update();
            }
        });
});

GUI.prototype.update = function() {
    $('.active-ant').html("");
    places = this.get_places();
    for (r in places) {
        if (r == "Hive") {
            continue;
        }
        for (c in places[r]) {
            if ("type" in places[r][c]["insects"]) {
                console.log("Adding insect: " + places[r][c]["insects"]["name"]);
                $('.places-table').find('.places-td[data-row="' + r  + '"][data-col="' + c  + '"]').find('.tunnel-img-container').html('<img class="active-ant" src="' + places[r][c]["insects"]["img"]  + '">');
            }
        }
    }
}
