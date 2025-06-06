import requests

def generate_image_caption(img_path, api_key):
    return "이미지 설명 기능은 구현되지 않았습니다."

def speech_to_text(audio_path, api_key):
    return "음성 인식 기능은 구현되지 않았습니다."

def query_groq_llm(prompt, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    try:
        res = requests.post(url, headers=headers, json=payload)

        print("🔍 응답 상태 코드:", res.status_code)
        print("🔍 응답 본문 (text):", res.text)

        # 응답이 JSON이 아닐 수도 있어서 먼저 체크
        try:
            response_json = res.json()
            print("🔍 응답 JSON 전체:", response_json)
        except Exception as parse_error:
            print("❌ JSON 파싱 실패:", parse_error)
            return "[오류] 응답을 JSON으로 변환할 수 없습니다."

        # 정상 응답이면 내용 추출 시도
        if res.status_code == 200:
            choice = response_json.get("choices", [{}])[0]
            message = choice.get("message", {})
            if "content" in message:
                return message["content"]
            elif "text" in choice:
                return choice["text"]
            else:
                return "[오류] 응답에 text나 content가 없음"
        else:
            return f"[오류] 상태 코드 {res.status_code} - {response_json}"

    except Exception as e:
        print("❌ 요청 실패:", e)


def multimodal_chat(user_text, user_image_path, user_audio_path, api_key):
    context = []

    if user_image_path:
        caption = generate_image_caption(user_image_path, api_key)
        context.append(f"이미지 설명: {caption}")

    if user_audio_path:
        spoken_text = speech_to_text(user_audio_path, api_key)
        context.append(f"음성 내용: {spoken_text}")

    if user_text.strip():
        context.append(f"사용자 입력: {user_text}")