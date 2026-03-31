"""
OCR Handler - OpenRouter API를 통한 VLM 호출
이미지 분석 및 텍스트 추출 기능을 제공합니다.
"""
import base64
import requests
from io import BytesIO
from PIL import Image
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_API_URL, SYSTEM_PROMPT


def image_to_base64(image_input) -> str:
    """
    이미지를 Base64 문자열로 변환합니다.
    
    Args:
        image_input: PIL Image 또는 numpy array
        
    Returns:
        Base64 인코딩된 문자열
    """
    if isinstance(image_input, Image.Image):
        image = image_input
    else:
        # numpy array인 경우
        image = Image.fromarray(image_input)
    
    # RGB 모드로 변환 (RGBA 등 다른 형식 처리)
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # BytesIO로 변환
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    
    # Base64 인코딩
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded


def call_ocr_api(image_input, user_query: str) -> dict:
    """
    OpenRouter API를 호출하여 이미지에서 텍스트를 추출합니다.
    
    Args:
        image_input: PIL Image 또는 numpy array
        user_query: 사용자의 요청 (예: "이 이미지에서 날짜를 추출해줘")
        
    Returns:
        API 응답 딕셔너리 {
            "success": bool,
            "content": str (추출된 텍스트),
            "error": str (에러 메시지, 성공시 None)
        }
    """
    try:
        # 이미지를 Base64로 변환
        image_base64 = image_to_base64(image_input)
        
        # API 요청 구성
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        
        prompt_text = f"{SYSTEM_PROMPT}\n\n사용자 요청: {user_query}"

        # Google Gemma 계열은 provider에 따라 developer/system instruction을 거부할 수 있으므로
        # 사용자 메시지 단일 턴으로 지시문과 질의를 함께 전달합니다.
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                            },
                        },
                    ],
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1024,
        }
        
        # API 호출
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        # 응답 파싱
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"].get("content", "")
            if isinstance(content, list):
                # 일부 provider는 content를 배열로 반환합니다.
                content = "\n".join(
                    item.get("text", "") for item in content if isinstance(item, dict)
                ).strip()
            return {
                "success": True,
                "content": content,
                "error": None,
            }
        else:
            return {
                "success": False,
                "content": "",
                "error": "API 응답에서 생성된 내용을 찾을 수 없습니다.",
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "content": "",
            "error": "API 요청 시간 초과 (30초). 다시 시도해주세요.",
        }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "content": "",
            "error": f"API 오류: {e.response.status_code} - {e.response.text}",
        }
    except Exception as e:
        return {
            "success": False,
            "content": "",
            "error": f"오류 발생: {str(e)}",
        }


def clear_conversation():
    """대화 히스토리를 초기화합니다."""
    return []
