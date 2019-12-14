let isPause;
let coef_x, coef_y;

window.onload = function() {
    let container = document.getElementById('container');
    for (let i = 0; i < 10; i++) {
        let elem = document.createElement("div");
        if (i < 5)
            elem.className = "player player1";
        else
            elem.className = "player player2";
        container.appendChild(elem);
    }
    coef_x = parseInt(getComputedStyle(container).width) / 2000.0
    coef_y = parseInt(getComputedStyle(container).height) / 2000.0

    isPause = true;
    myMove();
};

function toggle() {
    if (isPause) {
        document.getElementById("overlay").style.display = "none";
        isPause = false;
    }
    else {
        document.getElementById("overlay").style.display = "block";
        isPause = true;
    }
}

function myMove() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", '/get-response', true);
    xhr.send(null);
    let response;
    xhr.onload = function () {
        response = JSON.parse(xhr.responseText);

        let elem = document.getElementsByClassName("player");
        let iter = 0;
        let max_iter = 0;
        let id = setInterval(frame, 20);

        for (let i = 0; i < 10; i++) {
            max_iter = Math.max(max_iter, response['player_' + i]['X'].length);
        }

        function frame() {
            if (iter == max_iter) {
                clearInterval(id);
            } else {
                if (!isPause)
                    iter++;
                for (let i = 0; i < 10; i++) {
                    let x = response['player_' + i]['X'][iter];
                    let y = response['player_' + i]['Y'][iter];
                    x = 1500 + (x - 670) / 2.56;
                    y = 1500 + (y - 851) / 2.56;
                    x = Math.trunc(x * coef_x);
                    y = Math.trunc(y * coef_y);

                    if (response['player_' + i]['X'].length >= iter) {
                        elem[i].style.bottom = y + "px";
                        elem[i].style.left = x + "px";
                    }
                    else {
                        elem[i].style.display = 'none';
                    }
                }
            }
        }
    }
}