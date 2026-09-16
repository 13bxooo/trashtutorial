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

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #dcefe5;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#gameWrapper {
    width: 100%;
    height: 560px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

#info {
    width: 95%;
    max-width: 900px;
    height: 65px;
    display: flex;
    gap: 8px;
    margin-top: 8px;
}

.box {
    flex: 1;
    background: white;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.label {
    font-size: 13px;
    font-weight: bold;
    color: #245c45;
}

.value {
    font-size: 20px;
    font-weight: bold;
    color: #164d39;
    margin-top: 3px;
}

#life {
    letter-spacing: 3px;
}

#gameCanvas {
    width: 95%;
    max-width: 900px;
    height: 430px;
    margin-top: 8px;
    border-radius: 18px;
    border: 2px solid #b9dcc8;
    background: #dff1e6;
    outline: none;
    cursor: crosshair;
}

#controls {
    width: 95%;
    max-width: 900px;
    background: white;
    border-radius: 12px;
    margin-top: 8px;
    padding: 10px;
    text-align: center;
    color: #60766a;
    font-size: 13px;
}

#message {
    position: absolute;
    top: 230px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 30px;
    font-weight: bold;
    color: #245c45;
    text-align: center;
    pointer-events: none;
    opacity: 0;
}

</style>

</head>

<body>

<div id="gameWrapper">

    <div id="info">

        <div class="box">
            <div class="label">LEVEL</div>
            <div class="value" id="level">1</div>
        </div>

        <div class="box">
            <div class="label">SCORE</div>
            <div class="value" id="score">0</div>
        </div>

        <div class="box">
            <div class="label">LIFE</div>
            <div class="value" id="life">❤️ ❤️ ❤️</div>
        </div>

        <div class="box">
            <div class="label">COMBO</div>
            <div class="value" id="combo">0</div>
        </div>

    </div>

    <canvas id="gameCanvas" tabindex="0"></canvas>

    <div id="controls">
        ← → 이동　|　↑ ↓ 각도　|　SPACE 던지기　|　R 재시작
    </div>

</div>

<div id="message"></div>


<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 900;
canvas.height = 430;


/* =========================
   SOUND
========================= */

let audioContext = null;

function initAudio() {

    if (!audioContext) {
        audioContext = new (
            window.AudioContext ||
            window.webkitAudioContext
        )();
    }

    if (audioContext.state === "suspended") {
        audioContext.resume();
    }
}


function playTone(
    frequency,
    duration,
    type = "sine",
    volume = 0.08
) {

    initAudio();

    const oscillator =
        audioContext.createOscillator();

    const gain =
        audioContext.createGain();

    oscillator.type = type;
    oscillator.frequency.value = frequency;

    gain.gain.setValueAtTime(
        volume,
        audioContext.currentTime
    );

    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime + duration
    );

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    oscillator.start();

    oscillator.stop(
        audioContext.currentTime + duration
    );
}


/* 성공 */

function successSound() {

    playTone(660, 0.12, "sine", 0.08);

    setTimeout(() => {
        playTone(880, 0.16, "sine", 0.08);
    }, 100);
}


/* 실패 */

function missSound() {

    playTone(180, 0.16, "triangle", 0.09);

    setTimeout(() => {
        playTone(120, 0.20, "triangle", 0.07);
    }, 100);
}


/* 목숨 감소 */

function lifeLostSound() {

    playTone(240, 0.15, "square", 0.07);

    setTimeout(() => {
        playTone(150, 0.28, "square", 0.06);
    }, 120);
}


/* 게임 오버 */

function gameOverSound() {

    playTone(300, 0.20, "sawtooth", 0.06);

    setTimeout(() => {
        playTone(220, 0.20, "sawtooth", 0.06);
    }, 180);

    setTimeout(() => {
        playTone(140, 0.40, "sawtooth", 0.05);
    }, 360);
}


/* =========================
   GAME VARIABLES
========================= */

let level = 1;
let score = 0;
let life = 3;
let combo = 0;

let gameOver = false;

let keys = {};

let angle = 45;

let projectile = null;

let particles = [];

let wind = 0;


/* 플레이어 */

let player = {

    x: 90,

    y: 325,

    width: 42,

    height: 60,

    speed: 6

};


/* 쓰레기통 */

let bin = {

    x: 700,

    y: 285,

    width: 70,

    height: 90

};


/* 접근 금지 거리 */

