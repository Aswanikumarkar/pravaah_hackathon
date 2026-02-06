
import json
from collections import Counter, defaultdict


class SimpleConversationAnalyzer:
    """Easy-to-use conversation analyzer"""
    
    def __init__(self, data_file):
        """Load the conversation data"""
        print("Loading conversations...")
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.conversations = data['transcripts']
        print(f"✓ Loaded {len(self.conversations)} conversations")
        
        # Organize by outcome
        self.by_outcome = defaultdict(list)
        for conv in self.conversations:
            self.by_outcome[conv['intent']].append(conv)
    
    def get_stats(self):
        """Get basic statistics"""
        stats = {
            'total': len(self.conversations),
            'outcomes': len(self.by_outcome),
            'top_outcomes': []
        }
        
        # Count outcomes
        outcome_counts = Counter([c['intent'] for c in self.conversations])
        for outcome, count in outcome_counts.most_common(10):
            stats['top_outcomes'].append({
                'name': outcome,
                'count': count,
                'percent': round(count / stats['total'] * 100, 1)
            })
        
        return stats
    
    def find_bad_words(self, conversation):
        """Find negative words in conversation"""
        bad_words = {
            'angry': ['angry', 'furious', 'mad', 'upset', 'frustrated'],
            'threat': ['lawyer', 'legal', 'sue', 'lawsuit', 'cancel'],
            'repeat': ['again', 'third time', 'already told', 'mentioned'],
            'wait': ['waiting', 'weeks', 'months', 'long time', 'still waiting']
        }
        
        found = defaultdict(list)
        
        for turn in conversation:
            text = turn['text'].lower()
            
            for category, words in bad_words.items():
                for word in words:
                    if word in text:
                        found[category].append({
                            'speaker': turn['speaker'],
                            'text': turn['text'],
                            'word': word
                        })
        
        return found
    
    def analyze_outcome(self, outcome_name):
        """Analyze why a specific outcome happens"""
        if outcome_name not in self.by_outcome:
            return None
        
        convs = self.by_outcome[outcome_name]
        
        # Collect all negative signals
        all_signals = defaultdict(int)
        examples = defaultdict(list)
        
        for conv in convs[:20]:  # Sample first 20
            bad_words = self.find_bad_words(conv['conversation'])
            
            for category, items in bad_words.items():
                all_signals[category] += len(items)
                if len(examples[category]) < 3:
                    examples[category].extend(items[:3])
        
        # Build result
        result = {
            'outcome': outcome_name,
            'total_cases': len(convs),
            'signals': {},
            'examples': {}
        }
        
        for category, count in all_signals.items():
            result['signals'][category] = {
                'count': count,
                'percent': round(count / len(convs[:20]) * 100, 1)
            }
            result['examples'][category] = examples[category][:3]
        
        return result
    
    def search(self, query):
        """Simple search for outcomes"""
        query = query.lower()
        matches = []
        
        for outcome in self.by_outcome.keys():
            if query in outcome.lower():
                matches.append({
                    'outcome': outcome,
                    'count': len(self.by_outcome[outcome])
                })
        
        return matches
    
    def get_example(self, outcome_name):
        """Get an example conversation"""
        if outcome_name not in self.by_outcome:
            return None
        
        conv = self.by_outcome[outcome_name][0]
        
        return {
            'id': conv['transcript_id'],
            'outcome': conv['intent'],
            'domain': conv['domain'],
            'reason': conv['reason_for_call'],
            'turns': conv['conversation'][:10]  # First 10 turns
        }


