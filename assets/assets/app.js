$.ajaxSetup({
        async: false,
        cache: false,
});

function GUI() {
    this.oldState;
    this.newState;
}

function drawControlPanel(food, ants) {
    tr = $('#antsTableRow');
    for (var id in ants) {
        ant = ants[id];
        if (ant["cost"] > food)
            tr.append('<td class="ant-row ant-inactive"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
        else
            tr.append('<td class="ant-row"><img class="ant-img" src="' + ant["img"] + '"> ' + ant["name"] + '<hr class="ant-row-divider" /><span class="badge ant-cost">' + ant["cost"] + '</span></td>');
    }
}

function startGame() {
    var gui = new GUI();
    gui.get_gameState();
    drawControlPanel(gui.get_food(), gui.get_antTypes());
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
    });
};

GUI.prototype.updateState = function(s) {
    this.oldState = this.newState;
    this.newState = s;
}

GUI.prototype.get_antTypes = function() {
    return this.newState["ant_types"];
}

GUI.prototype.get_food = function() {
    return this.newState["food"];
}

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
    $.post("ajax/exit");
    alert("GUI Exited");
});
