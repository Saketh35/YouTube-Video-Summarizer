import os
import re
import requests
import markdown
from flask import Flask, render_template, request, redirect, url_for, flash
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY in environment variables.")

SYSTEM_PROMPT = """
You are an AI specialized in summarizing YouTube video captions. 
Your role is to analyze raw transcript text, typically consisting of fragmented or unpunctuated sentences, and generate a clean, coherent, human-readable summary.

Instructions:
- Expect raw, unstructured text that may be repetitive or out of sequence.
- Identify the main themes, key points, and overall message of the transcript.
- Use clear, professional, and concise language.
- Omit filler phrases, repeated lines, timestamps, or on-screen instructions unless they are critical to the meaning.
- If the transcript contains a tutorial, educational content, or list, extract steps or bullet points where appropriate.
- If the content is motivational, entertainment, or storytelling, summarize the plot or argument.
- Always assume the input is from a spoken-video transcript and optimize for that format.

Do not respond unless the user provides caption text.
Wait for the user to paste or upload YouTube captions before summarizing.
"""

def extract_video_id(url):
    # Improved and flexible regex patterns
    patterns = [
        r"youtu\.be/([^\?&]+)",
        r"v=([^\?&]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Could not extract video ID.")

def get_transcript(video_id):
    preferred_languages = ['en-US', 'en', 'te', 'hi', 'ta']  # Order of preference

    try:
        # Try all preferred languages in order
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=preferred_languages)
        return "\n".join([entry["text"] for entry in transcript])

    except (TranscriptsDisabled, NoTranscriptFound):
        raise ValueError("Transcript not available or disabled for this video.")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")

    # try:
    #     transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en-US"])
    #     return "\n".join([entry["text"] for entry in transcript])
    # except (TranscriptsDisabled, NoTranscriptFound):
    #     raise ValueError("Transcript not available for this video.")
    # except Exception as e:
    #     raise ValueError(f"Error fetching transcript: {str(e)}")

def generate_summary(transcript_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://colab.research.google.com/",  # Required by OpenRouter
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript_text}
        ],
        "temperature": 0.2
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)

    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    summary_raw = None
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if not video_url:
            flash("Please provide a YouTube URL.", "danger")
            return redirect(url_for("index"))

        try:
            video_id = extract_video_id(video_url)
            transcript = get_transcript(video_id)
            summary_raw = generate_summary(transcript)
            summary = markdown.markdown(summary_raw)
            # summary = render_markdown_safe(summary_raw)

        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("index"))

    # return render_template("index.html", summary=summary)
    return render_template("index.html", summary=summary, summary_raw=summary_raw)


if __name__ == "__main__":
    app.run(debug=True)
