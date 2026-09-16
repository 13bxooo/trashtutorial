import streamlit as st
import streamlit.components.v1 as components


# ==========================================
# STREAMLIT 설정
# ==========================================

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
    margin-bottom: 5px;
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


# ==========================================
# GAME HTML
# ==========================================

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

    background: #dcefe5;

    font-family:
        Arial,
        sans-serif;

    overflow: hidden;
}


/* ==========================================
   전체 게임
========================================== */

#gameWrapper {

    width: 100%;

    height: 620px;

    display: flex;

    flex-direction: column;

    align-items: center;

}


/* ==========================================
   정보창
========================================== */

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

    font-size: 12px;

    font-weight: bold;

    color: #245c45;

}


.value {

    font-size: 20px;

    font-weight: bold;

    color: #164d39;

    margin-top: 3px;

    transition:
        transform 0.1s;

}


/* ==========================================
   Canvas
========================================== */

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


/* ==========================================
   조작 설명
========================================== */

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


/* ==========================================
   메시지
========================================== */

#message {

    position: absolute;

    top: 235px;

    left: 50%;

    transform: translateX(-50%);

    font-size: 30px;

    font-weight: bold;

    color: #245c45;

    text-align: center;

    pointer-events: none;

    opacity: 0;

    transition:
        opacity 0.15s;

    z-index: 10;

    white-space: nowrap;

}

</style>

</head>


<body>


<div id="gameWrapper">


    <!-- =====================================
         정보
    ====================================== -->

    <div id="info">


        <div class="box">

            <div class="label">
                LEVEL
            </div>

            <div
                class="value"
                id="level"
            >
                1
            </div>

        </div>


        <div class="box">

            <div class="label">
                TIME
            </div>

            <div
                class="value"
                id="time"
            >
                30
            </div>

        </div>


        <div class="box">

            <div class="label">
                SCORE
            </div>

            <div
                class="value"
                id="score"
            >
                0
            </div>

        </div>


        <div class="box">

            <div class="label">
                LIFE
            </div>

            <div
                class="value"
                id="life"
            >
                ❤️ ❤️ ❤️
            </div>

        </div>


        <div class="box">

            <div class="label">
                COMBO
            </div>

            <div
                class="value"
                id="combo"
            >
                0
            </div>

        </div>


    </div>


    <!-- =====================================
         게임 화면
    ====================================== -->

    <canvas
        id="gameCanvas"
        tabindex="0"
    ></canvas>


    <!-- =====================================
         조작법
    ====================================== -->

    <div id="controls">

        ← → 이동　|　
        ↑ ↓ 각도　|　
        SPACE 던지기　|　
        R 재시작

    </div>


</div>


<div id="message"></div>


<script>


/* ==========================================
   CANVAS
========================================== */

const canvas =
    document.getElementById(
        "gameCanvas"
    );

const ctx =
    canvas.getContext("2d");


canvas.width = 900;

canvas.height = 430;


/* ==========================================
   AUDIO
========================================== */

let audioContext = null;


