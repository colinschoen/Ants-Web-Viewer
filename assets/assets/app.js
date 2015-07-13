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
            tr.append('<td data-disabled="1" data-name="' + ant["name"] + '" id="ant_' + ant["name"]  + '" class="ant-row ant-inactive"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
        else
            tr.append('<td data-disabled="0" class="ant-row"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
    }
    updateFoodCount();
    drawInitialPlaces();
}

function drawInitialPlaces() {
    pTable = $('.places-table');
    rows = gui.get_rows();
    console.log(rows);
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
            tr.append('<td class="places-td" id="pCol' + col + '"><div class="tunnel-div"><div style="background-image: url(\'assets/tiles/sky/' + random_sky + '.png\')"class="tunnel-goc-div"></div><div style="background-image: url(\'assets/tiles/ground/' + random_ground + '.png\')" class="tunnel-goc-div"></div></div></td>');
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
GUI.prototype.selectAnt = function(name) {
    this.selected_ant = name;
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
        $('#antsTableRow').find("[data-name = '" + currentSelected + "']").removeClass("ant-selected");
    }
    $(this).addClass('ant-selected');
    gui.selectAnt($(this).attr('data-name'));
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
