$(document).ready(function () {
    var $container = $('#main-container');
    var jsonData;
    var gameArray = [];

    $(document).ready(loadNewGame());

    function loadNewGame(){
        $.ajax({
            type: 'GET',
            url: '/new_game',
            success: function(data) {
                console.log('new data', data)
                storeData(data);
                createGameGrid();
            },
            error: function() {
                alert('error loading data');
            }
        });
    }

    function storeData(data) {
        console.log('store data', data)
        jsonData = data;
        gameArray = data.board;
        console.log("gameArray", gameArray)
    }

    function showMessage(message) {
        if (message == 'won') {
            alert('Congratulations, you Won!');
            revealMines()
        } else if (message == 'lost') {
            alert('Sorry, you lost :(');
            revealMines()
        }
    }

    function revealMines(){
        for (var i = 0; i < jsonData.size; i++) {
            for (var j = 0; j < jsonData.size; j++) {
                var $field = $container.find('#'+i+'x'+j);
                if (($field.hasClass('unclicked')) && (gameArray[i][j].value == -1)) {
                    $field.attr('src', ('/static/minesweeper_img/mine.png'));
                }
                $field.removeClass('unclicked');
            }
        }  
    }

    function createGameGrid() {
        $container.css('grid-template-columns', 'repeat(' + jsonData.size + ', auto)');
        gameArray.forEach(function(row, i) {
            row.forEach(function(field, j) {
                $container.append('<img id="'+i+'x'+j+'" class="unclicked" src="/static/minesweeper_img/unclicked.png" alt="field" width="40" height="40">');
            });
        });
        $container.css('visibility','visible');
        $('#count-of-mines').text(jsonData.num_mines);
    }

    function updateGameGrid() {
        console.log("UPDATE GAME GRID")
        for (var i = 0; i < jsonData.size; i++) {
            for (var j = 0; j < jsonData.size; j++) {
                var $field = $container.find('#'+i+'x'+j);
                if ($field.hasClass('unclicked')) {
                    if(gameArray[i][j].is_clicked){
                        if(gameArray[i][j].value == -1) {
                            $field.attr('src', ('/static/minesweeper_img/mine.png'));
                        }
                        else{
                            $field.attr('src', ('/static/minesweeper_img/' + gameArray[i][j].value +'.png'));
                        }
                        $field.removeClass('unclicked');
                    }
                }
            }
        }
    }

    $('#new-game-button').on('click', function() {
        $container.css('visibility','hidden');
        $container.html('');
        loadNewGame();
    });

    $container.on('click', '.unclicked', function() {
        var str = $(this).attr('id');
        var clickedXY = str.split('x');
        if (gameArray[clickedXY[0]][clickedXY[1]].marked) {
            return;
        }
        console.log(clickedXY[0] + ' - ' + clickedXY[1] + ' was clicked');

        jsonData.y_guess = parseInt(clickedXY[0]);
        jsonData.x_guess = parseInt(clickedXY[1]);
        jsonData.board = gameArray;

        $.ajax({
            type: 'POST',
            url: '/update_game',
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: function(data) {
                storeData(data);
                updateGameGrid();
                showMessage(data.message);
            },
            error: function() {
                alert('error sending data');
            }
        });
    });
});