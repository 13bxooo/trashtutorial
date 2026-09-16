import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="쓰레기통 골인 게임",
    page_icon="🗑️",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: #f4f8f5;
    }

    .title {
        text-align: center;
        color: #245c45;
        font-size: 38px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #718078;
        margin-bottom: 20px;
    }

    iframe {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🗑️ 쓰레기통 골인!</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">화살표 키로 움직이고 쓰레기를 던져보세요!</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 게임
# --------------------------------------------------

game_html = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game {
    width: 100%;
    max-width: 850px;
    margin: auto;
}

canvas {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 20px;
    background: #dff3e6;
    border: 2px solid #c9e4d3;
}

.info {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    gap: 10px;
}

.box {
    flex: 1;
    background: white;
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    color: #245c45;
    font-weight: bold;
}

.help {
    margin-top: 12px;
    padding: 12px;
    background: white;
    border-radius: 12px;
    text-align: center;
    color: #66756d;
    font-size: 14px;
}

#message {
    position: fixed;
    left: 50%;
    top: 45%;
    transform: translate(-50%, -50%);
    font-size: 40px;
    font-weight: bold;
    color: #245c45;
    pointer-events: none;
    display: none;
}

</style>

</head>

<body>

<div id="game">

    <canvas id="canvas" width="850" height="500"></canvas>

    <div class="info">

        <div class="box">
            점수<br>
            <span id="score">0</span>
        </div>

        <div class="box">
            남은 시간<br>
            <span id="time">30</span>초
        </div>

        <div class="box">
            각도<br>
            <span id="angle">45</span>°
        </div>

    </div>

    <div class="help">
        ← → 이동　│　↑ ↓ 조준　│　SPACE 던지기　│　R 다시 시작
    </div>

</div>

<div id="message"></div>


<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const timeText = document.getElementById("time");
const angleText = document.getElementById("angle");
const message = document.getElementById("message");


// --------------------------------------------------
// 게임 변수
// --------------------------------------------------

let score = 0;
let timeLeft = 30;
let gameOver = false;

let keys = {};

let angle = 45;

let player = {
    x: 100,
    y: 410,
    width: 45,
    height: 65,
    speed: 6
};

let trash = {
    x: 115,
    y: 380,
    radius: 13
};

let bin = {
    x: 680,
    y: 360,
    width: 75,
    height: 90
};

let projectile = null;

let particles = [];


// --------------------------------------------------
// 키보드
// --------------------------------------------------

document.addEventListener("keydown", function(e) {

    if (
        e.key === "ArrowLeft" ||
        e.key === "ArrowRight" ||
        e.key === "ArrowUp" ||
        e.key === "ArrowDown" ||
        e.code === "Space"
    ) {
        e.preventDefault();
    }

    keys[e.key] = true;

    if (e.code === "Space") {

        if (!gameOver && projectile === null) {
            throwTrash();
        }

    }

    if (
        (e.key === "r" || e.key === "R") &&
        gameOver
    ) {
        restart();
    }

});


document.addEventListener("keyup", function(e) {
    keys[e.key] = false;
});


// --------------------------------------------------
// 쓰레기 던지기
// --------------------------------------------------

function throwTrash() {

    const radians = angle * Math.PI / 180;

    const speed = 13;

    projectile = {

        x: player.x + 35,
        y: player.y - 35,

        vx: Math.cos(radians) * speed,

        vy: -Math.sin(radians) * speed,

        radius: 13,

        rotation: 0

    };

}


// --------------------------------------------------
// 쓰레기통 위치 변경
// --------------------------------------------------

function moveBin() {

    bin.x = 560 + Math.random() * 220;

    bin.y = 350 + Math.random() * 30;

}


// --------------------------------------------------
// 플레이어
// --------------------------------------------------

function updatePlayer() {

    if (keys["ArrowLeft"]) {

        player.x -= player.speed;

    }

    if (keys["ArrowRight"]) {

        player.x += player.speed;

    }

    if (keys["ArrowUp"]) {

        angle += 1;

    }

    if (keys["ArrowDown"]) {

        angle -= 1;

    }

    angle = Math.max(15, Math.min(75, angle));

    player.x = Math.max(
        20,
        Math.min(430, player.x)
    );

    angleText.textContent = Math.round(angle);

}


