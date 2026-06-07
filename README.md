# 🖼️ Image Finder Tool

A simple Flask web app that searches and previews images from **3 different APIs**:

- 📸 [Unsplash API](https://unsplash.com/developers)
- 📷 [Pexels API](https://www.pexels.com/api/)
- 🎨 [Pixabay API](https://pixabay.com/api/docs/)

## Features

- Search images by keyword
- Preview images directly in the browser
- View full image URLs from each platform separately
- Arabic RTL interface
- Responsive grid layout

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/hadi-hani/image-finder-tool.git
cd image-finder-tool
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your API keys

Copy the example file and fill in your API keys:

```bash
cp .env.example .env
```

Then open `.env` and set your keys:

```env
UNSPLASH_API_KEY=your_unsplash_access_key
PEXELS_API_KEY=your_pexels_api_key
PIXABAY_API_KEY=your_pixabay_api_key
```

### 4. Run the app

```bash
python3 app.py
```

Open your browser at: **http://localhost:5000**

## Getting API Keys

| Platform | Registration Link | Free Tier |
|----------|------------------|-----------|
| Unsplash | https://unsplash.com/developers | 50 req/hour |
| Pexels | https://www.pexels.com/api/ | 200 req/hour |
| Pixabay | https://pixabay.com/api/docs/ | 100 req/min |

## Project Structure

```
image-finder-tool/
├── app.py            # Main Flask application
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
└── README.md         # This file
```
