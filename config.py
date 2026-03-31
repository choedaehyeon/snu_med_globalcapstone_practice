"""
Configuration 파일
환경변수 및 API 설정을 관리합니다.
"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenRouter API 설정
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "qwen/qwen3.5-35b-a3b"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Streamlit 설정
STREAMLIT_THEME = "light"
UPLOAD_FOLDER = "./data"
RESULTS_FOLDER = "./results"

# VLM 프롬프트 템플릿
SYSTEM_PROMPT = """당신은 이미지에서 사용자가 요청한 텍스트를 정확하게 추출하는 OCR 전문가입니다.
사용자가 특정 텍스트나 정보를 요청하면, 이미지를 분석하여 정확한 텍스트를 추출해주세요.
추출된 텍스트는 명확하고 읽기 쉬운 형식으로 제공해주세요."""

# 검증
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY 환경변수가 설정되지 않았습니다.")