// --------------------------------------------------
// 투사체
// --------------------------------------------------

function updateProjectile() {

    if (projectile === null) {
        return;
    }

    projectile.x += projectile.vx;

    projectile.y += projectile.vy;

    projectile.vy += 0.35;

    projectile.rotation += 0.2;


    // 쓰레기통 충돌
    const insideX =
        projectile.x >
        bin.x - 5 &&
        projectile.x <
        bin.x + bin.width + 5;

    const insideY =
        projectile.y >
        bin.y - 5 &&
        projectile.y <
        bin.y + bin.height;


    if (insideX && insideY) {

        success();

        projectile = null;

        return;
    }


    // 바닥에 떨어짐
    if (projectile.y > 460) {

        projectile = null;

        return;
    }


    // 화면 밖
    if (
        projectile.x > canvas.width + 50 ||
        projectile.x < -50 ||
        projectile.y < -100
    ) {

        projectile = null;

    }

}


// --------------------------------------------------
// 성공
// --------------------------------------------------

function success() {

    score += 100;

    scoreText.textContent = score;

    showMessage("🎯 GOAL! +100");

    createParticles(
        bin.x + bin.width / 2,
        bin.y
    );

    moveBin();

}


// --------------------------------------------------
// 메시지
// --------------------------------------------------

function showMessage(text) {

    message.textContent = text;

    message.style.display = "block";

    setTimeout(function() {

        message.style.display = "none";

    }, 700);

}


// --------------------------------------------------
// 파티클
// --------------------------------------------------

function createParticles(x, y) {

    for (let i = 0; i < 20; i++) {

        particles.push({

            x: x,
            y: y,

            vx: (Math.random() - 0.5) * 7,

            vy: (Math.random() - 0.8) * 7,

            life: 40

        });

    }

}


function updateParticles() {

    particles.forEach(p => {

        p.x += p.vx;

        p.y += p.vy;

        p.vy += 0.2;

        p.life--;

    });

    particles =
        particles.filter(p => p.life > 0);

}


// --------------------------------------------------
// 그리기
// --------------------------------------------------

function drawBackground() {

    // 하늘
    ctx.fillStyle = "#dff3e6";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // 구름
    ctx.fillStyle = "rgba(255,255,255,0.7)";

    ctx.beginPath();

    ctx.arc(120, 90, 25, 0, Math.PI * 2);

    ctx.arc(150, 80, 35, 0, Math.PI * 2);

    ctx.arc(185, 95, 25, 0, Math.PI * 2);

    ctx.fill();


    ctx.beginPath();

    ctx.arc(500, 100, 22, 0, Math.PI * 2);

    ctx.arc(530, 90, 32, 0, Math.PI * 2);

    ctx.arc(565, 105, 22, 0, Math.PI * 2);

    ctx.fill();


    // 바닥
    ctx.fillStyle = "#cbded1";

    ctx.fillRect(
        0,
        430,
        canvas.width,
        70
    );


    // 바닥선
    ctx.strokeStyle = "#aac5b4";

    ctx.lineWidth = 3;

    ctx.beginPath();

    ctx.moveTo(0, 430);

    ctx.lineTo(canvas.width, 430);

    ctx.stroke();

}


// --------------------------------------------------
// 플레이어 그리기
// --------------------------------------------------

