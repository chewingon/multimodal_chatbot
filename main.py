import gradio as gr
import os
from dotenv import load_dotenv
from modules.groq_inference import multimodal_chat

# 🔐 .env 파일에서 API 키 불러오기
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("🧪 불러온 API 키:", GROQ_API_KEY)

# 🧠 사용자 입력을 받아 multimodal_chat 함수 호출
def gradio_multimodal_interface(text_input, image_input, audio_input):
    print("🧪 버튼 클릭됨!")
    if not text_input and not image_input and not audio_input:
        return "입력된 내용이 없습니다. 텍스트를 입력하거나 이미지/음성을 업로드해주세요."
    response = multimodal_chat(text_input, image_input, audio_input, GROQ_API_KEY)
    print("🧪 LLM 응답:", response)
    return response


# 🎛️ Gradio 인터페이스 구성
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 멀티모달 챗봇 (Groq + Gradio)")

    text_box = gr.Textbox(label="텍스트 입력", lines=2, placeholder="무엇이든 물어보세요!")
    image_uploader = gr.Image(type="filepath", label="이미지 업로드 (선택)")
    audio_recorder = gr.Audio(type="filepath", label="음성 업로드 (선택)")
    chat_button = gr.Button("보내기")
    output_box = gr.Textbox(label="챗봇 응답", lines=4)

    chat_button.click(
        fn=gradio_multimodal_interface,
        inputs=[text_box, image_uploader, audio_recorder],
        outputs=output_box
    )

# 🚀 실행
if __name__ == "__main__":
    demo.launch()