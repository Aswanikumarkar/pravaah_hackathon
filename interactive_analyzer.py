
import json
from collections import Counter, defaultdict
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import webbrowser


class ConversationAnalyzer:
    """Simple analyzer with all the smarts"""
    
    def __init__(self, data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.conversations = data['transcripts']
        self.by_outcome = defaultdict(list)
        
        for conv in self.conversations:
            self.by_outcome[conv['intent']].append(conv)
    
    def get_all_outcomes(self):
        """Get list of all outcomes"""
        outcome_counts = Counter([c['intent'] for c in self.conversations])
        return [
            {
                'name': outcome,
                'count': count,
                'percent': round(count / len(self.conversations) * 100, 1)
            }
            for outcome, count in outcome_counts.most_common(15)
        ]
    
    def analyze(self, outcome_name):
        """Analyze a specific outcome"""
        convs = self.by_outcome.get(outcome_name, [])
        if not convs:
            return None
        
        # Keywords to look for
        keywords = {
            'Frustrated': ['frustrated', 'angry', 'upset', 'mad', 'furious'],
            'Legal Threat': ['lawyer', 'legal', 'sue', 'lawsuit', 'attorney'],
            'Repeated Issue': ['again', 'third time', 'already told', 'mentioned before'],
            'Long Wait': ['weeks', 'months', 'waiting', 'long time', 'still waiting'],
            'Want Supervisor': ['manager', 'supervisor', 'escalate', 'higher up']
        }
        
        signals = defaultdict(int)
        examples = defaultdict(list)
        
        for conv in convs[:30]:  # Analyze first 30
            for turn in conv['conversation']:
                text = turn['text'].lower()
                
                for category, words in keywords.items():
                    for word in words:
                        if word in text:
                            signals[category] += 1
                            if len(examples[category]) < 3:
                                examples[category].append({
                                    'speaker': turn['speaker'],
                                    'text': turn['text']
                                })
                            break
        
        return {
            'outcome': outcome_name,
            'total_cases': len(convs),
            'signals': {
                cat: {
                    'count': count,
                    'percent': round(count / min(30, len(convs)) * 100, 1)
                }
                for cat, count in signals.items()
            },
            'examples': {
                cat: exs[:3] for cat, exs in examples.items()
            }
        }
    
    def search_outcomes(self, query):
        """Search for outcomes matching query"""
        query = query.lower()
        matches = []
        
        for outcome, convs in self.by_outcome.items():
            if query in outcome.lower():
                matches.append({
                    'name': outcome,
                    'count': len(convs)
                })
        
        return sorted(matches, key=lambda x: -x['count'])[:10]


# Global analyzer instance
ANALYZER = None


class DashboardHandler(BaseHTTPRequestHandler):
    """Handle web requests"""
    
    def log_message(self, format, *args):
        """Suppress request logging"""
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        
        if parsed.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_html_dashboard().encode())
        
        elif parsed.path == '/api/outcomes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            outcomes = ANALYZER.get_all_outcomes()
            self.wfile.write(json.dumps(outcomes).encode())
        
        elif parsed.path == '/api/analyze':
            params = parse_qs(parsed.query)
            outcome = params.get('outcome', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            result = ANALYZER.analyze(outcome)
            self.wfile.write(json.dumps(result).encode())
        
        elif parsed.path == '/api/search':
            params = parse_qs(parsed.query)
            query = params.get('q', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            results = ANALYZER.search_outcomes(query)
            self.wfile.write(json.dumps(results).encode())


def get_html_dashboard():
    """Generate the HTML dashboard"""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Conversation Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #333;
            font-size: 42px;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 18px;
        }
        
        .search-card {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .search-card h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 24px;
        }
        
        .search-box {
            display: flex;
            gap: 15px;
        }
        
        .search-box input {
            flex: 1;
            padding: 18px 25px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            transition: border 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .search-box button {
            padding: 18px 40px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .search-box button:hover {
            background: #5568d3;
        }
        
        #searchResults {
            margin-top: 20px;
        }
        
        .search-result {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .search-result:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
        }
        
        .outcomes-list {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-height: 800px;
            overflow-y: auto;
        }
        
        .outcomes-list h2 {
            color: #333;
            margin-bottom: 20px;
            position: sticky;
            top: 0;
            background: white;
            padding-bottom: 10px;
        }
        
        .outcome-item {
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .outcome-item:hover {
            background: #f8f9fa;
            transform: translateX(5px);
        }
        
        .outcome-name {
            color: #333;
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .outcome-stats {
            color: #666;
            font-size: 14px;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 12px;
            margin-left: 8px;
        }
        
        .results-panel {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-height: 800px;
        }
        
        .empty-state {
            text-align: center;
            padding: 100px 40px;
            color: #999;
        }
        
        .empty-state h3 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .loading {
            text-align: center;
            padding: 100px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result-header {
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .result-header h2 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .result-stat {
            color: #666;
            font-size: 16px;
        }
        
        .signals-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .signal-card {
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .signal-card h4 {
            font-size: 14px;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        
        .signal-card .number {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .signal-card .percent {
            font-size: 14px;
            opacity: 0.8;
        }
        
        .examples-section {
            margin-top: 40px;
        }
        
        .examples-section h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 22px;
        }
        
        .category-examples {
            margin-bottom: 30px;
        }
        
        .category-examples h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .example-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin: 12px 0;
            border-left: 5px solid #ffd700;
        }
        
        .example-speaker {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .example-text {
            color: #333;
            line-height: 1.6;
            font-size: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Conversation Analyzer</h1>
            <p>Discover why conversations lead to bad outcomes</p>
        </div>
        
        <div class="search-card">
            <h2>🔎 Search & Analyze</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search for an outcome (e.g., 'escalation', 'fraud', 'refund')">
                <button onclick="search()">Search</button>
            </div>
            <div id="searchResults"></div>
        </div>
        
        <div class="grid">
            <div class="outcomes-list">
                <h2>📊 Top Outcomes</h2>
                <div id="outcomesList">
                    <div class="loading">
                        <div class="spinner"></div>
                    </div>
                </div>
            </div>
            
            <div class="results-panel" id="resultsPanel">
                <div class="empty-state">
                    <h3>👈 Select an outcome to analyze</h3>
                    <p>Click on any outcome from the list to see why it happens</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Load outcomes on page load
        window.onload = function() {
            loadOutcomes();
        };
        
        function loadOutcomes() {
            fetch('/api/outcomes')
                .then(r => r.json())
                .then(outcomes => {
                    let html = '';
                    outcomes.forEach(outcome => {
                        html += `
                            <div class="outcome-item" onclick="analyzeOutcome('${outcome.name.replace(/'/g, "\\'")}')">
                                <div class="outcome-name">${outcome.name}</div>
                                <div class="outcome-stats">
                                    <span class="badge">${outcome.count} cases</span>
                                    <span style="margin-left: 10px;">${outcome.percent}% of all</span>
                                </div>
                            </div>
                        `;
                    });
                    document.getElementById('outcomesList').innerHTML = html;
                });
        }
        
        function search() {
            const query = document.getElementById('searchInput').value;
            if (!query) return;
            
            fetch('/api/search?q=' + encodeURIComponent(query))
                .then(r => r.json())
                .then(results => {
                    let html = '';
                    if (results.length === 0) {
                        html = '<div style="padding: 20px; text-align: center; color: #666;">No matching outcomes found</div>';
                    } else {
                        results.forEach(result => {
                            html += `
                                <div class="search-result" onclick="analyzeOutcome('${result.name.replace(/'/g, "\\'")}')">
                                    <strong>${result.name}</strong> (${result.count} cases)
                                </div>
                            `;
                        });
                    }
                    document.getElementById('searchResults').innerHTML = html;
                });
        }
        
        function analyzeOutcome(outcomeName) {
            // Show loading
            document.getElementById('resultsPanel').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <p style="margin-top: 20px; color: #666;">Analyzing conversations...</p>
                </div>
            `;
            
            // Fetch analysis
            fetch('/api/analyze?outcome=' + encodeURIComponent(outcomeName))
                .then(r => r.json())
                .then(result => {
                    if (!result) {
                        document.getElementById('resultsPanel').innerHTML = '<div class="empty-state"><h3>No data found</h3></div>';
                        return;
                    }
                    
                    let html = `
                        <div class="result-header">
                            <h2>${result.outcome}</h2>
                            <div class="result-stat">Total Cases: <strong>${result.total_cases}</strong></div>
                        </div>
                    `;
                    
                    // Signals
                    if (Object.keys(result.signals).length > 0) {
                        html += '<h3 style="color: #333; margin-bottom: 20px;">🎯 Why This Happens</h3>';
                        html += '<div class="signals-grid">';
                        
                        for (const [category, data] of Object.entries(result.signals)) {
                            html += `
                                <div class="signal-card">
                                    <h4>${category}</h4>
                                    <div class="number">${data.count}</div>
                                    <div class="percent">${data.percent}% of cases</div>
                                </div>
                            `;
                        }
                        html += '</div>';
                    }
                    
                    // Examples
                    if (Object.keys(result.examples).length > 0) {
                        html += '<div class="examples-section">';
                        html += '<h3>💬 Evidence from Real Conversations</h3>';
                        
                        for (const [category, examples] of Object.entries(result.examples)) {
                            if (examples && examples.length > 0) {
                                html += `<div class="category-examples">`;
                                html += `<h4>${category}</h4>`;
                                
                                examples.forEach(ex => {
                                    html += `
                                        <div class="example-box">
                                            <div class="example-speaker">${ex.speaker}</div>
                                            <div class="example-text">${ex.text}</div>
                                        </div>
                                    `;
                                });
                                
                                html += '</div>';
                            }
                        }
                        html += '</div>';
                    }
                    
                    document.getElementById('resultsPanel').innerHTML = html;
                });
        }
        
        // Allow Enter key to search
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    search();
                }
            });
        });
    </script>
</body>
</html>
"""


def start_server(port=8000):
    """Start the web server"""
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"🌐 Server running at http://localhost:{port}")
    print(f"📊 Dashboard will open in your browser...")
    print(f"⚠️  Press Ctrl+C to stop the server")
    print()
    
    # Open browser
    threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")


def main():
    """Run the analyzer"""
    global ANALYZER
    
    print()
    print("=" * 60)
    print("  🔍 INTERACTIVE CONVERSATION ANALYZER")
    print("=" * 60)
    print()
    
    # Load data
    print("Loading conversation data...")
    data_file = '/mnt/user-data/uploads/Conversational_Transcript_Dataset.json'
    ANALYZER = ConversationAnalyzer(data_file)
    print(f"✓ Loaded {len(ANALYZER.conversations)} conversations")
    print()
    
    # Start server
    start_server(port=8000)


if __name__ == '__main__':
    main()
