# 📺 YouTube Video Summarizer

Hey there! Thanks for checking out this project. This is a simple but powerful web app I built that takes any public YouTube video, fetches its transcript (if available), and generates a clear, human-readable summary using AI. It's perfect for when you want the gist of a long video—without watching the whole thing.

---

## 🔑 Key Features

- **Paste a YouTube link, get a summary** — one click is all it takes.
- **AI-powered summaries** using the OpenRouter API (DeepSeek model).
- **Supports multiple languages** — English, Telugu, Hindi, Tamil.
- **Clean markdown rendering** with a toggle for raw view.
- **Dark/light mode toggle** (because we love our eyes).
- **Responsive UI** with Bootstrap 5 for a better user experience.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Flask** – backend framework
- **Jinja2** – for rendering HTML templates
- **YouTube Transcript API** – pulls subtitles from videos
- **OpenRouter API** – used to generate summaries
- **Markdown** – to format summary output
- **Bootstrap 5** + **custom CSS** – styling and theming

---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/Saketh35/YouTube-Video-Summarizer.git
   cd YouTube-Video-Summarizer
   ````

2. **Set up a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate     # On macOS/Linux
   venv\Scripts\activate        # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory:

   ```env
   SECRET_KEY=your_secret_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

---

## ▶️ Running the App

```bash
python app.py
```

Then open your browser and go to `http://localhost:5000`.
Paste a YouTube URL and hit **Summarize 🎯**—that’s it!

---

## ⚠️ Known Limitations

* **Transcript must exist**
  Some videos don’t have captions or restrict access—those won’t work.

* **API rate limits**
  If you’re using a free OpenRouter key, you might hit limits after a few uses.

* **Video ID parsing**
  While most YouTube links are supported, some rare URL formats might throw errors.

---

## 🧠 Ideas for Improvement

* Add drag-and-drop file support (for uploading transcripts)
* Save summary history in session
* Deploy it live (maybe using Vercel, Heroku, or Render)
* Use OpenAI or Gemini models as alternative engines

---

## 🤝 Contribute / Collaborate

This was built as a passion project while learning Flask and APIs—so I’d *love* your thoughts, feedback, or contributions!

**👉 [Check out the repo](https://github.com/Saketh35/YouTube-Video-Summarizer)**
Feel free to fork, star ⭐, or open a pull request if you want to build on this.

---

**Made with curiosity, caffeine, and a love for clean summaries.**
– Saketh 💻
