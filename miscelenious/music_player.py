from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads/music'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'm4a', 'flac'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Playlist storage (in production, use a database)
PLAYLIST_FILE = 'playlist.json'


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_playlist():
    """Load playlist from JSON file"""
    if os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, 'r') as f:
            return json.load(f)
    return []


def save_playlist(playlist):
    """Save playlist to JSON file"""
    with open(PLAYLIST_FILE, 'w') as f:
        json.dump(playlist, f, indent=2)


@app.route('/')
def index():
    """Main page with music player"""
    playlist = load_playlist()
    return render_template('index.html', playlist=playlist)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Ensure unique filename
        base_name = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[1]
        counter = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = f"{base_name}_{counter}.{extension}"
            counter += 1
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Add to playlist
        playlist = load_playlist()
        song_info = {
            'id': len(playlist) + 1,
            'filename': filename,
            'title': base_name.replace('_', ' ').title(),
            'path': filepath
        }
        playlist.append(song_info)
        save_playlist(playlist)
        
        return jsonify({'success': True, 'song': song_info})
    
    return jsonify({'error': 'File type not allowed'}), 400


@app.route('/stream/<int:song_id>')
def stream_music(song_id):
    """Stream music file"""
    playlist = load_playlist()
    
    for song in playlist:
        if song['id'] == song_id:
            filepath = song['path']
            if os.path.exists(filepath):
                return send_file(filepath, mimetype='audio/mpeg')
    
    return jsonify({'error': 'Song not found'}), 404


@app.route('/delete/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    """Delete a song from playlist"""
    playlist = load_playlist()
    
    for i, song in enumerate(playlist):
        if song['id'] == song_id:
            # Delete file
            if os.path.exists(song['path']):
                os.remove(song['path'])
            
            # Remove from playlist
            playlist.pop(i)
            save_playlist(playlist)
            
            return jsonify({'success': True})
    
    return jsonify({'error': 'Song not found'}), 404


@app.route('/playlist')
def get_playlist():
    """Get current playlist as JSON"""
    playlist = load_playlist()
    return jsonify(playlist)


if __name__ == '__main__':
    print("🎵 Music Streaming App Starting...")
    print("📂 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("🌐 Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
