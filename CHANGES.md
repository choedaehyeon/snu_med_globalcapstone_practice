### ✅ 핫픽스 (2026-03-31)

**Issue**: pip install 실패 (Python 3.12 호환성)
```
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```

**Root Cause**: 
- numpy 1.24.3이 Python 3.12를 지원하지 않음
- setuptools가 오래된 pkgutil API 참조

**Fix**: requirements.txt 패키지 버전 업그레이드

| 패키지 | 기존 | 수정 | 비고 |
|--------|------|------|------|
| numpy | 1.24.3 | 1.26.2 | ✅ Python 3.12 호환 |
| streamlit | 1.28.1 | 1.31.1 | ✅ 최신 버전 |
| pillow | 10.0.1 | 10.1.0 | ✅ 보안 업데이트 |
| requests | 2.31.0 | 2.31.0 | (변경 없음) |
| python-dotenv | 1.0.0 | 1.0.0 | (변경 없음) |
| opencv-python | 4.8.1.78 | 4.8.1.78 | (변경 없음) |

**Result**: ✅ 모든 패키지 설치 성공

---
# 📝 OCR Chat Bot 프로젝트 - 코드 변경 추적 로그

**프로젝트**: OCR + Chat Streamlit 애플리케이션 (Google Gemma 3 27b VLM 이용)  
**생성 일시**: 2026-03-31  
**상태**: ✅ 완료 (Phase 1-4)

---

## 📊 변경사항 요약

### 총 생성 파일: 4개

| 파일명 | 상태 | 라인수 | 설명 |
|--------|------|--------|------|
| `requirements.txt` | ✅ 생성 | 6 | 환경 의존성 명시 |
| `config.py` | ✅ 생성 | 36 | API 키 및 설정 관리 |
| `ocr_handler.py` | ✅ 생성 | 142 | OpenRouter API 호출 로직 |
| `app.py` | ✅ 생성 | 277 | Streamlit UI 및 메인 앱 |
| **합계** | - | **461** | - |

---

## 📄 파일별 상세 변경사항

### 1️⃣ `requirements.txt`
**상태**: ✅ 새로 생성  
**목적**: Python 패키지 의존성 관리

**추가된 패키지:**
```
streamlit==1.28.1       # 웹 UI 프레임워크
python-dotenv==1.0.0    # 환경변수 관리
requests==2.31.0        # HTTP 요청 (API 호출)
pillow==10.0.1          # 이미지 처리
numpy==1.24.3           # 배열 연산 (이미지 처리)
opencv-python==4.8.1.78 # 웹캠 처리 (선택사항)
```

**설치 방법:**
```bash
pip install -r requirements.txt
```

---

### 2️⃣ `config.py`
**상태**: ✅ 새로 생성  
**목적**: 중앙화된 설정 관리

**주요 설정:**
- `OPENROUTER_API_KEY`: .env 파일에서 API 키 로드
- `OPENROUTER_MODEL`: "google/gemma-3-27b-it:free" 지정
- `OPENROUTER_API_URL`: https://openrouter.ai/api/v1/chat/completions
- `SYSTEM_PROMPT`: VLM용 시스템 프롬프트 정의
- 폴더 경로: `./data`, `./results`

**엔바이롱먼트 검증:**
```python
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다.")
```

---

### 3️⃣ `ocr_handler.py`
**상태**: ✅ 새로 생성  
**목적**: OpenRouter API 통신 및 VLM 호출

**주요 함수:**

| 함수명 | 입력 | 출력 | 설명 |
|--------|------|------|------|
| `image_to_base64()` | PIL Image / numpy array | str (Base64) | 이미지를 Base64로 인코딩 |
| `call_ocr_api()` | Image, 질문 | dict | VLM API 호출 및 텍스트 추출 |
| `clear_conversation()` | - | list | 대화 히스토리 초기화 |

**API 호출 흐름:**
1. 이미지 → Base64 변환
2. OpenRouter API 요청 (헤더: Bearer token)
3. Payload 구성 (모델명, 이미지, 사용자 질문)
4. 응답 파싱 및 반환

**에러 처리:**
- Timeout 오류 (30초)
- HTTP 오류 (400, 401, 429 등)
- 일반 예외 처리

---

### 4️⃣ `app.py`
**상태**: ✅ 새로 생성  
**목적**: Streamlit 기반 사용자 인터페이스

**주요 구성:**

#### A. 페이지 레이아웃
```
┌─────────────────────────────────────────┐
│          🔍 OCR Chat Bot                │
└─────────────────────────────────────────┘
┌──────────────────┬──────────────────────┐
│   📸 이미지 입력  │   💬 대화            │
│ ─────────────── │ ─────────────────── │
│ • 🎥 웹캠       │ • 대화 히스토리      │
│ • 📁 파일업로드 │ • 사용자 입력        │
│ • 이미지 미리보기 │ • 전송/초기화 버튼   │
└──────────────────┴──────────────────────┘
```

#### B. 기능
| 기능 | 구현 내용 |
|------|---------|
| **웹캠 입력** | `st.camera_input()` 사용 |
| **파일 업로드** | `st.file_uploader()` (jpg, png, bmp, gif 지원) |
| **이미지 미리보기** | `st.image()` 표시 |
| **대화 히스토리** | 사용자/AI 메시지 순차 표시 |
| **질문 입력** | 텍스트 에어리어 (`st.text_area()`) |
| **세션 상태 관리** | `st.session_state` 사용 |

