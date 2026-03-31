"""
Streamlit 기반 OCR + 대화형 인터페이스
웹캠/드래그앤드롭으로 이미지 업로드 후 VLM을 통한 실시간 텍스트 추출
"""
import streamlit as st
import numpy as np
from PIL import Image
from ocr_handler import call_ocr_api

# 페이지 설정
st.set_page_config(
    page_title="OCR Chat Bot",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS 스타일 커스터마이징
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stImage {
        text-align: center;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 세션 상태 초기화
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "image_source" not in st.session_state:
    st.session_state.image_source = None


def reset_conversation():
    """새로운 대화 시작"""
    st.session_state.conversation_history = []
    st.session_state.current_image = None
    st.session_state.image_source = None


def process_query(user_input: str):
    """사용자 입력을 처리하고 VLM을 호출합니다."""
    if not st.session_state.current_image:
        st.error("❌ 먼저 이미지를 업로드해주세요.")
        return
    
    if not user_input.strip():
        st.error("❌ 질문을 입력해주세요.")
        return
    
    # 사용자 메시지 추가
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
    })
    
    # VLM API 호출
    with st.spinner("🔄 분석 중..."):
        result = call_ocr_api(st.session_state.current_image, user_input)
    
    if result["success"]:
        # 어시스턴트 응답 추가
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": result["content"],
        })
        st.success("✅ 완료!")
    else:
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": f"[오류] {result['error']}",
        })
        st.error(f"❌ 오류: {result['error']}")


# 헤더
st.title("🔍 OCR Chat Bot")
st.markdown("**이미지에서 텍스트를 추출하고 대화로 상세한 정보를 수집하세요.**")

# 메인 레이아웃: 2열
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 이미지 입력")
    
    # 이미지 입력 방식 탭
    tab1, tab2 = st.tabs(["🎥 웹캠", "📁 파일 업로드"])
    
    with tab1:
        st.markdown("**웹캠으로 촬영하기:**")
        camera_image = st.camera_input("사진을 찍어주세요")
        if camera_image:
            image = Image.open(camera_image)
            st.session_state.current_image = image
            st.session_state.image_source = "웹캠"
            st.success("✅ 웹캠 이미지가 로드되었습니다.")
    
    with tab2:
        st.markdown("**파일을 드래그&드롭하거나 선택하세요:**")
        uploaded_file = st.file_uploader(
            "이미지 파일 선택",
            type=["jpg", "jpeg", "png", "bmp", "gif"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.session_state.current_image = image
            st.session_state.image_source = f"파일: {uploaded_file.name}"
            st.success("✅ 파일이 로드되었습니다.")
    
    # 현재 이미지 표시
    if st.session_state.current_image:
        st.markdown("---")
        st.markdown("**로드된 이미지:**")
        st.image(st.session_state.current_image, use_column_width=True)
        st.caption(f"📍 출처: {st.session_state.image_source}")
        
        if st.button("🔄 이미지 변경", use_container_width=True):
            reset_conversation()
            st.rerun()

with col2:
    st.subheader("💬 대화")
    
    if st.session_state.current_image:
        # 대화 히스토리 표시
        if st.session_state.conversation_history:
            st.markdown("**대화 기록:**")
            for message in st.session_state.conversation_history:
                if message["role"] == "user":
                    st.markdown(f"👤 **당신:** {message['content']}")
                else:
                    st.markdown(f"🤖 **AI:** {message['content']}")
                st.divider()
        else:
            st.info("💡 이미지가 로드되었습니다. 추출하고 싶은 텍스트나 정보를 입력하세요!")
        
        # 사용자 입력 영역
        st.markdown("---")
        st.markdown("**질문 입력:**")
        
        # 입력 폼
        with st.form("query_form", border=False):
            user_query = st.text_area(
                "물어보기",
                placeholder="예: '이 이미지에서 모든 텍스트를 추출해줘' 또는 '날짜는 언제야?'",
                height=80,
                label_visibility="collapsed",
            )
            col_submit, col_reset = st.columns(2)
            
            with col_submit:
                submit_button = st.form_submit_button(
                    "✉️ 전송",
                    use_container_width=True,
                    type="primary",
                )
            
            with col_reset:
                reset_button = st.form_submit_button(
                    "🗑️ 초기화",
                    use_container_width=True,
                )
            
            if submit_button:
                process_query(user_query)
                st.rerun()
            
            if reset_button:
                reset_conversation()
                st.rerun()
    
    else:
        st.warning("⚠️ 왼쪽 패널에서 이미지를 먼저 업로드해주세요.")

# 사이드바 정보
with st.sidebar:
    st.markdown("## ℹ️ 정보")
    st.markdown("""
    ### 사용 방법:
    1. **이미지 업로드**: 웹캠 또는 파일로 이미지 선택
    2. **질문 입력**: 추출하고 싶은 텍스트나 정보 입력
    3. **결과 확인**: AI가 분석한 결과 확인
    4. **추가 질문**: 대화를 통해 더 자세한 정보 요청
    
    ### 지원 기능:
    - 📸 웹캠 촬영
    - 📁 파일 드래그&드롭 업로드
    - 💬 다중턴 대화
    - 🔄 이미지 변경 기능
    
    ### 모델 정보:
    - **모델**: google/gemma-3-27b-it:free
    - **API**: OpenRouter
    """)
    
    st.markdown("---")
    st.markdown("**📊 세션 정보:**")
    st.write(f"- 이미지 로드됨: {st.session_state.current_image is not None}")
    st.write(f"- 대화 턴 수: {len(st.session_state.conversation_history)}")
