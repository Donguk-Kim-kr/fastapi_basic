# ==================================================================
# streamlit_app.py
# - 지금까지 만든 FastAPI Todo API를 호출해서 화면으로 보여주는 프론트엔드
# - FastAPI는 계속 uvicorn으로 따로 실행 중이어야 합니다 (localhost:8000)
# - 실행: streamlit run streamlit_app.py
#
# 전체 흐름:
#   1) 로그인 안 된 상태 → 로그인/회원가입 탭만 보여줌
#   2) 로그인 성공 → JWT 토큰을 st.session_state에 저장해두고
#      이후 모든 API 요청에 "Authorization: Bearer {토큰}" 헤더로 붙여서 보냄
# ==================================================================
import streamlit as st
import requests

# --------------------------------------------------------------------
# 기본 설정
# --------------------------------------------------------------------
API_BASE = "http://127.0.0.1:8000"  # uvicorn으로 띄운 FastAPI 주소

st.set_page_config(
    page_title="나의 할 일 관리",
    page_icon="✅",
    layout="centered",
)

# 카드처럼 보이게 하는 커스텀 CSS
# (Streamlit 기본 위젯만으로는 "할 일 하나 = 카드 한 장" 느낌을 내기 어려워서
#  약간의 CSS를 얹었습니다. unsafe_allow_html=True가 있어야 HTML/CSS가 실제로 적용됩니다.)
st.markdown("""
<style>
.todo-card {
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid #e6e6e6;
}
.todo-done {
    background-color: #f0f7f0;
    text-decoration: line-through;
    color: #888;
}
.todo-pending {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------
# 세션 상태(session_state) 초기화
# --------------------------------------------------------------------
# Streamlit은 버튼을 누를 때마다 전체 스크립트가 위에서 아래로 다시 실행됩니다.
# 그래서 "로그인했다"는 사실을 변수에 담아두면 다음 클릭에서 사라집니다.
# st.session_state는 재실행돼도 값이 유지되는 유일한 저장 공간이라
# 토큰/로그인 여부를 여기에 저장해야 합니다.
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


def get_headers() -> dict:
    """로그인 후 API 요청에 매번 붙여야 하는 인증 헤더를 만들어 반환."""
    return {"Authorization": f"Bearer {st.session_state.access_token}"}


def logout():
    """세션 상태를 비워서 로그아웃 처리 (서버에 요청 보낼 필요 없음 — JWT는 Stateless)"""
    st.session_state.access_token = None
    st.session_state.user_email = None


# ======================================================================
# 로그인 안 된 상태 — 로그인 / 회원가입 화면
# ======================================================================
if not st.session_state.access_token:
    st.title("✅ 나의 할 일 관리")
    st.caption("로그인하거나 새로 가입해주세요.")

    tab_login, tab_signup = st.tabs(["🔑 로그인", "📝 회원가입"])

    # --- 로그인 탭 ----------------------------------------------------
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("이메일", key="login_email")
            password = st.text_input("비밀번호", type="password", key="login_pw")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            try:
                res = requests.post(
                    f"{API_BASE}/users/login",
                    json={"email": email, "password": password},
                )
                if res.status_code == 200:
                    st.session_state.access_token = res.json()["access_token"]
                    st.session_state.user_email = email
                    st.rerun()  # 로그인 성공 → 화면을 즉시 새로고침해서 아래 Todo 화면으로 전환
                else:
                    # FastAPI가 HTTPException으로 준 detail 메시지를 그대로 보여줌
                    st.error(res.json().get("detail", "로그인에 실패했습니다."))
            except requests.exceptions.ConnectionError:
                st.error("서버에 연결할 수 없습니다. uvicorn이 실행 중인지 확인해주세요.")

    # --- 회원가입 탭 ----------------------------------------------------
    with tab_signup:
        st.caption("비밀번호는 대문자·소문자·숫자·특수문자를 각 1개 이상 포함해야 합니다.")
        with st.form("signup_form"):
            email = st.text_input("이메일", key="signup_email")
            password = st.text_input("비밀번호", type="password", key="signup_pw")
            submitted = st.form_submit_button("가입하기", use_container_width=True)

        if submitted:
            try:
                res = requests.post(
                    f"{API_BASE}/users/signup",
                    json={"email": email, "password": password},
                )
                if res.status_code == 201:
                    st.success("가입 완료! 로그인 탭에서 로그인해주세요.")
                else:
                    # 비밀번호 규칙 위반 시 FastAPI가 422와 함께 상세 사유를 줌
                    detail = res.json().get("detail", "가입에 실패했습니다.")
                    st.error(detail)
            except requests.exceptions.ConnectionError:
                st.error("서버에 연결할 수 없습니다. uvicorn이 실행 중인지 확인해주세요.")

    st.stop()  # 로그인 전이면 아래 코드(Todo 화면)는 아예 실행하지 않고 여기서 멈춤


# ======================================================================
# 로그인 된 상태 — Todo 화면
# ======================================================================

# --- 상단 헤더 -----------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("✅ 나의 할 일")
    st.caption(f"{st.session_state.user_email}님, 환영합니다.")
with col2:
    st.write("")  # 버튼 위치를 살짝 아래로 맞추기 위한 여백
    if st.button("로그아웃", use_container_width=True):
        logout()
        st.rerun()

# --- 할 일 목록 가져오기 --------------------------------------------
res = requests.get(f"{API_BASE}/todos", headers=get_headers())

if res.status_code == 401:
    # 토큰이 만료됐거나 유효하지 않으면 자동으로 로그아웃 처리
    st.warning("로그인이 만료되었습니다. 다시 로그인해주세요.")
    logout()
    st.stop()

todos = res.json()

# --- 진행 현황 (멋지게 보여주는 부분) --------------------------------
total = len(todos)
done_count = sum(1 for t in todos if t["is_done"])

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("전체", total)
metric_col2.metric("완료", done_count)
metric_col3.metric("남은 일", total - done_count)

if total > 0:
    st.progress(done_count / total, text=f"{done_count}/{total} 완료")

st.divider()

# --- 새 할 일 추가 --------------------------------------------------
with st.form("add_todo_form", clear_on_submit=True):
    new_title = st.text_input("새로운 할 일", placeholder="할 일을 입력하세요")
    add_submitted = st.form_submit_button("➕ 추가", use_container_width=True)

if add_submitted and new_title.strip():
    requests.post(
        f"{API_BASE}/todos",
        json={"title": new_title, "is_done": False},
        headers=get_headers(),
    )
    st.rerun()  # 추가 후 목록을 다시 불러오기 위해 새로고침

st.divider()

# --- 할 일 목록 표시 (카드 형태) --------------------------------------
if total == 0:
    st.info("아직 할 일이 없습니다. 위에서 추가해보세요!")

for todo in todos:
    card_class = "todo-done" if todo["is_done"] else "todo-pending"
    check_col, title_col, delete_col = st.columns([1, 6, 1])

    with check_col:
        # 체크박스 값이 바뀌는 순간(=클릭하는 순간) PATCH 요청을 보냄
        new_state = st.checkbox(
            "", value=todo["is_done"], key=f"check_{todo['id']}"
        )
        if new_state != todo["is_done"]:
            requests.patch(
                f"{API_BASE}/todos/{todo['id']}",
                json={"is_done": new_state},
                headers=get_headers(),
            )
            st.rerun()

    with title_col:
        st.markdown(
            f'<div class="todo-card {card_class}">{todo["title"]}</div>',
            unsafe_allow_html=True,
        )

    with delete_col:
        if st.button("🗑️", key=f"delete_{todo['id']}"):
            requests.delete(f"{API_BASE}/todos/{todo['id']}", headers=get_headers())
            st.rerun()
