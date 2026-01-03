# Bytez Text-to-Video Gradio App

A simple Gradio interface for generating videos from text prompts using Bytez and the `ali-vilab/text-to-video-ms-1.7b` model.

## Setup

1. **Create a virtual environment** (if not already created):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install gradio bytez requests python-dotenv
   ```

3. **Set up your Bytez API key**:
   - Create a `.env` file in the project root
   - Add your Bytez API key:
     ```
     BYTEZ_KEY=your_bytez_key_here
     ```
   - **Important**: Never commit your `.env` file to version control!

## Usage

1. **Activate the virtual environment** (if not already active):
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```

3. **Open your browser** to the URL shown in the terminal (usually `http://127.0.0.1:7860`)

4. **Enter a text prompt** and click "Generate video" to create a video from your description.

## Example Prompts

- "A cat in a wizard hat walking down the street"
- "A serene sunset over the ocean"
- "A robot dancing in a futuristic city"

## Notes

- The app downloads generated videos to temporary files for preview
- Videos are generated using the Bytez API and the `ali-vilab/text-to-video-ms-1.7b` model
- Make sure you have a valid Bytez API key before running the app


## video recording link 
https://www.loom.com/share/46063ea6490f4fd0bfbe29066502c3ba