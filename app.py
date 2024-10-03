from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle fetching m3u8 link
@app.route('/get-m3u8', methods=['GET'])
def get_m3u8():
    video_page_url = request.args.get('url')

    if not video_page_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Fetch the video page content
        response = requests.get(video_page_url)
        response.raise_for_status()
        
        # Extract m3u8 link from the page content
        m3u8_link = extract_m3u8(response.text)
        
        if m3u8_link:
            return jsonify({'m3u8_url': m3u8_link})
        else:
            return jsonify({'error': 'm3u8 link not found'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Function to extract m3u8 URL from page content
def extract_m3u8(page_content):
    import re
    # Regex to find m3u8 URLs in the page content
    m3u8_regex = re.compile(r'https?://[^\s]+\.m3u8')
    match = m3u8_regex.search(page_content)
    if match:
        return match.group(0)
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
