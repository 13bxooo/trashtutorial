import streamlit as st


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="MBTI 여행지 추천",
    page_icon="✈️",
    layout="centered"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f5f9ff 0%, #ffffff 55%);
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #163a63;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #6b7c93;
        margin-bottom: 35px;
    }

    .select-title {
        font-size: 20px;
        font-weight: 700;
        color: #163a63;
        margin-bottom: 8px;
    }

    .result-card {
        background: white;
        border-radius: 20px;
        padding: 28px;
        margin-top: 25px;
        border: 1px solid #e4edf7;
        box-shadow: 0 8px 25px rgba(35, 82, 125, 0.08);
    }

    .result-label {
        color: #4a90c2;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .destination {
        color: #163a63;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .description {
        color: #526579;
        font-size: 16px;
        line-height: 1.7;
    }

    .reason-box {
        background: #f1f7fd;
        border-radius: 14px;
        padding: 17px;
        margin-top: 18px;
        color: #315574;
        line-height: 1.6;
    }

    .tag {
        display: inline-block;
        background: #e4f2ff;
        color: #2670a8;
        border-radius: 20px;
        padding: 6px 12px;
        margin-right: 5px;
        margin-bottom: 5px;
        font-size: 13px;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        color: #9aa9b8;
        font-size: 13px;
        margin-top: 45px;
        margin-bottom: 20px;
    }

    div[data-testid="stButton"] button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MBTI 여행지 데이터
# --------------------------------------------------

