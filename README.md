# 🎥 Universal Video Downloader
A powerful universal video and audio downloader built with Python. This tool allows fetching media from virtually any URL, offering options for high-quality video downloads or audio-only extraction.

# 🎮 Live Playground
Link: https://video-downloader-ws.streamlit.app/

## 🚀 Features

-   **Universal Support:** Leverages industry-standard engines to support hundreds of platforms (YouTube, Vimeo, Twitter, etc.).
-   **Format Flexibility:** Download full videos or extract audio.
-   **Clean Architecture:** Separated `backend` logic and `frontend` interface for better maintainability.

---

## 🛠️ Tech Stack

-   **Language:** Python 3.10+
-   **Core Engine:** `yt-dlp`
-   **Backend:** Python-based processing logic (Fastapi).
-   **Frontend:** Python-driven UI (Streamlit).

---

## 📂 Project Structure

```text
Video-Downloader/
├── .devcontainer/ 
├── backend/            # Core download logic and API handling
│   └── ...             # Logic for yt-dlp integration
├── frontend/           # User interface components
│   └── ...             # UI implementation (Streamlit)
├── LICENSE             # MIT License
└── README.md           # Project documentation
```

---

## ⚙️ Installation

### Prerequisites
-   **Python 3.10 or higher**
-   **FFmpeg:** Required for merging video/audio streams and format conversion.
    -   *Ubuntu:* `sudo apt install ffmpeg`
    -   *macOS:* `brew install ffmpeg`
    -   *Windows:* Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SedeWahlid/Video-Downloader.git
    cd Video-Downloader
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Activate on Windows:
    .\venv\Scripts\activate
    # Activate on macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    ```

---

## 🖥️ Usage

To launch the application, run the frontend.py and the backend.py:

```bash
streamlit run frontend/frontend.py

fastapi run backend/backend.py
```

1.  **Paste the URL** of the video you wish to download.
2.  **Select the format** (Video or Audio or both).
3.  **Click Download** and wait for the process to complete.
4.  **Clicke Save** and that is it.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---