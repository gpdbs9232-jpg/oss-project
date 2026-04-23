import streamlit as st
import pandas as pd

# ---------------------------------------------------
# 기본 설정
# ---------------------------------------------------
st.set_page_config(
    page_title="Tottenham Hotspur App",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------------------------------
# 로그인 계정
# ---------------------------------------------------
USERS = {
    "ilovekwu": "1234",
    "student": "kw2024"
}

# ---------------------------------------------------
# 세션 상태
# ---------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "progress" not in st.session_state:
    st.session_state.progress = 0

# ---------------------------------------------------
# 로그인 함수
# ---------------------------------------------------
def login(user_id, password):
    if user_id in USERS and USERS[user_id] == password:
        st.session_state.logged_in = True
        st.session_state.username = user_id
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# ---------------------------------------------------
# 로그인 화면
# ---------------------------------------------------
def show_login():
    st.title("🔐 로그인")
    st.subheader("2023204061 권혁준")

    user_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    st.info("예시 계정: ilovekwu / 1234")

    if st.button("로그인"):
        if login(user_id, password):
            st.success("로그인 성공")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호 오류")

# ---------------------------------------------------
# 캐싱 함수
# ---------------------------------------------------
@st.cache_data
def load_player_data():
    df = pd.read_csv("players.csv")
    return df

@st.cache_data
def load_quiz_data():
    return [
        {"image": "images/son.jpg", "answer": "손흥민"},
        {"image": "images/mds.jpg", "answer": "제임스 매디슨"},
        {"image": "images/poro.jpg", "answer": "페드로 포로"}
    ]

# ---------------------------------------------------
# 메인 앱
# ---------------------------------------------------
def show_main():
    st.title("2023204061 권혁준 중간고사 대체 실습과제")
    st.subheader("⚽ Tottenham Hotspur 소개 및 퀴즈")

    st.sidebar.success(f"{st.session_state.username} 로그인됨")

    if st.sidebar.button("로그아웃"):
        logout()
        st.rerun()

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["소개", "캐싱 기능", "선수 퀴즈"]
    )

    st.write("---")

    # ---------------- 소개 ----------------
    if menu == "소개":
        st.header("1. Tottenham Hotspur 소개")

        st.image("images/tot.jpg", width=400)

        st.write("""
        - 1882년에 창단된 축구 클럽이다.
        - 영국 런던에 위치한 팀이다.
        - 라이벌은 Arsenal이며 북런던 더비로 유명하다.
        - 현재 프리미어리그 순위(33R 기준): 18위 
        """)

    # ---------------- 캐싱 ----------------
    elif menu == "캐싱 기능":
        st.header("2. 캐싱 기능 (CSV 데이터 활용)")

        st.write("""
        이 페이지는 CSV 파일에서 선수 데이터를 불러오고,
        Streamlit의 캐싱 기능을 통해 데이터를 재사용합니다.
        """)

        if st.button("캐시 새로고침"):
            st.cache_data.clear()
            st.rerun()

        df = load_player_data()

        selected = st.selectbox("선수 선택", df["name"])

        player = df[df["name"] == selected].iloc[0]

        col1, col2 = st.columns(2)  

        with col1:
            st.write(f"이름: {player['name']}")
            st.write(f"포지션: {player['position']}")
            st.write(f"등번호: {player['number']}")

        with col2:
            st.image(player["image"], width=250)

        # ---------------- 퀴즈 ----------------
    elif menu == "선수 퀴즈":
        st.header("3. 선수 이름 맞히기")

        quiz = load_quiz_data()
        total = len(quiz)

        # 게이지 표시
        st.progress(st.session_state.progress / total)

        if st.session_state.current_question < total:
            q = quiz[st.session_state.current_question]

            st.image(q["image"], width=300)

            answer = st.text_input(
                "이 선수 이름은?",
                key=f"quiz_answer_{st.session_state.current_question}"
)

            if st.button("제출"):
                user = answer.strip().replace(" ", "")
                real = q["answer"].strip().replace(" ", "")

                if user == real:
                    st.success("정답!")

                    st.session_state.score += 1
                    st.session_state.current_question += 1
                    st.session_state.progress += 1

                    st.rerun()
                else:
                    st.error("틀렸습니다! 다시 입력하세요 ❌")

        else:
            st.success("퀴즈 종료 🎉 당신은 토트넘 핫스퍼의 팬이 되었습니다!")
            st.write(f"점수: {st.session_state.score} / {total}")
            st.progress(1.0)

            if st.button("다시 시작"):
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.progress = 0
                st.rerun()

# ---------------------------------------------------
# 실행
# ---------------------------------------------------
if st.session_state.logged_in:
    show_main()
else:
    show_login()