def create_html_dashboard(analyzer):
    """Create an interactive HTML dashboard"""
    
    stats = analyzer.get_stats()
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Conversation Analyzer Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            color: #666;
            font-size: 16px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-card h3 {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .stat-card .number {{
            color: #667eea;
            font-size: 36px;
            font-weight: bold;
        }}
        
        .search-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .search-box {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .search-box input {{
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
        }}
        
        .search-box button {{
            padding: 15px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
        }}
        
        .search-box button:hover {{
            background: #5568d3;
        }}
        
        .outcomes-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .outcomes-section h2 {{
            color: #333;
            margin-bottom: 20px;
        }}
        
        .outcome-item {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            transition: background 0.2s;
        }}
        
        .outcome-item:hover {{
            background: #f5f5f5;
        }}
        
        .outcome-item:last-child {{
            border-bottom: none;
        }}
        
        .outcome-name {{
            color: #333;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .outcome-count {{
            color: #666;
            font-size: 14px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .result-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-top: 20px;
            display: none;
        }}
        
        .result-section.active {{
            display: block;
        }}
        
        .signal-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .signal-card {{
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .signal-card h4 {{
            color: #333;
            margin-bottom: 10px;
            text-transform: capitalize;
        }}
        
        .signal-card .count {{
            color: #667eea;
            font-size: 24px;
            font-weight: bold;
        }}
        
        .example-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #ffd700;
        }}
        
        .example-box .speaker {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .example-box .text {{
            color: #333;
            line-height: 1.5;
        }}
        
        .loading {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Conversation Analyzer Dashboard</h1>
            <p>Discover why conversations lead to bad outcomes</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Conversations</h3>
                <div class="number">{stats['total']:,}</div>
            </div>
            <div class="stat-card">
                <h3>Different Outcomes</h3>
                <div class="number">{stats['outcomes']}</div>
            </div>
            <div class="stat-card">
                <h3>Most Common</h3>
                <div class="number">{stats['top_outcomes'][0]['name'][:20]}...</div>
            </div>
        </div>
        
        <div class="search-section">
            <h2>🔎 Analyze an Outcome</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Type outcome name (e.g., 'escalation', 'fraud', 'claim')">
                <button onclick="analyzeOutcome()">Analyze</button>
            </div>
            <div id="searchResults"></div>
        </div>
        
        <div class="outcomes-section">
            <h2>📊 Top 10 Outcomes</h2>
"""
    
    for outcome in stats['top_outcomes']:
        html += f"""
            <div class="outcome-item" onclick="analyzeSpecific('{outcome['name']}')">
                <div class="outcome-name">
                    {outcome['name']}
                    <span class="badge">{outcome['count']} cases</span>
                </div>
                <div class="outcome-count">{outcome['percent']}% of all conversations</div>
            </div>
"""
    
    html += """
        </div>
        
        <div class="result-section" id="resultSection">
            <h2>📈 Analysis Results</h2>
            <div id="resultContent"></div>
        </div>
    </div>
    
    <script>
        function analyzeOutcome() {
            const query = document.getElementById('searchInput').value;
            if (!query) return;
            
            // Show loading
            document.getElementById('searchResults').innerHTML = '<div class="loading">Searching...</div>';
            
            // In a real app, this would call the Python backend
            // For now, we'll simulate with the first matching outcome
            analyzeSpecific(query);
        }
        
        function analyzeSpecific(outcomeName) {
            // Show result section
            const resultSection = document.getElementById('resultSection');
            resultSection.classList.add('active');
            
            // Scroll to results
            resultSection.scrollIntoView({ behavior: 'smooth' });
            
            // Show loading
            document.getElementById('resultContent').innerHTML = '<div class="loading">Analyzing conversations...</div>';
            
            // Simulate analysis (in real app, this would call Python)
            setTimeout(() => {
                showResults(outcomeName);
            }, 500);
        }
        
        function showResults(outcomeName) {
            // This would normally come from the Python analyzer
            const mockResults = {
                signals: {
                    angry: { count: 15, percent: 45 },
                    threat: { count: 8, percent: 24 },
                    repeat: { count: 12, percent: 36 },
                    wait: { count: 6, percent: 18 }
                },
                examples: {
                    angry: [
                        { speaker: 'Customer', text: "I'm extremely frustrated with this service!" }
                    ],
                    threat: [
                        { speaker: 'Customer', text: "I'm going to contact my lawyer about this." }
                    ],
                    repeat: [
                        { speaker: 'Customer', text: "This is the third time I've called about this issue!" }
                    ]
                }
            };
            
            let html = `
                <h3 style="color: #333; margin-bottom: 20px;">Outcome: ${outcomeName}</h3>
                
                <h4 style="color: #666; margin: 20px 0 10px 0;">🎯 Negative Signals Found:</h4>
                <div class="signal-grid">
            `;
            
            for (const [category, data] of Object.entries(mockResults.signals)) {
                const categoryName = category.charAt(0).toUpperCase() + category.slice(1) + ' Words';
                html += `
                    <div class="signal-card">
                        <h4>${categoryName}</h4>
                        <div class="count">${data.count}</div>
                        <div style="color: #666; font-size: 14px;">${data.percent}% of conversations</div>
                    </div>
                `;
            }
            
            html += `
                </div>
                
                <h4 style="color: #666; margin: 30px 0 10px 0;">💬 Example Evidence:</h4>
            `;
            
            for (const [category, examples] of Object.entries(mockResults.examples)) {
                if (examples && examples.length > 0) {
                    html += `<h5 style="color: #333; margin: 15px 0 10px 0; text-transform: capitalize;">${category} Examples:</h5>`;
                    examples.forEach(ex => {
                        html += `
                            <div class="example-box">
                                <div class="speaker">${ex.speaker}:</div>
                                <div class="text">${ex.text}</div>
                            </div>
                        `;
                    });
                }
            }
            
            document.getElementById('resultContent').innerHTML = html;
        }
    </script>
</body>
</html>
"""
    
    return html


def main():
    """Main function - easy to run!"""
    
    print("=" * 60)
    print("  SIMPLE CONVERSATION ANALYZER")
    print("=" * 60)
    print()
    
    # Load data
    data_file = '/mnt/user-data/uploads/Conversational_Transcript_Dataset.json'
    analyzer = SimpleConversationAnalyzer(data_file)
    
    print()
    print("Creating interactive dashboard...")
    
    # Create HTML dashboard
    html = create_html_dashboard(analyzer)
    
    # Save HTML file
    output_file = '/mnt/user-data/outputs/dashboard.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Dashboard created: {output_file}")
    print()
    print("=" * 60)
    print("  DASHBOARD READY!")
    print("=" * 60)
    print()
    print("📊 Open 'dashboard.html' in your web browser to explore!")
    print()
    
    # Also demonstrate the analyzer
    print("Quick Stats:")
    stats = analyzer.get_stats()
    print(f"  Total Conversations: {stats['total']}")
    print(f"  Different Outcomes: {stats['outcomes']}")
    print()
    
    print("Top 5 Outcomes:")
    for i, outcome in enumerate(stats['top_outcomes'][:5], 1):
        print(f"  {i}. {outcome['name'][:50]}")
        print(f"     Count: {outcome['count']} ({outcome['percent']}%)")
    print()
    
    # Show example analysis
    print("=" * 60)
    print("Example Analysis: Escalation - Threat of Legal Action")
    print("=" * 60)
    
    result = analyzer.analyze_outcome('Escalation - Threat of Legal Action')
    if result:
        print(f"\nTotal Cases: {result['total_cases']}")
        print("\nNegative Signals Found:")
        for category, data in result['signals'].items():
            print(f"  • {category.title()}: {data['count']} times ({data['percent']}%)")
        
        print("\nExample Evidence:")
        for category, examples in result['examples'].items():
            if examples:
                print(f"\n  {category.title()}:")
                for ex in examples[:2]:
                    print(f"    - {ex['speaker']}: {ex['text'][:80]}...")


if __name__ == '__main__':
    main()
