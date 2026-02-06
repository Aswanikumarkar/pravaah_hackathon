
import os
import sys


def print_banner():
    """Show welcome message"""
    print()
    print("=" * 70)
    print("   CONVERSATION ANALYZER - QUICK START")
    print("=" * 70)
    print()
    print("  Discover why conversations lead to bad outcomes!")
    print("  Easy to use • Beautiful dashboard • Instant insights")
    print()
    print("=" * 70)
    print()


def check_requirements():
    """Make sure everything is ready"""
    print("Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print(" Python 3.6 or higher required")
        print(f"   You have: Python {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print("✓ Python version OK")
    
    # Check if data file exists
    data_file = '/mnt/user-data/uploads/Conversational_Transcript_Dataset.json'
    if not os.path.exists(data_file):
        print(f" Data file not found: {data_file}")
        return False
    print("✓ Data file found")
    
    print()
    return True


def show_menu():
    """Show user options"""
    print("=" * 70)
    print("  CHOOSE HOW YOU WANT TO ANALYZE")
    print("=" * 70)
    print()
    print("  1.  Interactive Web Dashboard (RECOMMENDED)")
    print("     → Beautiful web interface")
    print("     → Point and click")
    print("     → Opens in your browser")
    print()
    print("  2.  Simple Command Line")
    print("     → Quick stats and analysis")
    print("     → See results in terminal")
    print("     → Creates HTML file")
    print()
    print("  3.  Show me what this does")
    print()
    print("  4. Exit")
    print()
    print("=" * 70)
    print()


def run_web_dashboard():
    """Launch the interactive dashboard"""
    print()
    print("=" * 70)
    print("   STARTING INTERACTIVE WEB DASHBOARD")
    print("=" * 70)
    print()
    
    try:
        import interactive_analyzer
        interactive_analyzer.main()
    except KeyboardInterrupt:
        print("\n\n✓ Dashboard closed")
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nTrying alternative method...")
        os.system('python3 interactive_analyzer.py')


def run_simple_analyzer():
    """Run the simple command line version"""
    print()
    print("=" * 70)
    print("   RUNNING SIMPLE ANALYZER")
    print("=" * 70)
    print()
    
    try:
        import simple_analyzer
        simple_analyzer.main()
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nTrying alternative method...")
        os.system('python3 simple_analyzer.py')


def show_info():
    """Explain what this does"""
    print()
    print("=" * 70)
    print("  WHAT THIS ANALYZER DOES")
    print("=" * 70)
    print()
    print("   ANALYZES: Customer service conversations")
    print()
    print("   FINDS:")
    print("     • Why customers get angry")
    print("     • What triggers escalations")
    print("     • Common complaint patterns")
    print("     • Legal threat indicators")
    print("     • Repeated issues")
    print()
    print("   SHOWS YOU:")
    print("     • Statistics (how often things happen)")
    print("     • Real examples (actual customer quotes)")
    print("     • Patterns (what goes wrong)")
    print("     • Evidence (proof from conversations)")
    print()
    print("   FEATURES:")
    print("     • Search for specific outcomes")
    print("     • Click to analyze instantly")
    print("     • See visual charts")
    print("     • Read real customer quotes")
    print("     • No coding needed!")
    print()
    print("   EXAMPLE:")
    print("     You click 'Escalation - Legal Threat'")
    print("     You see:")
    print("       → 75% mentioned being frustrated")
    print("       → 40% said 'lawyer' or 'lawsuit'")
    print("       → Real quote: 'I'm contacting my attorney!'")
    print()
    print("=" * 70)
    print()
    input("Press Enter to continue...")


def main():
    """Main program"""
    print_banner()
    
    # Check if everything is ready
    if not check_requirements():
        print("\n  Please fix the issues above and try again.")
        return
    
    # Main loop
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            run_web_dashboard()
            break
        
        elif choice == '2':
            run_simple_analyzer()
            print("\n Analysis complete!")
            print("\n Next: Open 'dashboard.html' in your browser to see visual results!")
            break
        
        elif choice == '3':
            show_info()
        
        elif choice == '4':
            print("\n Goodbye!\n")
            break
        
        else:
            print("\n Invalid choice. Please enter 1, 2, 3, or 4.\n")
            input("Press Enter to continue...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Goodbye!\n")
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        print("\n Tip: Try running 'python3 interactive_analyzer.py' directly")
