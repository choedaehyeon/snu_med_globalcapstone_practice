# Global Project Practice - Kildong Hong

Streamlit 기반 OCR + 대화형 VLM 실습 프로젝트입니다.  
웹캠 또는 파일 업로드로 이미지를 입력하고, OpenRouter를 통해 Cloud VLM에 질의하여 필요한 텍스트를 추출합니다.

## 1. 프로젝트 개요

- 목적: 문서/서식 이미지에서 원하는 텍스트를 질의형으로 추출
- UI: Streamlit
- 추론 API: OpenRouter Chat Completions
- 기본 모델 설정 파일: [config.py](config.py)

## 2. 주요 기능

- 웹캠 촬영 입력
- 파일 드래그 앤 드롭 업로드
- 대화형 OCR 질의/응답
- 세션 상태 기반 대화 히스토리 유지
- 업로드 403 및 호출 429 디버깅 가이드 제공

## 3. 프로젝트 구조

```text
.
├── app.py                 # Streamlit UI 엔트리포인트
├── config.py              # 모델/키/프롬프트 설정
├── ocr_handler.py         # OpenRouter 호출 로직
├── requirements.txt       # 의존성
├── .streamlit/
│   └── config.toml        # Streamlit 서버 설정(개발용)
├── data/                  # 테스트 이미지
└── results/               # 결과 저장용(확장용)
```

## 4. 사전 준비

### 4.1 Python 환경

- 권장: Python 3.11+
- 설치:

```bash
pip install -r requirements.txt
```

### 4.2 OpenRouter API 키

루트 폴더의 .env 파일에 아래 값을 설정합니다.

```env
OPENROUTER_API_KEY="your_openrouter_api_key"
```

주의: .env는 git에 커밋하지 않습니다.

## 5. 실행 방법

```bash
streamlit run app.py
```

실행 후 브라우저에서 안내되는 URL로 접속합니다.

## 6. 사용 방법

1. 좌측 입력 패널에서 웹캠 촬영 또는 파일 업로드
2. 우측 패널에 질문 입력
3. 전송 버튼으로 OCR 질의
4. 필요 시 추가 질의로 대화형 추출

예시 프롬프트:

- 영상CD 중 어떤 영상이 필요해?
- 신청서의 환자등록번호를 알려줘
- 날짜 항목만 추려서 보여줘

## 7. 모델 설정 변경

모델은 [config.py](config.py)의 OPENROUTER_MODEL에서 변경합니다.

```python
OPENROUTER_MODEL = "qwen/qwen3.5-35b-a3b"
```

원하면 다른 VLM 모델로 교체 가능합니다.

## 8. 트러블슈팅

### 8.1 업로드 시 AxiosError 403

증상:

- 파일 업로드 시 403 (AxiosError)

원인:

- Dev container/프록시 환경에서 CORS/XSRF 검증 충돌

대응:

- [.streamlit/config.toml](.streamlit/config.toml)에서 개발용 설정 적용
- 브라우저 강력 새로고침 후 재시도
- 새 탭으로 다시 접속

### 8.2 API 오류 429

증상:

- API 오류: 429 Too Many Requests

원인:

- 업스트림 모델 제공자의 일시적 rate limit

대응:

- 잠시 대기 후 재시도
- 요청 간격 늘리기
- OpenRouter BYOK 연동으로 개인 할당량 사용

### 8.3 API 오류 400

증상:

- provider별 메시지 포맷 제약으로 400 발생 가능

대응:

- [ocr_handler.py](ocr_handler.py)에서 현재 모델/provider가 허용하는 메시지 포맷 사용

## 9. 보안 및 운영 주의사항

- 개발환경에서는 업로드 안정화를 위해 XSRF/CORS를 완화했지만, 운영 배포 시에는 보안 설정을 재검토해야 합니다.
- 민감한 의료정보 이미지는 저장/전송 정책을 확인한 뒤 사용하세요.

## 10. 라이선스

저장소의 [LICENSE](LICENSE) 파일을 따릅니다.