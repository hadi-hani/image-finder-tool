
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# ⚠️ استبدل هذه القيم بمفاتيحك الحقيقية
UNSPLASH_API_KEY = "YOUR_UNSPLASH_API_KEY"
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"
PIXABAY_API_KEY = "YOUR_PIXABAY_API_KEY"

def fetch_unsplash_images(query="nature", limit=5):
    """استدعاء Unsplash API"""
    url = "https://api.unsplash.com/search/photos"
    params = {'query': query, 'per_page': limit}
    headers = {'Authorization': f'Client-ID {UNSPLASH_API_KEY}'}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            images = []
            for item in data.get('results', []):
                images.append({
                    'url': item['urls']['regular'],
                    'download_url': item['urls']['full'],
                    'author': item['user']['name']
                })
            return images
    except Exception as e:
        print(f"Unsplash error: {e}")
    return []

def fetch_pexels_images(query="nature", limit=5):
    """استدعاء Pexels API"""
    url = "https://api.pexels.com/v1/search"
    params = {'query': query, 'per_page': limit}
    headers = {'Authorization': PEXELS_API_KEY}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            images = []
            for item in data.get('photos', []):
                images.append({
                    'url': item['src']['large'],
                    'download_url': item['src']['original'],
                    'author': item['photographer']
                })
            return images
    except Exception as e:
        print(f"Pexels error: {e}")
    return []

def fetch_pixabay_images(query="nature", limit=5):
    """استدعاء Pixabay API"""
    url = "https://pixabay.com/api/"
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'per_page': limit,
        'image_type': 'photo'
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            images = []
            for item in data.get('hits', []):
                images.append({
                    'url': item['webformatURL'],
                    'download_url': item['largeImageURL'],
                    'author': item['user']
                })
            return images
    except Exception as e:
        print(f"Pixabay error: {e}")
    return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>أداة جمع الصور من 3 APIs</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .search-box { background: white; padding: 20px; margin-bottom: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .search-box input { width: 60%; padding: 12px; font-size: 16px; border: 1px solid #ddd; border-radius: 5px; margin-left: 10px; }
        .search-box button { padding: 12px 30px; font-size: 16px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .search-box button:hover { background: #45a049; }
        .api-section { background: white; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .api-section h2 { color: #4CAF50; margin-top: 0; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .images-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; margin-top: 15px; }
        .image-card { border: 1px solid #eee; border-radius: 8px; padding: 10px; background: #fafafa; }
        .image-card img { width: 100%; height: 200px; object-fit: cover; border-radius: 5px; }
        .image-info { margin-top: 10px; font-size: 14px; }
        .image-url { background: #f0f0f0; padding: 8px; margin: 5px 0; font-size: 11px; word-break: break-all; border-radius: 3px; font-family: monospace; }
        .image-url a { color: #4CAF50; text-decoration: none; }
        .author { color: #666; font-size: 13px; margin-bottom: 5px; }
        .no-images { color: #999; text-align: center; padding: 20px; }
        .badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .badge-unsplash { background: #000; color: #fff; }
        .badge-pexels { background: #05a081; color: #fff; }
        .badge-pixabay { background: #2ec66e; color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ أداة جمع الصور من 3 APIs</h1>
        <div class="search-box">
            <form method="GET" action="/search">
                <input type="text" name="query" placeholder="ابحث عن صور (مثال: nature, mountain, city)" value="{{ query or '' }}">
                <button type="submit">🔍 بحث</button>
            </form>
        </div>
        {% if results %}
        <div class="api-section">
            <h2><span class="badge badge-unsplash">Unsplash</span> نتائج Unsplash API</h2>
            <div class="images-grid">
                {% for image in results.unsplash %}
                <div class="image-card">
                    <img src="{{ image.url }}" alt="Unsplash image" loading="lazy">
                    <div class="image-info">
                        <div class="author">📷 {{ image.author }}</div>
                        <div class="image-url"><strong>Preview:</strong> <a href="{{ image.url }}" target="_blank">{{ image.url }}</a></div>
                        <div class="image-url"><strong>Full:</strong> <a href="{{ image.download_url }}" target="_blank">{{ image.download_url }}</a></div>
                    </div>
                </div>
                {% else %}
                <div class="no-images">❌ لا توجد نتائج من Unsplash</div>
                {% endfor %}
            </div>
        </div>
        <div class="api-section">
            <h2><span class="badge badge-pexels">Pexels</span> نتائج Pexels API</h2>
            <div class="images-grid">
                {% for image in results.pexels %}
                <div class="image-card">
                    <img src="{{ image.url }}" alt="Pexels image" loading="lazy">
                    <div class="image-info">
                        <div class="author">📷 {{ image.author }}</div>
                        <div class="image-url"><strong>Preview:</strong> <a href="{{ image.url }}" target="_blank">{{ image.url }}</a></div>
                        <div class="image-url"><strong>Full:</strong> <a href="{{ image.download_url }}" target="_blank">{{ image.download_url }}</a></div>
                    </div>
                </div>
                {% else %}
                <div class="no-images">❌ لا توجد نتائج من Pexels</div>
                {% endfor %}
            </div>
        </div>
        <div class="api-section">
            <h2><span class="badge badge-pixabay">Pixabay</span> نتائج Pixabay API</h2>
            <div class="images-grid">
                {% for image in results.pixabay %}
                <div class="image-card">
                    <img src="{{ image.url }}" alt="Pixabay image" loading="lazy">
                    <div class="image-info">
                        <div class="author">📷 {{ image.author }}</div>
                        <div class="image-url"><strong>Preview:</strong> <a href="{{ image.url }}" target="_blank">{{ image.url }}</a></div>
                        <div class="image-url"><strong>Full:</strong> <a href="{{ image.download_url }}" target="_blank">{{ image.download_url }}</a></div>
                    </div>
                </div>
                {% else %}
                <div class="no-images">❌ لا توجد نتائج من Pixabay</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, results=None, query=None)

@app.route('/search')
def search():
    query = request.args.get('query', 'nature')
    results = {
        'unsplash': fetch_unsplash_images(query),
        'pexels': fetch_pexels_images(query),
        'pixabay': fetch_pixabay_images(query)
    }
    return render_template_string(HTML_TEMPLATE, results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
