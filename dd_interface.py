from functions import duplicate_dna, copy_to_clipboard
import webview
import os

# API class to expose Python functions to JavaScript
class Api:
    def duplicate_dna(self, input_text):
        """Process DNA and return the result"""
        return duplicate_dna(input_text)
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard and return success status"""
        return copy_to_clipboard(text)

def start_gui():
    """Start the GUI application"""
    # Get the path to the HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'interface.html')
    
    # Create API instance
    api = Api()
    
    # Create the webview window with the HTML file
    icon_path = os.path.join(current_dir, 'icon.ico')
    window = webview.create_window(
        title='DNA Duplicator - Crusader Kings III',
        url=html_path,
        js_api=api,
        width=1000,
        height=700,
        resizable=True,
        text_select=True,
    )
    
    # Start the webview
    webview.start()

def main():
    """Main program function"""
    print("="*60)
    print("    DNA DUPLICATOR - CRUSADER KINGS")
    print("="*60)
    print()
    print("This program duplicates DNA values:")
    print("• Regular genes: A -> B (first value copied to second)")
    print("• Color genes: A1 A2 B1 B2 -> A1 A2 A1 A2")
    print()
    print("Instructions:")
    print("1. Paste your complete DNA text below")
    print("2. When finished pasting, press Ctrl+D (Linux/Mac) or Ctrl+Z+Enter (Windows)")
    print("   Or alternatively, type 'END' on a new line")
    print("3. The result will be displayed and copied to clipboard")
    print()
    print("-" * 60)
    print("Paste your content here:")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return
        except EOFError:
            # Ctrl+D pressed - end input
            break
    
    if not lines:
        print("No content entered.")
        return
    
    input_text = '\n'.join(lines)
    
    print("\n" + "-" * 60)
    print("Processing...")
    
    # Process the DNA
    result = duplicate_dna(input_text)
    
    if result.startswith("Error:"):
        print(f"❌ {result}")
        return
    
    print("✅ Processing successful!")
    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)
    print("=" * 60)
    
    # Try to copy to clipboard
    print("\nCopying to clipboard...")
    if copy_to_clipboard(result):
        print("✅ Result copied to clipboard successfully!")
        print("You can paste it directly into your file.")
    else:
        print("❌ Could not copy to clipboard.")
        print("You can manually copy the result above.")
    
    print("\nDone! Press Enter to exit...")
    input()

if __name__ == "__main__":
    import sys
    
    # Check if user wants CLI mode with --cli flag
    if "--cli" in sys.argv:
        main()
    else:
        # Default: Start GUI
        start_gui()