travel_data = {
    "ISTJ": {
        "destination": "경주",
        "emoji": "🏛️",
        "description": "차분하게 역사와 문화를 둘러보며 여행의 의미를 느끼기 좋은 곳이에요.",
        "reason": "계획적으로 움직이는 여행을 좋아한다면 경주의 역사 유적과 문화 공간을 일정에 맞춰 둘러보는 여행이 잘 어울려요.",
        "tags": ["역사", "문화", "차분한 여행", "계획형"]
    },

    "ISFJ": {
        "destination": "전주",
        "emoji": "🏘️",
        "description": "한옥과 맛있는 음식, 여유로운 분위기를 함께 즐길 수 있는 여행지예요.",
        "reason": "편안하고 따뜻한 분위기에서 맛있는 음식과 문화 체험을 즐기고 싶을 때 잘 어울리는 여행지예요.",
        "tags": ["한옥", "맛집", "문화", "여유"]
    },

    "INFJ": {
        "destination": "제주",
        "emoji": "🌿",
        "description": "아름다운 자연 속에서 천천히 생각하고 휴식하기 좋은 곳이에요.",
        "reason": "복잡한 일상에서 벗어나 자연을 바라보며 여유롭게 시간을 보내고 싶을 때 제주도의 자연 풍경이 잘 어울려요.",
        "tags": ["자연", "힐링", "감성", "산책"]
    },

    "INTJ": {
        "destination": "서울",
        "emoji": "🏙️",
        "description": "다양한 문화와 전시, 공간을 효율적으로 탐방할 수 있는 도시예요.",
        "reason": "관심 분야를 직접 찾아보고 자신만의 일정으로 도시를 탐방하는 여행을 좋아한다면 서울이 잘 맞아요.",
        "tags": ["도시", "전시", "문화", "탐방"]
    },

    "ISTP": {
        "destination": "강릉",
        "emoji": "🌊",
        "description": "바다와 카페, 다양한 액티비티를 자유롭게 즐길 수 있는 곳이에요.",
        "reason": "정해진 일정에 얽매이기보다 그날의 기분에 따라 바다와 다양한 활동을 즐기는 여행에 잘 어울려요.",
        "tags": ["바다", "액티비티", "자유", "카페"]
    },

    "ISFP": {
        "destination": "통영",
        "emoji": "🎨",
        "description": "바다와 섬, 예술적인 공간이 어우러진 감성적인 여행지예요.",
        "reason": "아름다운 풍경과 예술적인 분위기를 천천히 즐기며 자신만의 시간을 보내기 좋은 곳이에요.",
        "tags": ["바다", "예술", "감성", "풍경"]
    },

    "INFP": {
        "destination": "제주",
        "emoji": "🌺",
        "description": "자연과 아름다운 풍경을 바라보며 자신만의 시간을 보내기 좋은 곳이에요.",
        "reason": "조용한 자연 속에서 산책하고 풍경을 감상하며 여유로운 시간을 보내는 여행과 잘 어울려요.",
        "tags": ["자연", "감성", "산책", "힐링"]
    },

    "INTP": {
        "destination": "대전",
        "emoji": "🔬",
        "description": "과학과 연구, 다양한 전시를 접할 수 있는 도시예요.",
        "reason": "과학관이나 연구 관련 공간처럼 새로운 지식을 탐구할 수 있는 장소를 방문하는 여행과 잘 어울려요.",
        "tags": ["과학", "탐구", "전시", "도시"]
    },

    "ESTP": {
        "destination": "부산",
        "emoji": "🌊",
        "description": "바다부터 맛집과 액티비티까지 다양한 경험을 즐길 수 있는 도시예요.",
        "reason": "새로운 경험을 직접 체험하고 활기찬 분위기를 즐기고 싶다면 부산의 다양한 관광지를 추천해요.",
        "tags": ["바다", "액티비티", "맛집", "도시"]
    },

    "ESFP": {
        "destination": "부산",
        "emoji": "🎡",
        "description": "맛집과 바다, 관광 명소를 다양하게 즐길 수 있는 활기찬 여행지예요.",
        "reason": "친구나 가족과 함께 돌아다니며 맛있는 음식과 재미있는 경험을 많이 만들고 싶을 때 잘 어울려요.",
        "tags": ["맛집", "바다", "관광", "즐거움"]
    },

    "ENFP": {
        "destination": "제주",
        "emoji": "🌴",
        "description": "새로운 장소를 발견하고 다양한 경험을 즐기기 좋은 여행지예요.",
        "reason": "한 가지 활동에 머무르기보다 자연, 카페, 관광지 등 여러 장소를 자유롭게 돌아다니는 여행과 잘 어울려요.",
        "tags": ["모험", "자연", "카페", "새로운 경험"]
    },

    "ENTP": {
        "destination": "서울",
        "emoji": "🚇",
        "description": "새로운 장소와 문화, 사람들을 다양하게 만날 수 있는 도시예요.",
        "reason": "매번 다른 장소를 탐방하고 새로운 경험을 찾아다니는 도시 여행을 즐기기에 좋아요.",
        "tags": ["도시", "탐방", "문화", "새로운 경험"]
    },

    "ESTJ": {
        "destination": "서울",
        "emoji": "🏙️",
        "description": "효율적인 이동과 다양한 볼거리를 함께 즐길 수 있는 도시예요.",
        "reason": "하루 일정을 체계적으로 구성하고 여러 관광지를 효율적으로 둘러보는 여행에 잘 어울려요.",
        "tags": ["도시", "계획", "관광", "효율적인 여행"]
    },

    "ESFJ": {
        "destination": "전주",
        "emoji": "🍲",
        "description": "맛있는 음식과 문화 체험을 함께 즐기기 좋은 여행지예요.",
        "reason": "사람들과 함께 맛있는 음식을 먹고 다양한 문화 체험을 즐기는 여행에 잘 어울려요.",
        "tags": ["맛집", "한옥", "문화", "친구와 여행"]
    },

    "ENFJ": {
        "destination": "경주",
        "emoji": "🌸",
        "description": "친구들과 함께 역사와 문화를 경험하기 좋은 여행지예요.",
        "reason": "혼자보다는 함께하는 여행을 즐기면서 역사와 문화에 관한 이야기도 나눌 수 있는 곳이에요.",
        "tags": ["문화", "역사", "친구", "체험"]
    },

    "ENTJ": {
        "destination": "서울",
        "emoji": "🏢",
        "description": "다양한 문화와 도시 경험을 한 번에 즐길 수 있는 여행지예요.",
        "reason": "효율적인 동선으로 여러 장소를 방문하고 새로운 문화와 공간을 빠르게 경험하는 여행과 잘 어울려요.",
        "tags": ["도시", "문화", "계획", "탐방"]
    }
}


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">✈️ MBTI 여행지 추천</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">나의 MBTI에 어울리는 여행지를 찾아보세요</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# MBTI 선택
# --------------------------------------------------

st.markdown(
    '<div class="select-title">나의 MBTI를 선택해주세요</div>',
    unsafe_allow_html=True
)

mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "MBTI",
    mbti_list,
    label_visibility="collapsed"
)


# --------------------------------------------------
# 추천 버튼
# --------------------------------------------------

if st.button("✨ 여행지 추천받기"):

    data = travel_data[selected_mbti]

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                {selected_mbti}에게 추천하는 여행지
            </div>

            <div class="destination">
                {data["emoji"]} {data["destination"]}
            </div>

            <div class="description">
                {data["description"]}
            </div>

            <div class="reason-box">
                <strong>💡 추천 이유</strong><br>
                {data["reason"]}
            </div>

            <div style="margin-top: 20px;">
                {"".join(
                    f'<span class="tag">{tag}</span>'
                    for tag in data["tags"]
                )}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    '<div class="footer">MBTI는 여행 스타일을 가볍게 알아보기 위한 참고용이에요 ✈️</div>',
    unsafe_allow_html=True
)
