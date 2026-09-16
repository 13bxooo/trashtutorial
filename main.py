import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Trash Shot",
    page_icon="🗑️",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: #eef5f0;
}

.title {
    text-align: center;
    color: #245c45;
    font-size: 40px;
    font-weight: 800;
    margin-top: 15px;
}

.subtitle {
    text-align: center;
    color: #718078;
    margin-bottom: 15px;
}

iframe {
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🗑️ TRASH SHOT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">화살표 키로 움직이고, 정확하게 쓰레기를 던져보세요.</div>',
    unsafe_allow_html=True
)


game_html = r"""
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
    max-width: 900px;
    margin: auto;
}

canvas {
    width: 100%;
    display: block;
    border-radius: 20px;
    background: #dcefe3;
    border: 2px solid #c5dfcf;
    outline: none;
}

.stats {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.stat {
    flex: 1;
    background: white;
    border-radius: 12px;
    text-align: center;
    padding: 9px 4px;
    color: #245c45;
    font-weight: bold;
    font-size: 14px;
}

.stat span {
    font-size: 20px;
}

.help {
    margin-top: 10px;
    background: white;
    border-radius: 12px;
    padding: 11px;
    text-align: center;
    color: #65746c;
    font-size: 13px;
}

#message {
    position: fixed;
    left: 50%;
    top: 42%;
    transform: translate(-50%, -50%);
    font-size: 38px;
    font-weight: 900;
    color: #245c45;
    pointer-events: none;
    display: none;
    text-align: center;
    white-space: nowrap;
}

</style>
</head>

<body>

<div id="game">

    <canvas
        id="canvas"
        width="900"
        height="520"
        tabindex="0">
    </canvas>

    <div class="stats">

        <div class="stat">
            LEVEL<br>
            <span id="level">1</span>
        </div>

        <div class="stat">
            SCORE<br>
            <span id="score">0</span>
        </div>

        <div class="stat">
            LIFE<br>
            <span id="life">❤️❤️❤️</span>
        </div>

        <div class="stat">
            COMBO<br>
            <span id="combo">0</span>
        </div>

    </div>

    <div class="help">
        ← → 이동　│　↑ ↓ 각도　│　SPACE 던지기　│　R 재시작
    </div>

</div>

<div id="message"></div>


<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.focus();


// ==================================================
// 기본 게임 상태
// ==================================================

let level = 1;
let score = 0;
let life = 3;
let combo = 0;

let gameOver = false;

let keys = {};

let angle = 45;


// ==================================================
// 플레이어
// ==================================================

let player = {
    x: 100,
    y: 425,
    width: 45,
    height: 65,
    speed: 6
};


// ==================================================
// 쓰레기
// ==================================================

let projectile = null;


// ==================================================
// 쓰레기통
// ==================================================

let bin = {
    x: 700,
    y: 365,
    width: 80,
    height: 100
};


// 접근 금지 거리
let forbiddenDistance = 220;


// ==================================================
// 레벨별 설정
// ==================================================

function getLevelSettings() {

    return {

        // 레벨이 올라갈수록 중력 증가
        gravity:
            0.28 + (level - 1) * 0.045,

        // 레벨이 올라갈수록 바람 증가
        wind:
            (Math.random() - 0.5)
            * (0.10 + level * 0.045),

        // 쓰레기통 크기 감소
        binSize:
            Math.max(
                48,
                80 - (level - 1) * 4
            ),

        // 접근 금지 거리 증가
        forbidden:
            Math.min(
                300,
                220 + (level - 1) * 8
            ),

        // 목표 정확도
        tolerance:
            Math.max(
                8,
                22 - (level - 1) * 1.2
            )
    };
}


// ==================================================
// 키 입력
// ==================================================

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

        if (
            !gameOver &&
            projectile === null
        ) {
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


// ==================================================
// 플레이어 이동
// ==================================================

function updatePlayer() {

    if (keys["ArrowLeft"]) {
        player.x -= player.speed;
    }

    if (keys["ArrowRight"]) {
        player.x += player.speed;
    }

    if (keys["ArrowUp"]) {
        angle += 0.8;
    }

    if (keys["ArrowDown"]) {
        angle -= 0.8;
    }


    // 각도 제한
    angle = Math.max(
        15,
        Math.min(80, angle)
    );


    // 화면 경계
    player.x = Math.max(
        25,
        Math.min(
            canvas.width - 450,
            player.x
        )
    );


    // ==============================================
    // 쓰레기통과의 접근 금지 거리
    // ==============================================

    const playerCenter =
        player.x + player.width / 2;

    const binCenter =
        bin.x + bin.width / 2;

    const distance =
        Math.abs(binCenter - playerCenter);

    const minimumDistance =
        getLevelSettings().forbidden;


    if (distance < minimumDistance) {

        if (playerCenter < binCenter) {

            player.x =
                binCenter
                - minimumDistance
                - player.width / 2;

        } else {

            player.x =
                binCenter
                + minimumDistance
                - player.width / 2;

        }

    }

    document.getElementById("angle").textContent =
        Math.round(angle);

}


// ==================================================
// 쓰레기 던지기
// ==================================================

function throwTrash() {

    const radians =
        angle * Math.PI / 180;

    const speed =
        11 + Math.min(level * 0.3, 5);


    projectile = {

        x:
            player.x + 55,

        y:
            player.y - 45,

        vx:
            Math.cos(radians) * speed,

        vy:
            -Math.sin(radians) * speed,

        radius: 14,

        rotation: 0

    };

}


// ==================================================
// 투사체 업데이트
// ==================================================

function updateProjectile() {

    if (projectile === null) {
        return;
    }

    const settings =
        getLevelSettings();


    // 바람
    projectile.vx += settings.wind;


    // 위치
    projectile.x += projectile.vx;

    projectile.y += projectile.vy;


    // 중력
    projectile.vy += settings.gravity;


    // 회전
    projectile.rotation += 0.25;


    // ==============================================
    // 쓰레기통 충돌
    // ==============================================

    const insideX =
        projectile.x >
        bin.x + 5 &&
        projectile.x <
        bin.x + bin.width - 5;

    const insideY =
        projectile.y >
        bin.y - 5 &&
        projectile.y <
        bin.y + 35;


    if (insideX && insideY) {

        success();

        projectile = null;

        return;
    }


    // ==============================================
    // 바닥
    // ==============================================

    if (projectile.y > 455) {

        fail();

        projectile = null;

        return;
    }


    // 화면 밖
    if (
        projectile.x < -100 ||
        projectile.x > canvas.width + 100 ||
        projectile.y < -100
    ) {

        fail();

        projectile = null;

    }

}


// ==================================================
// 성공
// ==================================================

function success() {

    combo++;


    let earned =
        100 * level;


    // 콤보 보너스
    if (combo >= 2) {
        earned += combo * 30;
    }


    score += earned;


    document.getElementById("score")
        .textContent = score;

    document.getElementById("combo")
        .textContent = combo;


    showMessage(
        "🎯 PERFECT! +" + earned
    );


    createParticles(
        bin.x + bin.width / 2,
        bin.y
    );


    // 다음 레벨
    level++;


    document.getElementById("level")
        .textContent = level;


    // 새로운 쓰레기통
    newBin();

}


// ==================================================
// 실패
// ==================================================

function fail() {

    combo = 0;

    life--;


    document.getElementById("combo")
        .textContent = combo;


    updateLife();


    if (life <= 0) {

        gameOver = true;

        showMessage(
            "💀 GAME OVER<br>R을 눌러 다시 시작"
        );

    } else {

        showMessage(
            "💨 MISS!"
        );

    }

}


// ==================================================
// 목숨 표시
// ==================================================

function updateLife() {

    let text = "";

    for (let i = 0; i < 3; i++) {

        if (i < life) {
            text += "❤️";
        } else {
            text += "🖤";
        }

    }

    document.getElementById("life")
        .textContent = text;

}


// ==================================================
// 새로운 쓰레기통
// ==================================================

function newBin() {

    const settings =
        getLevelSettings();


    bin.width =
        settings.binSize;

    bin.height =
        settings.binSize * 1.25;


    // 플레이어가 접근할 수 없는 거리 유지
    const minimumX =
        player.x
        + settings.forbidden;


    bin.x =
        Math.max(
            minimumX,
            570 + Math.random() * 250
        );


    // 화면 밖 방지
    bin.x =
        Math.min(
            canvas.width - bin.width - 20,
            bin.x
        );


    bin.y =
        350 + Math.random() * 20;

}


// ==================================================
// 메시지
// ==================================================

function showMessage(text) {

    message.innerHTML = text;

    message.style.display = "block";


    setTimeout(function() {

        message.style.display = "none";

    }, 700);

}


// ==================================================
// 파티클
// ==================================================

let particles = [];


function createParticles(x, y) {

    for (let i = 0; i < 25; i++) {

        particles.push({

            x: x,

            y: y,

            vx:
                (Math.random() - 0.5) * 8,

            vy:
                (Math.random() - 0.8) * 8,

            life: 45

        });

    }

}


function updateParticles() {

    particles.forEach(function(p) {

        p.x += p.vx;

        p.y += p.vy;

        p.vy += 0.2;

        p.life--;

    });


    particles =
        particles.filter(
            p => p.life > 0
        );

}


// ==================================================
// 배경
// ==================================================

function drawBackground() {

    // 하늘
    ctx.fillStyle = "#dcefe3";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // 구름
    ctx.fillStyle =
        "rgba(255,255,255,0.7)";


    ctx.beginPath();

    ctx.arc(
        130,
        90,
        25,
        0,
        Math.PI * 2
    );

    ctx.arc(
        165,
        80,
        35,
        0,
        Math.PI * 2
    );

    ctx.arc(
        205,
        95,
        25,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // 바닥
    ctx.fillStyle = "#c7dbce";

    ctx.fillRect(
        0,
        435,
        canvas.width,
        85
    );


    // 바닥선
    ctx.strokeStyle = "#9fbaa9";

    ctx.lineWidth = 3;

    ctx.beginPath();

    ctx.moveTo(0, 435);

    ctx.lineTo(
        canvas.width,
        435
    );

    ctx.stroke();

}


// ==================================================
// 접근 금지 구역
// ==================================================

function drawForbiddenZone() {

    const settings =
        getLevelSettings();


    const binCenter =
        bin.x + bin.width / 2;


    const left =
        binCenter -
        settings.forbidden;


    ctx.strokeStyle =
        "rgba(210,70,70,0.65)";

    ctx.lineWidth = 3;

    ctx.setLineDash([8, 8]);


    ctx.beginPath();

    ctx.arc(
        binCenter,
        435,
        settings.forbidden,
        Math.PI,
        Math.PI * 2
    );

    ctx.stroke();


    ctx.setLineDash([]);


    // 영역 설명
    ctx.fillStyle =
        "rgba(170,60,60,0.75)";

    ctx.font = "12px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "APPROACH LIMIT",
        left + settings.forbidden,
        405
    );

}


// ==================================================
// 플레이어
// ==================================================

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
    ctx.fillStyle = "#f1c5a0";

    ctx.beginPath();

    ctx.arc(
        player.x + 22,
        player.y - 73,
        18,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // 모자
    ctx.fillStyle = "#245c45";

    ctx.fillRect(
        player.x + 3,
        player.y - 92,
        38,
        8
    );


    // 팔
    ctx.strokeStyle = "#f1c5a0";

    ctx.lineWidth = 9;

    ctx.beginPath();

    ctx.moveTo(
        player.x + 38,
        player.y - 40
    );

    ctx.lineTo(
        player.x + 57,
        player.y - 55
    );

    ctx.stroke();


    // 조준선
    const radians =
        angle * Math.PI / 180;


    ctx.strokeStyle =
        "rgba(36,92,69,0.4)";

    ctx.lineWidth = 3;

    ctx.setLineDash([7, 7]);


    ctx.beginPath();

    ctx.moveTo(
        player.x + 40,
        player.y - 50
    );


    ctx.lineTo(

        player.x +
        40 +
        Math.cos(radians) * 100,

        player.y -
        50 -
        Math.sin(radians) * 100

    );


    ctx.stroke();

    ctx.setLineDash([]);

}


// ==================================================
// 쓰레기통
// ==================================================

function drawBin() {

    // 몸체
    ctx.fillStyle = "#58656d";

    ctx.fillRect(
        bin.x,
        bin.y,
        bin.width,
        bin.height
    );


    // 뚜껑
    ctx.fillStyle = "#3f494f";

    ctx.fillRect(
        bin.x - 5,
        bin.y - 9,
        bin.width + 10,
        12
    );


    // 손잡이
    ctx.strokeStyle = "#3f494f";

    ctx.lineWidth = 7;

    ctx.beginPath();

    ctx.arc(
        bin.x + bin.width / 2,
        bin.y - 7,
        17,
        Math.PI,
        0
    );

    ctx.stroke();


    // 재활용 표시
    ctx.fillStyle = "white";

    ctx.font =
        Math.max(
            22,
            bin.width * 0.4
        ) + "px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "♻",
        bin.x + bin.width / 2,
        bin.y + bin.height * 0.65
    );

}


// ==================================================
// 대기 중 쓰레기
// ==================================================

function drawTrash() {

    if (projectile !== null) {
        return;
    }


    ctx.font = "30px Arial";

    ctx.textAlign = "center";


    ctx.fillText(
        "🥤",
        player.x + 58,
        player.y - 38
    );

}


// ==================================================
// 날아가는 쓰레기
// ==================================================

function drawProjectile() {

    if (projectile === null) {
        return;
    }


    ctx.save();


    ctx.translate(
        projectile.x,
        projectile.y
    );


    ctx.rotate(
        projectile.rotation
    );


    ctx.font = "30px Arial";

    ctx.textAlign = "center";


    ctx.fillText(
        "🥤",
        0,
        0
    );


    ctx.restore();

}


// ==================================================
// 파티클
// ==================================================

function drawParticles() {

    particles.forEach(function(p) {

        ctx.fillStyle =
            "rgba(46,125,80," +
            (p.life / 45) +
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


// ==================================================
// 게임 루프
// ==================================================

function update() {

    if (!gameOver) {

        updatePlayer();

        updateProjectile();

    }

    updateParticles();

}


function draw() {

    drawBackground();

    drawForbiddenZone();

    drawBin();

    drawPlayer();

    drawTrash();

    drawProjectile();

    drawParticles();

}


function gameLoop() {

    update();

    draw();

    requestAnimationFrame(
        gameLoop
    );

}


// ==================================================
// 재시작
// ==================================================

function restart() {

    level = 1;

    score = 0;

    life = 3;

    combo = 0;

    angle = 45;

    gameOver = false;

    projectile = null;

    particles = [];


    player.x = 100;


    document.getElementById("level")
        .textContent = level;

    document.getElementById("score")
        .textContent = score;

    document.getElementById("combo")
        .textContent = combo;


    updateLife();

    newBin();

}


// ==================================================
// 시작
// ==================================================

newBin();

updateLife();

gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=680,
    scrolling=False
)