function initAudio() {

    if (!audioContext) {

        audioContext =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();

    }


    if (
        audioContext.state ===
        "suspended"
    ) {

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

    oscillator.frequency.value =
        frequency;


    gain.gain.setValueAtTime(
        volume,
        audioContext.currentTime
    );


    gain.gain.exponentialRampToValueAtTime(
        0.001,
        audioContext.currentTime +
        duration
    );


    oscillator.connect(gain);

    gain.connect(
        audioContext.destination
    );


    oscillator.start();


    oscillator.stop(
        audioContext.currentTime +
        duration
    );

}


/* ==========================================
   성공 효과음
========================================== */

function successSound() {

    playTone(
        660,
        0.12,
        "sine",
        0.08
    );


    setTimeout(() => {

        playTone(
            880,
            0.16,
            "sine",
            0.08
        );

    }, 100);

}


/* ==========================================
   실패 효과음
========================================== */

function missSound() {

    playTone(
        180,
        0.16,
        "triangle",
        0.09
    );


    setTimeout(() => {

        playTone(
            120,
            0.20,
            "triangle",
            0.07
        );

    }, 100);

}


/* ==========================================
   목숨 감소 효과음
========================================== */

function lifeLostSound() {

    playTone(
        240,
        0.15,
        "square",
        0.07
    );


    setTimeout(() => {

        playTone(
            150,
            0.28,
            "square",
            0.06
        );

    }, 120);

}


/* ==========================================
   게임오버 효과음
========================================== */

function gameOverSound() {

    playTone(
        300,
        0.20,
        "sawtooth",
        0.06
    );


    setTimeout(() => {

        playTone(
            220,
            0.20,
            "sawtooth",
            0.06
        );

    }, 180);


    setTimeout(() => {

        playTone(
            140,
            0.40,
            "sawtooth",
            0.05
        );

    }, 360);

}


/* ==========================================
   게임 변수
========================================== */

let level = 1;

let score = 0;

let life = 3;

let combo = 0;

let gameOver = false;


/* ==========================================
   시간
========================================== */

const GAME_TIME = 30;

let timeLeft = GAME_TIME;

let lastTime =
    performance.now();


/* ==========================================
   키
========================================== */

let keys = {};

let angle = 45;


/* ==========================================
   플레이어
========================================== */

let player = {

    x: 90,

    y: 325,

    width: 42,

    height: 60,

    speed: 6

};


/* ==========================================
   쓰레기
========================================== */

let projectile = null;


/* ==========================================
   쓰레기통
========================================== */

let bin = {

    x: 700,

    y: 285,

    width: 70,

    height: 90

};


/* ==========================================
   쓰레기통 움직임 변수
========================================== */

let gameTime = 0;

let binBaseX = 700;

let binBaseY = 285;

let forbiddenDistance = 220;

let wind = 0;


/* ==========================================
   파티클
========================================== */

let particles = [];


/* ==========================================
   메시지 타이머
========================================== */

let messageTimer = null;


/* ==========================================
   레벨 설정
========================================== */

function getLevelSettings() {

    return {

        gravity:
            0.28 +
            (level - 1) * 0.045,


        binSize:
            Math.max(
                45,
                75 -
                (level - 1) * 4
            ),


        forbidden:
            Math.min(
                300,
                220 +
                (level - 1) * 8
            ),


        windPower:
            0.04 +
            level * 0.012

    };

}


/* ==========================================
   새로운 쓰레기통
========================================== */

function newBin() {

    const settings =
        getLevelSettings();


    bin.width =
        settings.binSize;


    bin.height =
        settings.binSize * 1.25;


    /*
       새로운 기본 위치
    */

    binBaseX =
        580 +
        Math.random() * 220;


    binBaseY =
        270 +
        Math.random() * 45;


    /*
       화면 밖 방지
    */

    binBaseX =
        Math.min(
            canvas.width -
            bin.width -
            20,

            binBaseX
        );


    /*
       플레이어와 너무 가까운 경우
       오른쪽으로 이동
    */

    const playerCenter =
        player.x +
        player.width / 2;


    const requiredX =
        playerCenter +
        settings.forbidden;


    if (
        binBaseX <
        requiredX
    ) {

        binBaseX =
            Math.min(
                canvas.width -
                bin.width -
                20,

                requiredX
            );

    }


    /*
       바람은 레벨 시작마다
       한 번 결정
    */

    wind =
        (
            Math.random() * 2 - 1
        ) *
        settings.windPower;


    forbiddenDistance =
        settings.forbidden;


    /*
       실제 위치 초기화
    */

    bin.x = binBaseX;

    bin.y = binBaseY;

}


/* ==========================================
   쓰레기통 움직임
========================================== */

function updateBin(deltaTime) {

    if (gameOver) return;


    gameTime += deltaTime;


    const t =
        gameTime;


    let moveX = 0;

    let moveY = 0;

    let shakeX = 0;

    let shakeY = 0;


    /* ======================================
       LEVEL 1
       거의 고정
    ====================================== */

    if (level === 1) {

        moveX =
            Math.sin(
                t * 0.0015
            ) * 8;


        moveY =
            Math.sin(
                t * 0.0018
            ) * 3;

    }


    /* ======================================
       LEVEL 2
       좌우 움직임
    ====================================== */

    else if (level === 2) {

        moveX =
            Math.sin(
                t * 0.0022
            ) * 30;


        moveY =
            Math.sin(
                t * 0.0028
            ) * 8;

    }


    /* ======================================
       LEVEL 3
       본격적인 움직임
    ====================================== */

    else if (level === 3) {

        moveX =
            Math.sin(
                t * 0.0032
            ) * 65;


        moveY =
            Math.sin(
                t * 0.0040
            ) * 25;

    }


    /* ======================================
       LEVEL 4
       더 큰 움직임
    ====================================== */

    else if (level === 4) {

        moveX =
            Math.sin(
                t * 0.0040
            ) * 100;


        moveY =
            Math.sin(
                t * 0.0055
            ) * 40;


        moveX +=
            Math.sin(
                t * 0.008
            ) * 25;

    }


    /* ======================================
       LEVEL 5+
       큰 움직임 + 진동
    ====================================== */

    else {

        moveX =
            Math.sin(
                t * 0.0045
            ) *
            (
                110 +
                level * 5
            );


        moveY =
            Math.sin(
                t * 0.0060
            ) *
            (
                45 +
                level * 2
            );


        /*
           복합 움직임
        */

        moveX +=
            Math.sin(
                t * 0.012
            ) *
            (
                30 +
                level * 2
            );


        moveY +=
            Math.sin(
                t * 0.015
            ) *
            (
                15 +
                level
            );


        /*
           진동
        */

        const vibration =
            Math.min(
                3 +
                (level - 5) * 0.8,

                8
            );


        shakeX =
            Math.sin(
                t * 0.08
            ) *
            vibration;


        shakeY =
            Math.cos(
                t * 0.095
            ) *
            vibration;


        /*
           Lv.7부터
           더욱 불규칙한 진동
        */

        if (level >= 7) {

            shakeX +=
                Math.sin(
                    t * 0.17
                ) *
                vibration *
                0.5;


            shakeY +=
                Math.cos(
                    t * 0.21
                ) *
                vibration *
                0.5;

        }

    }


    /*
       실제 위치
    */

    bin.x =
        binBaseX +
        moveX +
        shakeX;


    bin.y =
        binBaseY +
        moveY +
        shakeY;


    /*
       화면 밖 방지
    */

    bin.x =
        Math.max(
            480,

            Math.min(
                canvas.width -
                bin.width -
                15,

                bin.x
            )
        );


    bin.y =
        Math.max(
            210,

            Math.min(
                330,

                bin.y
            )
        );

}


/* ==========================================
   플레이어
========================================== */

function updatePlayer() {

    if (
        keys["ArrowLeft"]
    ) {

        player.x -=
            player.speed;

    }


    if (
        keys["ArrowRight"]
    ) {

        player.x +=
            player.speed;

    }


    if (
        keys["ArrowUp"]
    ) {

        angle += 0.8;

    }


    if (
        keys["ArrowDown"]
    ) {

        angle -= 0.8;

    }


    /*
       각도 제한
    */

    angle =
        Math.max(
            15,

            Math.min(
                80,
                angle
            )
        );


    /*
       기본 이동 제한
    */

    player.x =
        Math.max(
            25,

            Math.min(
                canvas.width -
                430,

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

        }

        else {

            player.x =
                binCenter +
                forbiddenDistance -
                player.width / 2;

        }

    }

}


/* ==========================================
   쓰레기 던지기
========================================== */

function throwTrash() {

    initAudio();


    const radians =
        angle *
        Math.PI /
        180;


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
            Math.cos(
                radians
            ) *
            speed,

        vy:
            -Math.sin(
                radians
            ) *
            speed,

        radius: 13,

        rotation: 0

    };

}