#### C. 세션 상태 변수
```python
st.session_state = {
    "conversation_history": [],  # 대화 히스토리 (user/assistant)
    "current_image": None,       # 현재 로드된 이미지
    "image_source": None,        # 이미지 출처 (웹캠/파일명)
}
```

#### D. 주요 함수
- `reset_conversation()`: 새 대화 시작
- `process_query()`: 사용자 쿼리 처리 및 VLM 호출

#### E. 사이드바 정보
- 사용 방법 가이드
- 지원 기능 목록
- 모델 정보
- 세션 통계

---

## 🔄 작업 흐름

```
사용자 인터페이스 (Streamlit - app.py)
         ↓
    이미지 입력
  (웹캠/파일)
         ↓
   세션 상태 저장
 (st.session_state)
         ↓
  사용자 질문 입력
         ↓
   OCR 핸들러
 (ocr_handler.py)
         ↓
  이미지 Base64 변환
         ↓
  OpenRouter API 호출
 (config.py 설정 사용)
         ↓
  VLM 응답 받기
         ↓
   Streamlit UI에서
     결과 표시
         ↓
  대화 계속 (또는 새 이미지)
```

---

## 🚀 실행 방법

### 1단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 2단계: 환경변수 확인
```bash
# .env 파일에 API 키가 있는지 확인
cat .env
# 예상 출력: OPENROUTER_API_KEY="sk-or-v1-..."
```

### 3단계: Streamlit 앱 실행
```bash
streamlit run app.py
```

### 4단계: 웹브라우저 접속
```
http://localhost:8501
```

---

## ✅ 구현된 기능

| 기능 | 상태 | 우선순위 |
|------|------|---------|
| requirements.txt 준비 | ✅ 완료 | 🔴 필수 |
| API 설정 관리 | ✅ 완료 | 🔴 필수 |
| OpenRouter API 호출 | ✅ 완료 | 🔴 필수 |
| 기본 Streamlit UI | ✅ 완료 | 🔴 필수 |
| 웹캠 기능 | ✅ 완료 | 🟡 중요 |
| 드래그앤드롭 업로드 | ✅ 완료 | 🟡 중요 |
| 대화형 인터페이스 | ✅ 완료 | 🟡 중요 |
| 세션 상태 관리 | ✅ 완료 | 🟡 중요 |
| 에러 핸들링 | ✅ 완료 | 🟢 선택 |

---

## 📋 파일 구조 (최종)

```
/workspaces/snu_med_globalcapstone_practice/
├── requirements.txt          ✅ 생성 (6줄)
├── .env                      (기존) API 키 보유
├── config.py                 ✅ 생성 (36줄)
├── ocr_handler.py            ✅ 생성 (142줄)
├── app.py                    ✅ 생성 (277줄)
├── data/                     (폴더) 업로드된 이미지 저장
├── results/                  (폴더) 결과 저장
└── README.md, LICENSE 등 (기존 파일)
```

---

## 🔧 디버그 기록 (2026-03-31)

### 증상
- Streamlit에서 전송 버튼 클릭 후 AI 응답이 보이지 않음

### 원인
- OpenRouter 호출 시 `system` role을 사용하고 있었고,
- Google AI Studio provider가 `gemma-3-27b-it`에 developer/system instruction을 허용하지 않아 400 에러 반환
- 에러 메시지: `Developer instruction is not enabled for models/gemma-3-27b-it`

### 수정
- [ocr_handler.py](ocr_handler.py):
       - `system` 메시지 제거
       - 지시문 + 사용자 질의를 `user` 텍스트로 통합
       - 이미지 포맷을 `image_url` + data URL(base64) 형식으로 변경
       - content 파싱을 문자열/배열 모두 대응하도록 보완
- [app.py](app.py):
       - API 실패 시 에러를 대화 히스토리에도 남기도록 수정

### 검증
- `data/sample.png` + 프롬프트 `영상CD 중 어떤 영상이 필요해?`로 테스트
- 결과: `success=True`, `error=None`, OCR 응답 본문 정상 수신

---

## 🔧 커스터마이징 옵션

필요시 이 부분들을 수정할 수 있습니다:

1. **모델 변경** (`config.py`):
   ```python
   OPENROUTER_MODEL = "다른-모델명"
   ```

2. **프롬프트 커스터마이징** (`config.py`):
   ```python
   SYSTEM_PROMPT = "당신의 커스텀 프롬프트..."
   ```

3. **UI 스타일** (`app.py`):
   - CSS 커스터마이징
   - 페이지 레이아웃 변경
   - 컬러 테마 수정

4. **API 타임아웃** (`ocr_handler.py`):
   ```python
   timeout=30  # 초 단위로 수정
   ```

---

## ⚠️ 주의사항

1. **API 키**: `.env` 파일에 유효한 OpenRouter API 키가 필수
2. **인터넷 연결**: OpenRouter API 호출에 필요
3. **이미지 크기**: 너무 큰 이미지는 타임아웃 발생 가능
4. **모델 유효성**: google/gemma-3-27b-it:free 모델이 OpenRouter에서 실시간 가용이어야 함

---

## 📞 다음 단계

필요한 경우 다음 기능을 추가 개발할 수 있습니다:

- [ ] 추출된 텍스트 복사 버튼
- [ ] 이미지/대화 히스토리 파일 저장 (JSON/CSV)
- [ ] 다중 언어 지원
- [ ] 배치 이미지 처리
- [ ] 성능 최적화 (캐싱, 압축)
- [ ] 배포 (Docker, Streamlit Cloud)

---

**문서 작성일**: 2026-03-31  
**상태**: ✅ 모든 필수 기능 구현 완료  
**테스트 대기**: ⏳ 예정
