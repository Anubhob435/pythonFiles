from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats')
def stats():
    username = request.args.get('username')
    if not username:
        return render_template('index.html', error="Please enter a username")
    
    headers = {}
    # If we had a token, we'd use it here: {'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
    
    # Fetch user data
    try:
        user_resp = requests.get(f"{GITHUB_API_URL}/users/{username}", headers=headers)
        if user_resp.status_code == 404:
            return render_template('index.html', error="User not found")
        elif user_resp.status_code != 200:
            return render_template('index.html', error=f"API Error: {user_resp.status_code}")
        
        user_data = user_resp.json()
        
        # Fetch repos (limit to 100)
        repos_resp = requests.get(f"{GITHUB_API_URL}/users/{username}/repos?per_page=100", headers=headers)
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        
        # Calculate repo stats
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        languages = {}
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Fetch Contributions & Streaks
        contrib_resp = requests.get(f"https://github-contributions-api.jogruber.de/v4/{username}")
        contrib_data = contrib_resp.json() if contrib_resp.status_code == 200 else {}
        
        total_contributions = 0
        current_streak = 0
        longest_streak = 0
        
        if contrib_data:
            # Total contributions are sometimes directly available or need summing
            # The API returns 'total' usually? Let's check structure or assume 'total' keys
            # Actually, let's sum up from the calendar or use the keys if available.
            # jogruber API structure: { "total": { "2023": 123, ... }, "contributions": [ ... ] }
            # Wait, usually it returns 'total' dictionary.
            total_contributions = sum(contrib_data.get('total', {}).values())
            
            # Calculate streaks
            # Flatten contributions list: [{date: '...', count: 1, level: 1}, ...]
            import datetime
            contributions = contrib_data.get('contributions', [])
            
            # Sort by date just in case
            contributions.sort(key=lambda x: x['date'])
            
            # Longest streak
            temp_streak = 0
            for day in contributions:
                if day['count'] > 0:
                    temp_streak += 1
                else:
                    longest_streak = max(longest_streak, temp_streak)
                    temp_streak = 0
            longest_streak = max(longest_streak, temp_streak)
            
            # Current streak
            # Iterate backwards from today
            current_streak = 0
            today = datetime.date.today().isoformat()
            # We need to find today in the list
            # Or just iterate backwards
            
            # Simple backwards iteration
            for day in reversed(contributions):
                if day['date'] > today:
                    continue # specific API might return future days? usually not
                if day['count'] > 0:
                    current_streak += 1
                elif day['date'] == today and day['count'] == 0:
                    continue # if today has 0, streak might still be active from yesterday
                else:
                    break

        # Total Commits (Search API) - Note: Rate limiting is strict
        # Accept header for search commits is experimental but widely used
        search_headers = headers.copy()
        search_headers['Accept'] = 'application/vnd.github.cloak-preview'
        commits_resp = requests.get(f"{GITHUB_API_URL}/search/commits?q=author:{username}", headers=search_headers)
        total_commits = commits_resp.json().get('total_count', 0) if commits_resp.status_code == 200 else "N/A"

        return render_template('stats.html', 
                               user=user_data, 
                               stars=total_stars, 
                               forks=total_forks, 
                               languages=top_languages,
                               total_contributions=total_contributions,
                               current_streak=current_streak,
                               longest_streak=longest_streak,
                               total_commits=total_commits)
                               
    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