/* ==========================================
   쓰레기 이동
========================================== */

function updateProjectile() {

    if (
        !projectile
    ) return;


    const settings =
        getLevelSettings();


    /*
       바람
    */

    projectile.vx +=
        wind;


    /*
       위치
    */

    projectile.x +=
        projectile.vx;


    projectile.y +=
        projectile.vy;


    /*
       중력
    */

    projectile.vy +=
        settings.gravity;


    projectile.rotation +=
        0.25;


    /*
       쓰레기통과 충돌
    */

    const insideX =
        projectile.x >
            bin.x - 5 &&

        projectile.x <
            bin.x +
            bin.width +
            5;


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

        projectile =
            null;

        return;

    }


    /*
       땅
    */

    if (
        projectile.y >
        390
    ) {

        fail();

        projectile =
            null;

        return;

    }


    /*
       화면 밖
    */

    if (

        projectile.x <
            -100 ||

        projectile.x >
            canvas.width + 100 ||

        projectile.y <
            -100

    ) {

        fail();

        projectile =
            null;

    }

}


/* ==========================================
   성공
========================================== */

function success() {

    combo++;


    let earned =
        100 * level;


    /*
       콤보 보너스
    */

    if (
        combo >= 2
    ) {

        earned +=
            combo * 30;

    }


    score +=
        earned;


    document.getElementById(
        "score"
    ).textContent =
        score;


    document.getElementById(
        "combo"
    ).textContent =
        combo;


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


    /*
       레벨업
    */

    level++;


    document.getElementById(
        "level"
    ).textContent =
        level;


    /*
       새로운 쓰레기통
    */

    newBin();

}


