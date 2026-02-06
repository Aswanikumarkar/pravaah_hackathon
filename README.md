#  Simple Conversation Analyzer - Easy Guide

## What This Does
Analyzes customer service conversations to find out **why bad things happen** (like escalations, refunds, angry customers).

---

##  Two Super Simple Ways to Use

### Option 1: Interactive Web Dashboard (RECOMMENDED)
**Best for:** Everyone! Easy point-and-click interface.

```bash
python interactive_analyzer.py
```

**What happens:**
1. Program loads your conversations
2. Web browser opens automatically
3. You see a beautiful dashboard
4. Click any outcome to analyze it
5. See why it happens with real examples!

**Features:**
- Search for specific outcomes
- See top 15 most common problems
- Get instant analysis with graphs
- Read real customer quotes as evidence
- No coding needed!

---

### Option 2: Command Line Version
**Best for:** Quick stats and simple analysis.

```bash
python simple_analyzer.py
```

**What you get:**
- Statistics about all conversations
- Analysis of specific outcomes
- Example evidence from real chats
- HTML dashboard file created

---

##  What You'll See

### Dashboard Shows:
1. **Total Conversations**: How many chats analyzed
2. **Different Outcomes**: Types of results (escalation, refund, etc.)
3. **Top Outcomes**: Most common problems
4. **Search Box**: Find specific issues

### When You Click an Outcome:
1. **Why It Happens** - The main reasons
   - Frustrated customers
   - Legal threats
   - Repeated problems
   - Long wait times
   
2. **Real Evidence** - Actual customer quotes
   - "This is the third time I've called!"
   - "I'm going to contact my lawyer"
   - "I've been waiting for weeks"

---

##  Dashboard Features

### What You Can Do:
- **Click** any outcome to analyze it
- **Search** for specific problems
- **See percentages** - How often things happen
- **Read examples** - Real conversation snippets
- **No programming** - Just point and click!

---

##  Example Usage

### Finding Why Customers Get Angry:

1. Run the program:
   ```bash
   python interactive_analyzer.py
   ```

2. Wait for browser to open

3. Click "Escalation - Threat of Legal Action"

4. See results like:
   ```
   Why This Happens:
   • Frustrated: 15 times (45% of cases)
   • Legal Threat: 8 times (24% of cases)
   • Repeated Issue: 12 times (36% of cases)
   
   Evidence:
   Customer: "I'm extremely frustrated!"
   Customer: "I'm contacting my lawyer"
   Customer: "Third time calling about this!"
   ```

---

##  What Gets Analyzed

### The System Looks For:

**Angry Words**
- frustrated, angry, upset, furious

**Legal Threats**
- lawyer, lawsuit, legal action, sue

**Repeated Problems**
- third time, already told you, mentioned before

**Long Waits**
- weeks, months, still waiting, long time

**Want Manager**
- supervisor, manager, escalate

---

##  Understanding Results

### Signal Cards Show:
- **Number**: How many times this happened
- **Percentage**: What % of conversations

Example:
```
Frustrated: 15
45% of cases
```
Means: In 45% of these conversations, customers said they were frustrated.

### Evidence Boxes Show:
- **Who said it**: Customer or Agent
- **What they said**: Exact quote from conversation

---

##  Tips for Best Results

1. **Start with Search**
   - Type keywords like "fraud", "escalation", "refund"
   - See matching outcomes instantly

2. **Check Top Outcomes First**
   - These are the most common problems
   - Biggest impact on your business

3. **Read the Evidence**
   - Real quotes show exactly what went wrong
   - Use for training agents

4. **Look at Percentages**
   - High % = very common problem
   - Low % = rare but important

---

##  Requirements

**You Need:**
- Python 3.6 or newer
- The conversation data file (JSON)
- A web browser

**That's It!** No special skills needed.

---

##  Troubleshooting

### Browser doesn't open?
Manually go to: `http://localhost:8000`

### Port already in use?
Someone else is using port 8000. Wait or restart your computer.

### No data showing?
Check that the JSON file is in the right location.

---

##  Files Included

1. **interactive_analyzer.py** - Main program (web dashboard)
2. **simple_analyzer.py** - Command line version
3. **dashboard.html** - Static HTML (created by simple version)

---

## What You'll Learn

### About Your Conversations:
- Most common problems
- Why customers get angry
- What triggers escalations
- How often issues repeat

### About Your Customers:
- Main frustration points
- When they threaten legal action
- Patterns in complaints
- Wait time impacts

### About Your Agents:
- (Future feature - coming soon!)

---

##  Next Steps

1. **Run the analyzer**
   ```
   python interactive_analyzer.py
   ```

2. **Explore different outcomes**
   - Click around
   - Search for patterns
   - Read customer quotes

3. **Take action**
   - Train agents on common issues
   - Fix repeated problems
   - Improve processes

---

## FAQ

**Q: Is this hard to use?**
A: No! If you can use a website, you can use this.

**Q: Do I need to code?**
A: Nope! Just run the program and click around.

**Q: How accurate is it?**
A: It finds exact keywords in conversations. Very accurate for clear signals.

**Q: Can I customize it?**
A: Yes! Edit the keywords in the Python file.

**Q: Does it work on Mac/Windows/Linux?**
A: Yes, works on all systems with Python.