function drawPlayer() {

    // 몸
    ctx.fillStyle = "#4d8064";

    ctx.fillRect(
        player.x,
        player.y - 55,
        player.width,
        55
    );


    // 머리
    ctx.fillStyle = "#f2c6a0";

    ctx.beginPath();

    ctx.arc(
        player.x + 22,
        player.y - 72,
        18,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // 모자
    ctx.fillStyle = "#245c45";

    ctx.fillRect(
        player.x + 3,
        player.y - 91,
        38,
        8
    );


    // 팔
    ctx.strokeStyle = "#f2c6a0";

    ctx.lineWidth = 9;

    ctx.beginPath();

    ctx.moveTo(
        player.x + 38,
        player.y - 42
    );

    ctx.lineTo(
        player.x + 57,
        player.y - 58
    );

    ctx.stroke();


    // 조준선
    const radians =
        angle * Math.PI / 180;

    ctx.strokeStyle =
        "rgba(36,92,69,0.35)";

    ctx.lineWidth = 3;

    ctx.setLineDash([7, 7]);

    ctx.beginPath();

    ctx.moveTo(
        player.x + 40,
        player.y - 50
    );

    ctx.lineTo(
        player.x + 40 + Math.cos(radians) * 100,
        player.y - 50 - Math.sin(radians) * 100
    );

    ctx.stroke();

    ctx.setLineDash([]);

}


// --------------------------------------------------
// 쓰레기통 그리기
// --------------------------------------------------

function drawBin() {

    // 본체
    ctx.fillStyle = "#5c6870";

    ctx.fillRect(
        bin.x,
        bin.y,
        bin.width,
        bin.height
    );


    // 윗부분
    ctx.fillStyle = "#424b51";

    ctx.fillRect(
        bin.x - 5,
        bin.y - 10,
        bin.width + 10,
        13
    );


    // 손잡이
    ctx.strokeStyle = "#424b51";

    ctx.lineWidth = 7;

    ctx.beginPath();

    ctx.arc(
        bin.x + bin.width / 2,
        bin.y - 7,
        18,
        Math.PI,
        0
    );

    ctx.stroke();


    // 쓰레기통 표시
    ctx.fillStyle = "white";

    ctx.font = "30px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "♻",
        bin.x + bin.width / 2,
        bin.y + 58
    );

}


// --------------------------------------------------
// 현재 쓰레기 그리기
// --------------------------------------------------

function drawTrash() {

    if (projectile !== null) {
        return;
    }

    ctx.font = "28px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "🥤",
        player.x + 58,
        player.y - 40
    );

}


// --------------------------------------------------
// 날아가는 쓰레기
// --------------------------------------------------

function drawProjectile() {

    if (projectile === null) {
        return;
    }

    ctx.save();

    ctx.translate(
        projectile.x,
        projectile.y
    );

    ctx.rotate(projectile.rotation);

    ctx.font = "30px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "🥤",
        0,
        0
    );

    ctx.restore();

}


// --------------------------------------------------
// 파티클 그리기
// --------------------------------------------------

function drawParticles() {

    particles.forEach(p => {

        ctx.fillStyle =
            "rgba(46, 125, 80, " +
            (p.life / 40) +
            ")";

        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            4,
            0,
            Math.PI * 2
        );

        ctx.fill();

    });

}


// --------------------------------------------------
// 게임 종료
// --------------------------------------------------

function endGame() {

    gameOver = true;

    showMessage(
        "🏆 GAME OVER!  R을 눌러 다시 시작"
    );

}


// --------------------------------------------------
// 재시작
// --------------------------------------------------

function restart() {

    score = 0;

    timeLeft = 30;

    gameOver = false;

    angle = 45;

    player.x = 100;

    projectile = null;

    particles = [];

    moveBin();

    scoreText.textContent = score;

    timeText.textContent = timeLeft;

}


// --------------------------------------------------
// 게임 업데이트
// --------------------------------------------------

function update() {

    if (!gameOver) {

        updatePlayer();

        updateProjectile();

    }

    updateParticles();

}


// --------------------------------------------------
// 게임 그리기
// --------------------------------------------------

function draw() {

    drawBackground();

    drawBin();

    drawPlayer();

    drawTrash();

    drawProjectile();

    drawParticles();

}


// --------------------------------------------------
// 게임 루프
// --------------------------------------------------

function gameLoop() {

    update();

    draw();

    requestAnimationFrame(gameLoop);

}


// --------------------------------------------------
// 타이머
// --------------------------------------------------

setInterval(function() {

    if (gameOver) {
        return;
    }

    timeLeft--;

    timeText.textContent = timeLeft;

    if (timeLeft <= 0) {

        endGame();

    }

}, 1000);


// 시작
moveBin();

gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)