/* ==========================================
   실패
========================================== */

function fail() {

    combo = 0;

    life--;


    document.getElementById(
        "combo"
    ).textContent =
        combo;


    updateLife();


    /*
       실패음
    */

    missSound();


    /*
       목숨 감소음
    */

    setTimeout(
        () => {

            lifeLostSound();

        },

        150
    );


    /*
       목숨 0
    */

    if (
        life <= 0
    ) {

        gameOver =
            true;


        setTimeout(
            () => {

                gameOverSound();

            },

            350
        );


        showMessage(
            "💀 GAME OVER<br>" +
            "R을 눌러 다시 시작"
        );

    }

    else {

        showMessage(
            "💨 MISS!<br>" +
            "❤️ 목숨 -1"
        );

    }

}


/* ==========================================
   목숨 표시
========================================== */

function updateLife() {

    let hearts = "";


    for (
        let i = 0;
        i < life;
        i++
    ) {

        hearts +=
            "❤️ ";

    }


    document.getElementById(
        "life"
    ).textContent =
        hearts.trim();

}


/* ==========================================
   시간
========================================== */

function updateTimer(
    deltaTime
) {

    if (gameOver)
        return;


    timeLeft -=
        deltaTime / 1000;


    timeLeft =
        Math.max(
            0,
            timeLeft
        );


    const timeElement =
        document.getElementById(
            "time"
        );


    timeElement.textContent =
        Math.ceil(
            timeLeft
        );


    /*
       10초 이하
    */

    if (
        timeLeft <= 10
    ) {

        timeElement.style.color =
            "#d94b4b";


        timeElement.style.fontWeight =
            "900";


        timeElement.style.transform =
            Math.sin(
                performance.now() / 100
            ) > 0

            ? "scale(1.12)"

            : "scale(1)";

    }


    /*
       시간 종료
    */

    if (
        timeLeft <= 0
    ) {

        gameOver =
            true;


        gameOverSound();


        showMessage(
            "⏰ TIME OVER!<br>" +
            "R을 눌러 다시 시작"
        );

    }

}


/* ==========================================
   파티클
========================================== */

function createParticles(
    x,
    y
) {

    for (
        let i = 0;
        i < 20;
        i++
    ) {

        particles.push({

            x: x,

            y: y,

            vx:
                (
                    Math.random() -
                    0.5
                ) * 6,

            vy:
                (
                    Math.random() -
                    0.5
                ) * 6,

            life: 1

        });

    }

}


function updateParticles() {

    particles.forEach(
        p => {

            p.x +=
                p.vx;


            p.y +=
                p.vy;


            p.vy +=
                0.1;


            p.life -=
                0.025;

        }
    );


    particles =
        particles.filter(
            p =>
                p.life > 0
        );

}


/* ==========================================
   메시지
========================================== */

function showMessage(
    text
) {

    const message =
        document.getElementById(
            "message"
        );


    message.innerHTML =
        text;


    message.style.opacity =
        1;


    clearTimeout(
        messageTimer
    );


    messageTimer =
        setTimeout(
            () => {

                message.style.opacity =
                    0;

            },

            1000
        );

}


/* ==========================================
   배경
========================================== */