let forbiddenDistance = 220;


/* =========================
   LEVEL SETTINGS
========================= */

function getLevelSettings() {

    return {

        gravity:
            0.28 +
            (level - 1) * 0.045,

        binSize:
            Math.max(
                45,
                75 - (level - 1) * 4
            ),

        forbidden:
            Math.min(
                300,
                220 + (level - 1) * 8
            ),

        windPower:
            0.04 +
            level * 0.012

    };

}


/* =========================
   NEW BIN
========================= */

function newBin() {

    const settings =
        getLevelSettings();

    bin.width = settings.binSize;

    bin.height =
        settings.binSize * 1.25;

    bin.x =
        560 +
        Math.random() * 280;

    bin.x =
        Math.min(
            canvas.width -
            bin.width -
            20,
            bin.x
        );

    bin.y =
        285 +
        Math.random() * 20;


    forbiddenDistance =
        settings.forbidden;


    /*
       플레이어와 쓰레기통의
       거리가 너무 가까워지지 않게
    */

    const playerCenter =
        player.x +
        player.width / 2;

    const binCenter =
        bin.x +
        bin.width / 2;

    if (
        Math.abs(
            binCenter -
            playerCenter
        ) < forbiddenDistance
    ) {

        bin.x =
            player.x +
            forbiddenDistance;

        bin.x =
            Math.min(
                canvas.width -
                bin.width -
                20,
                bin.x
            );
    }


    /*
       레벨마다 바람을 한 번만 결정
       → 날아가는 동안 바람이 바뀌지 않음
    */

    wind =
        (Math.random() * 2 - 1)
        * settings.windPower;

}


/* =========================
   PLAYER
========================= */

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


    angle =
        Math.max(
            15,
            Math.min(80, angle)
        );


    player.x =
        Math.max(
            25,
            Math.min(
                canvas.width - 430,
                player.x
            )
        );


    /*
       쓰레기통 접근 제한
    */

    const playerCenter =
        player.x +
        player.width / 2;

    const binCenter =
        bin.x +
        bin.width / 2;

    const distance =
        Math.abs(
            binCenter -
            playerCenter
        );


    if (
        distance <
        forbiddenDistance
    ) {

        if (
            playerCenter <
            binCenter
        ) {

            player.x =
                binCenter -
                forbiddenDistance -
                player.width / 2;

        } else {

            player.x =
                binCenter +
                forbiddenDistance -
                player.width / 2;

        }

    }

}


/* =========================
   THROW
========================= */

function throwTrash() {

    initAudio();

    const radians =
        angle *
        Math.PI / 180;


    const speed =
        11 +
        Math.min(
            level * 0.3,
            5
        );


    projectile = {

        x:
            player.x + 50,

        y:
            player.y - 20,

        vx:
            Math.cos(radians)
            * speed,

        vy:
            -Math.sin(radians)
            * speed,

        radius: 13,

        rotation: 0

    };

}


/* =========================
   PROJECTILE
========================= */

function updateProjectile() {

    if (!projectile) return;


    const settings =
        getLevelSettings();


    projectile.vx += wind;

    projectile.x +=
        projectile.vx;

    projectile.y +=
        projectile.vy;

    projectile.vy +=
        settings.gravity;

    projectile.rotation += 0.25;


    /*
       쓰레기통 충돌
    */

    const insideX =
        projectile.x >
        bin.x - 3 &&
        projectile.x <
        bin.x +
        bin.width + 3;


    const insideY =
        projectile.y >
        bin.y - 10 &&
        projectile.y <
        bin.y + 30;


    if (
        insideX &&
        insideY
    ) {

        success();

        projectile = null;

        return;

    }


    /*
       땅에 떨어짐
    */

    if (
        projectile.y >
        390
    ) {

        fail();

        projectile = null;

        return;

    }


    /*
       화면 밖
    */

    if (
        projectile.x < -100 ||
        projectile.x >
            canvas.width + 100 ||
        projectile.y < -100
    ) {

        fail();

        projectile = null;

    }

}


/* =========================
   SUCCESS
========================= */

function success() {

    combo++;


    let earned =
        100 * level;


    if (combo >= 2) {

        earned +=
            combo * 30;

    }


    score += earned;


    document.getElementById(
        "score"
    ).textContent = score;


    document.getElementById(
        "combo"
    ).textContent = combo;


    successSound();


    showMessage(
        "🎯 PERFECT! +" +
        earned
    );


    createParticles(
        bin.x +
        bin.width / 2,

        bin.y
    );


    level++;


    document.getElementById(
        "level"
    ).textContent = level;


    newBin();

}


