import streamlit as st
import random
import math

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="쓰레기통에 골인!",
    page_icon="🗑️",
    layout="centered"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #f3f8f5 0%, #ffffff 65%);
}

/* 제목 */
.game-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #245c45;
    margin-top: 25px;
    margin-bottom: 5px;
}

.game-subtitle {
    text-align: center;
    color: #718078;
    font-size: 16px;
    margin-bottom: 30px;
}

/* 게임 화면 */
.game-area {
    background: linear-gradient(180deg, #dff4e8 0%, #f8fcfa 100%);
    border: 1px solid #d5e9dd;
    border-radius: 24px;
    height: 300px;
    position: relative;
    margin-bottom: 25px;
    overflow: hidden;
}

/* 바닥 */
.ground {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 45px;
    background: #d9e4dc;
}

/* 쓰레기통 */
.trash-can {
    position: absolute;
    right: 70px;
    bottom: 43px;
    font-size: 70px;
}

/* 쓰레기 */
.trash {
    position: absolute;
    left: 70px;
    bottom: 45px;
    font-size: 48px;
}

/* 점수 카드 */
.score-card {
    background: white;
    border: 1px solid #e1ebe5;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(30, 80, 55, 0.06);
}

.score-number {
    font-size: 30px;
    font-weight: 800;
    color: #245c45;
}

.score-label {
    color: #7b8981;
    font-size: 13px;
}

/* 결과 */
.result-success {
    background: #e7f8ed;
    color: #247044;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    font-weight: 700;
    margin-top: 20px;
}

.result-fail {
    background: #fff1f1;
    color: #a84b4b;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    font-weight: 700;
    margin-top: 20px;
}

.final-card {
    background: white;
    border: 1px solid #dfeae3;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 0 8px 25px rgba(30, 80, 55, 0.08);
}

.final-score {
    font-size: 48px;
    font-weight: 800;
    color: #245c45;
}

.footer {
    text-align: center;
    color: #a0aaa5;
    font-size: 13px;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "best_combo" not in st.session_state:
    st.session_state.best_combo = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "trash" not in st.session_state:
    st.session_state.trash = "🥤"


# --------------------------------------------------
# 새 게임
# --------------------------------------------------

def reset_game():
    st.session_state.score = 0
    st.session_state.turn = 0
    st.session_state.combo = 0
    st.session_state.best_combo = 0
    st.session_state.last_result = None
    st.session_state.game_over = False
    st.session_state.trash = "🥤"


# --------------------------------------------------
# 제목
# --------------------------------------------------

st.markdown(
    '<div class="game-title">🗑️ 쓰레기통에 골인!</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">방향과 세기를 조절해서 쓰레기를 쓰레기통에 던져보세요!</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 게임 종료 전
# --------------------------------------------------

if not st.session_state.game_over:

    # 게임 화면
    st.markdown(
        f"""
        <div class="game-area">
            <div class="trash">{st.session_state.trash}</div>
            <div class="trash-can">🗑️</div>
            <div class="ground"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 점수 정보
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">{st.session_state.score}</div>
                <div class="score-label">점수</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {st.session_state.turn}/10
                </div>
                <div class="score-label">던진 횟수</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {st.session_state.combo}
                </div>
                <div class="score-label">현재 콤보</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # --------------------------------------------------
    # 쓰레기 선택
    # --------------------------------------------------

    st.subheader("🧹 어떤 쓰레기를 던질까요?")

    trash_options = {
        "🥤 플라스틱 컵": "🥤",
        "📄 종이": "📄",
        "🍌 바나나 껍질": "🍌",
        "🥫 캔": "🥫",
        "🍾 페트병": "🍾"
    }

    selected_trash = st.selectbox(
        "쓰레기 선택",
        list(trash_options.keys()),
        label_visibility="collapsed"
    )

    st.session_state.trash = trash_options[selected_trash]

    # --------------------------------------------------
    # 조작
    # --------------------------------------------------

    st.subheader("🎯 던지기 조절")

    angle = st.slider(
        "↗️ 방향",
        min_value=0,
        max_value=100,
        value=50,
        help="50에 가까울수록 쓰레기통 방향입니다."
    )

    power = st.slider(
        "💨 던지는 힘",
        min_value=0,
        max_value=100,
        value=50,
        help="적당한 힘으로 던져보세요."
    )

    # --------------------------------------------------
    # 던지기
    # --------------------------------------------------

    if st.button("🗑️ 던지기!", use_container_width=True):

        # 목표값
        target_angle = 68
        target_power = 64

        # 오차 계산
        angle_error = abs(angle - target_angle)
        power_error = abs(power - target_power)

        # 약간의 랜덤 요소
        random_error = random.randint(-5, 5)

        total_error = angle_error + power_error + random_error

        st.session_state.turn += 1

        # 성공 판정
        if total_error <= 18:

            base_score = 100

            # 정확도에 따른 추가 점수
            accuracy_bonus = max(
                0,
                int((18 - total_error) * 5)
            )

            # 콤보
            st.session_state.combo += 1

            combo_bonus = (
                st.session_state.combo - 1
            ) * 20

            earned_score = (
                base_score
                + accuracy_bonus
                + combo_bonus
            )

            st.session_state.score += earned_score

            st.session_state.best_combo = max(
                st.session_state.best_combo,
                st.session_state.combo
            )

            st.session_state.last_result = (
                "success",
                earned_score
            )

        else:

            st.session_state.combo = 0

            st.session_state.last_result = (
                "fail",
                0
            )

        # 10번 끝
        if st.session_state.turn >= 10:
            st.session_state.game_over = True

        st.rerun()

    # --------------------------------------------------
    # 최근 결과
    # --------------------------------------------------

    if st.session_state.last_result:

        result_type, earned_score = st.session_state.last_result

        if result_type == "success":

            st.markdown(
                f"""
                <div class="result-success">
                    🎉 골인 성공! +{earned_score}점<br>
                    현재 콤보: {st.session_state.combo}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="result-fail">
                    💨 아쉽게 빗나갔어요!<br>
                    방향과 힘을 조금 조절해보세요.
                </div>
                """,
                unsafe_allow_html=True
            )


# --------------------------------------------------
# 게임 종료
# --------------------------------------------------

else:

    st.markdown(
        """
        <div class="final-card">
            <div style="font-size: 55px;">🏆</div>
            <h2>게임 종료!</h2>
            <p>10번의 도전이 끝났습니다.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="final-card">
            <div style="color:#718078;">
                최종 점수
            </div>

            <div class="final-score">
                {st.session_state.score}점
            </div>

            <div style="margin-top:15px;color:#718078;">
                최고 콤보 : {st.session_state.best_combo}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.session_state.score >= 1200:
        message = "🌟 완벽해요! 쓰레기통 명사수!"
    elif st.session_state.score >= 800:
        message = "👏 훌륭해요! 꽤 정확하게 던졌네요!"
    elif st.session_state.score >= 400:
        message = "👍 좋아요! 조금만 더 연습해봐요!"
    else:
        message = "💪 괜찮아요! 다음에는 더 높은 점수를 노려봐요!"

    st.markdown(
        f"""
        <div class="result-success">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🔄 다시 플레이", use_container_width=True):
        reset_game()
        st.rerun()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ♻️ 쓰레기는 올바르게 분리배출해요!
    </div>
    """,
    unsafe_allow_html=True
)