function drawBackground() {

    /*
       하늘
    */

    ctx.fillStyle =
        "#d4ebdf";


    ctx.fillRect(
        0,
        0,
        canvas.width,
        375
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
       접근 제한 표시
    */

    const centerX =
        bin.x +
        bin.width / 2;


    const centerY =
        bin.y +
        bin.height / 2;


    ctx.beginPath();


    ctx.arc(
        centerX,
        centerY,
        forbiddenDistance,
        Math.PI,
        Math.PI * 2
    );


    ctx.strokeStyle =
        "rgba(220,70,70,0.6)";


    ctx.lineWidth =
        2;


    ctx.setLineDash(
        [8, 8]
    );


    ctx.stroke();


    ctx.setLineDash(
        []
    );


    /*
       안내
    */

    ctx.fillStyle =
        "#b24b4b";


    ctx.font =
        "13px Arial";


    ctx.textAlign =
        "center";


    ctx.fillText(
        "APPROACH LIMIT",
        centerX,
        centerY -
        forbiddenDistance -
        8
    );


    ctx.textAlign =
        "left";

}


/* ==========================================
   플레이어 그리기
========================================== */

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


    ctx.lineWidth =
        7;


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
       각도 표시
    */

    const radians =
        angle *
        Math.PI /
        180;


    ctx.strokeStyle =
        "rgba(36,92,69,0.45)";


    ctx.lineWidth =
        2;


    ctx.beginPath();


    ctx.moveTo(
        player.x + 52,
        player.y
    );


    ctx.lineTo(

        player.x +
        52 +
        Math.cos(
            radians
        ) * 65,

        player.y -
        Math.sin(
            radians
        ) * 65

    );


    ctx.stroke();


    /*
       각도 글자
    */

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


/* ==========================================
   쓰레기통 그리기
========================================== */

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


    ctx.lineWidth =
        3;


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
       재활용 표시
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


/* ==========================================
   쓰레기 그리기
========================================== */

function drawProjectile() {

    if (!projectile)
        return;


    ctx.save();


    ctx.translate(
        projectile.x,
        projectile.y
    );


    ctx.rotate(
        projectile.rotation
    );


    /*
       쓰레기
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


    /*
       묶인 부분
    */

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


/* ==========================================
   파티클 그리기
========================================== */

function drawParticles() {

    particles.forEach(
        p => {

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

        }
    );


    ctx.globalAlpha = 1;

}


/* ==========================================
   바람 표시
========================================== */

function drawWind() {

    if (!projectile)
        return;


    ctx.fillStyle =
        "#61776c";


    ctx.font =
        "13px Arial";


    const windText =
        wind > 0
        ? "→ WIND"
        : "← WIND";


    ctx.fillText(
        windText,
        20,
        25
    );

}


/* ==========================================
   키보드
========================================== */

window.addEventListener(
    "keydown",
    function(e) {

        initAudio();


        /*
           기본 브라우저 동작 방지
        */

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


        /*
           SPACE
        */

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


        /*
           R
        */

        if (

            (
                e.key === "r" ||
                e.key === "R"
            )

            &&

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


/* ==========================================
   Canvas 클릭
========================================== */

canvas.addEventListener(
    "click",
    function() {

        canvas.focus();

        initAudio();

    }
);


/* ==========================================
   재시작
========================================== */

function restart() {

    level = 1;

    score = 0;

    life = 3;

    combo = 0;

    angle = 45;

    timeLeft =
        GAME_TIME;

    gameOver = false;

    projectile = null;

    particles = [];

    player.x = 90;

    gameTime = 0;


    const timeElement =
        document.getElementById(
            "time"
        );


    timeElement.style.color =
        "#164d39";


    timeElement.style.transform =
        "scale(1)";


    document.getElementById(
        "level"
    ).textContent =
        level;


    document.getElementById(
        "score"
    ).textContent =
        score;


    document.getElementById(
        "combo"
    ).textContent =
        combo;


    timeElement.textContent =
        GAME_TIME;


    updateLife();

    newBin();

}


/* ==========================================
   게임 루프
========================================== */

function gameLoop() {

    const now =
        performance.now();


    const deltaTime =
        now -
        lastTime;


    lastTime =
        now;


    if (!gameOver) {

        updateTimer(
            deltaTime
        );

        updateBin(
            deltaTime
        );

        updatePlayer();

        updateProjectile();

    }


    updateParticles();


    /*
       그리기
    */

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


/* ==========================================
   게임 시작
========================================== */

newBin();

updateLife();

canvas.focus();

gameLoop();

</script>

</body>

</html>
"""


# ==========================================
# GAME 실행
# ==========================================

components.html(
    game_html,
    height=700,
    scrolling=False
)