/* =========================
   FAIL
========================= */

function fail() {

    combo = 0;

    life--;


    document.getElementById(
        "combo"
    ).textContent = combo;


    updateLife();


    /*
       실패 소리
    */

    missSound();


    /*
       목숨 감소 소리
    */

    setTimeout(() => {

        lifeLostSound();

    }, 150);


    if (life <= 0) {

        gameOver = true;


        setTimeout(() => {

            gameOverSound();

        }, 350);


        showMessage(
            "💀 GAME OVER<br>" +
            "R을 눌러 다시 시작"
        );


    } else {

        showMessage(
            "💨 MISS!<br>" +
            "❤️ 목숨 -1"
        );

    }

}


/* =========================
   LIFE
========================= */

function updateLife() {

    let hearts = "";

    for (
        let i = 0;
        i < life;
        i++
    ) {

        hearts += "❤️ ";

    }


    document.getElementById(
        "life"
    ).textContent =
        hearts.trim();

}


/* =========================
   PARTICLES
========================= */

function createParticles(x, y) {

    for (
        let i = 0;
        i < 20;
        i++
    ) {

        particles.push({

            x: x,

            y: y,

            vx:
                (Math.random() - 0.5)
                * 6,

            vy:
                (Math.random() - 0.5)
                * 6,

            life: 1

        });

    }

}


function updateParticles() {

    particles.forEach(p => {

        p.x += p.vx;

        p.y += p.vy;

        p.vy += 0.1;

        p.life -= 0.025;

    });


    particles =
        particles.filter(
            p => p.life > 0
        );

}


/* =========================
   MESSAGE
========================= */

let messageTimer = null;


function showMessage(text) {

    const message =
        document.getElementById(
            "message"
        );


    message.innerHTML = text;

    message.style.opacity = 1;


    clearTimeout(messageTimer);


    messageTimer =
        setTimeout(() => {

            message.style.opacity = 0;

        }, 900);

}


/* =========================
   DRAW
========================= */

function drawBackground() {

    ctx.fillStyle =
        "#dff1e6";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    /*
       하늘
    */

    ctx.fillStyle =
        "#d4ebdf";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        300
    );


    /*
       바닥
    */

    ctx.fillStyle =
        "#a9d1b9";

    ctx.fillRect(
        0,
        375,
        canvas.width,
        55
    );


    /*
       접근 제한 영역
    */

    const centerX =
        bin.x +
        bin.width / 2;


    ctx.beginPath();

    ctx.arc(
        centerX,
        bin.y +
        bin.height / 2,

        forbiddenDistance,

        Math.PI,
        Math.PI * 2
    );


    ctx.strokeStyle =
        "rgba(220,70,70,0.65)";

    ctx.lineWidth = 2;

    ctx.setLineDash([8, 8]);

    ctx.stroke();

    ctx.setLineDash([]);


    /*
       안내
    */

    ctx.fillStyle =
        "#b24b4b";

    ctx.font =
        "13px Arial";

    ctx.fillText(
        "APPROACH LIMIT",
        centerX - 48,
        bin.y +
        bin.height / 2 -
        forbiddenDistance -
        8
    );

}


