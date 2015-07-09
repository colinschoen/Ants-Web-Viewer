
$("#playBtn").on('click', function() {
    $(this).addClass('animated fadeOutLeft');
    $('#header-title').addClass('animated fadeOutUp');
    $('#hero-head').addClass('animated bounceOutDown').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
        //Load the game wrapper and bg
        $('#gameWrapper').show().addClass('animated bounceInDown');
        startGame();
    });
});

function GUI() {
    this.jsonLocation = "../gameState.json";
    this.oldState;
    this.newState;
}

function startGame() {
    var gui = new GUI();
}

function get_gameState() {
    //Read our JSON state file
    newState = $.getJSON(jsonLocation)
        .fail(function() {
            dispatchAlert("Error reading game state.");
        });
}

function drawCanvas() {

}
