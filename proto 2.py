# Streamlit 기반 장애인 일자리 매칭 시스템
import streamlit as st
import sqlite3

# DB 연결 함수
def connect_db():
    conn = sqlite3.connect("job_matching_fixed.db")
    return conn

# 구인자/구직자 입력 내역 별도 DB 연결
def connect_user_db():
    conn = sqlite3.connect("user_data.db")
    return conn

# 구인자 입력 내역 저장 함수
def save_job_posting(job_title, abilities):
    conn = connect_user_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS job_postings (id INTEGER PRIMARY KEY, title TEXT, abilities TEXT)")
    cur.execute("INSERT INTO job_postings (title, abilities) VALUES (?, ?)", (job_title, ", ".join(abilities)))
    conn.commit()
    conn.close()

# 구직자 입력 내역 저장 함수
def save_job_seeker(name, abilities):
    conn = connect_user_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS job_seekers (id INTEGER PRIMARY KEY, name TEXT, abilities TEXT)")
    cur.execute("INSERT INTO job_seekers (name, abilities) VALUES (?, ?)", (name, ", ".join(abilities)))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("장애인 일자리 매칭 시스템")

role = st.selectbox("사용자 역할 선택", ["구직자", "구인자"])

if role == "구직자":
    name = st.text_input("이름 입력")
    abilities = st.multiselect("본인의 능력 선택", ["주의력", "아이디어 발상 및 논리적 사고", "기억력", "지각능력", "수리능력", "공간능력", "언어능력", "지구력", "유연성 · 균형 및 조정", "체력", "움직임 통제능력", "정밀한 조작능력", "반응시간 및 속도", "청각 및 언어능력", "시각능력"])
    if st.button("매칭 결과 보기"):
        save_job_seeker(name, abilities)
        st.success("구직자 정보가 저장되었습니다!")
        st.write("등록한 능력:", abilities)

elif role == "구인자":
    job_title = st.text_input("일자리 제목 입력")
    abilities = st.multiselect("필요한 능력 선택", ["주의력", "아이디어 발상 및 논리적 사고", "기억력", "지각능력", "수리능력", "공간능력", "언어능력", "지구력", "유연성 · 균형 및 조정", "체력", "움직임 통제능력", "정밀한 조작능력", "반응시간 및 속도", "청각 및 언어능력", "시각능력"])
    if st.button("매칭 결과 보기"):
        save_job_posting(job_title, abilities)
        st.success("구인자 정보가 저장되었습니다!")
        st.write("등록한 능력:", abilities)

# 유료 서비스 여부 확인
if st.button("대화 종료"):
    if role == "구직자":
        use_service = st.radio("유료 취업준비 서비스 이용하시겠습니까?", ["네", "아니요"])
    else:
        use_service = st.radio("유료 직무개발 서비스 이용하시겠습니까?", ["네", "아니요"])
    if use_service == "네":
        st.write("서비스를 이용해 주셔서 감사합니다!")
    else:
        st.write("대화를 종료합니다.")