function drawPlayer() {

    /*
       몸
    */

    ctx.fillStyle =
        "#245c45";

    ctx.fillRect(
        player.x,
        player.y,
        player.width,
        player.height
    );


    /*
       머리
    */

    ctx.beginPath();

    ctx.arc(
        player.x + 21,
        player.y - 8,
        17,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        "#f1c7a5";

    ctx.fill();


    /*
       팔
    */

    ctx.strokeStyle =
        "#245c45";

    ctx.lineWidth = 7;

    ctx.beginPath();

    ctx.moveTo(
        player.x + 38,
        player.y + 20
    );

    ctx.lineTo(
        player.x + 60,
        player.y + 3
    );

    ctx.stroke();


    /*
       던지는 방향
    */

    const radians =
        angle *
        Math.PI / 180;


    ctx.strokeStyle =
        "rgba(36,92,69,0.45)";

    ctx.lineWidth = 2;

    ctx.beginPath();

    ctx.moveTo(
        player.x + 52,
        player.y
    );

    ctx.lineTo(
        player.x +
        52 +
        Math.cos(radians) * 65,

        player.y -
        Math.sin(radians) * 65
    );

    ctx.stroke();


    ctx.fillStyle =
        "#245c45";

    ctx.font =
        "14px Arial";

    ctx.fillText(
        "ANGLE " +
        Math.round(angle) +
        "°",

        player.x - 3,
        player.y + 82
    );

}


function drawBin() {

    /*
       몸체
    */

    ctx.fillStyle =
        "#727b75";

    ctx.fillRect(
        bin.x,
        bin.y,
        bin.width,
        bin.height
    );


    /*
       테두리
    */

    ctx.strokeStyle =
        "#4d5550";

    ctx.lineWidth = 3;

    ctx.strokeRect(
        bin.x,
        bin.y,
        bin.width,
        bin.height
    );


    /*
       뚜껑
    */

    ctx.fillStyle =
        "#59615c";

    ctx.fillRect(
        bin.x - 5,
        bin.y - 8,
        bin.width + 10,
        10
    );


    /*
       입구
    */

    ctx.fillStyle =
        "#202622";

    ctx.fillRect(
        bin.x + 7,
        bin.y + 5,
        bin.width - 14,
        17
    );


    /*
       쓰레기통 표시
    */

    ctx.fillStyle =
        "#e5eee8";

    ctx.font =
        "bold 20px Arial";

    ctx.textAlign =
        "center";

    ctx.fillText(
        "♻",
        bin.x +
        bin.width / 2,

        bin.y +
        bin.height / 2 +
        8
    );

    ctx.textAlign =
        "left";

}


function drawProjectile() {

    if (!projectile) return;


    ctx.save();

    ctx.translate(
        projectile.x,
        projectile.y
    );

    ctx.rotate(
        projectile.rotation
    );


    /*
       쓰레기 봉투
    */

    ctx.fillStyle =
        "#777";

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        projectile.radius,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.fillStyle =
        "#444";

    ctx.fillRect(
        -7,
        -5,
        14,
        3
    );


    ctx.restore();

}


function drawParticles() {

    particles.forEach(p => {

        ctx.globalAlpha =
            p.life;

        ctx.fillStyle =
            "#2f8f62";

        ctx.fillRect(
            p.x,
            p.y,
            5,
            5
        );

    });


    ctx.globalAlpha = 1;

}


/* =========================
   WIND DISPLAY
========================= */

function drawWind() {

    if (!projectile) return;


    ctx.fillStyle =
        "#61776c";

    ctx.font =
        "13px Arial";


    let windText =
        wind > 0
        ? "→ WIND"
        : "← WIND";


    ctx.fillText(
        windText,
        20,
        25
    );

}


/* =========================
   GAME LOOP
========================= */

function gameLoop() {

    if (!gameOver) {

        updatePlayer();

        updateProjectile();

    }


    updateParticles();


    drawBackground();

    drawBin();

    drawPlayer();

    drawProjectile();

    drawParticles();

    drawWind();


    requestAnimationFrame(
        gameLoop
    );

}


/* =========================
   KEYBOARD
========================= */

window.addEventListener(
    "keydown",
    function(e) {

        initAudio();


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


        if (
            e.code === "Space"
        ) {

            if (
                !gameOver &&
                projectile === null
            ) {

                throwTrash();

            }

        }


        if (
            (e.key === "r" ||
             e.key === "R") &&
            gameOver
        ) {

            restart();

        }

    }
);


window.addEventListener(
    "keyup",
    function(e) {

        keys[e.key] = false;

    }
);


/*
   Canvas를 클릭하면 키보드 입력 활성화
*/

canvas.addEventListener(
    "click",
    function() {

        canvas.focus();

        initAudio();

    }
);


/* =========================
   RESTART
========================= */

function restart() {

    level = 1;

    score = 0;

    life = 3;

    combo = 0;

    angle = 45;

    gameOver = false;

    projectile = null;

    particles = [];

    player.x = 90;


    document.getElementById(
        "level"
    ).textContent = level;


    document.getElementById(
        "score"
    ).textContent = score;


    document.getElementById(
        "combo"
    ).textContent = combo;


    updateLife();

    newBin();

}


/* =========================
   START
========================= */

newBin();

updateLife();

gameLoop();

canvas.focus();

</script>

</body>
</html>
"""


components.html(
    game_html,
    height=650,
    scrolling=False
)
