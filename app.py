import os
import tempfile
import time
from urllib.parse import urlparse

import gradio as gr
import requests
from dotenv import load_dotenv
from bytez import Bytez

load_dotenv()

BYTEZ_KEY = os.getenv("BYTEZ_KEY")
MODEL_ID = "ali-vilab/text-to-video-ms-1.7b"

if not BYTEZ_KEY:
    raise RuntimeError("Missing BYTEZ_KEY. Put it in your environment or a .env file.")

client = Bytez(BYTEZ_KEY)
model = client.model(MODEL_ID)


def _download_video(url: str) -> str:
    """
    Downloads the video URL to a temporary .mp4 file and returns the filepath.
    """
    # best-effort extension
    path = urlparse(url).path
    ext = os.path.splitext(path)[1] or ".mp4"
    if ext.lower() not in [".mp4", ".webm", ".mov", ".mkv", ".gif"]:
        ext = ".mp4"

    tmp_dir = tempfile.mkdtemp(prefix="bytez_vid_")
    out_path = os.path.join(tmp_dir, f"generated_{int(time.time())}{ext}")

    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return out_path


def generate_video(prompt: str):
    prompt = (prompt or "").strip()
    if not prompt:
        return None, "Please enter a prompt."

    try:
        # Bytez Python SDK pattern: result = model.run(input)
        # For text-to-video, input is the text prompt.
        result = model.run(prompt)

        # result.error is None on success (per SDK examples)
        if getattr(result, "error", None):
            return None, f"Bytez error: {result.error}"

        video_url = getattr(result, "output", None)
        if not video_url:
            return None, "No output returned from Bytez."

        # Bytez HTTP example shows output is a video link (URL) :contentReference[oaicite:2]{index=2}
        local_path = _download_video(video_url)
        return local_path, f"✅ Done. Source URL: {video_url}"

    except Exception as e:
        return None, f"Failed: {e}"


with gr.Blocks(title="Bytez Text-to-Video") as demo:
    gr.Markdown(
        """
# Bytez Text → Video (Gradio)
Model: `ali-vilab/text-to-video-ms-1.7b`

Enter a prompt, generate a short video, and preview it below.
"""
    )

    prompt = gr.Textbox(
        label="Prompt",
        placeholder="A cat in a wizard hat walking down the street",
        lines=3,
    )

    btn = gr.Button("Generate video")
    video = gr.Video(label="Generated video", autoplay=True)
    status = gr.Textbox(label="Status", interactive=False)

    btn.click(fn=generate_video, inputs=[prompt], outputs=[video, status], concurrency_limit=2)

if __name__ == "__main__":
    demo.launch()

