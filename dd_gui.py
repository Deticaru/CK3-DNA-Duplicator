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

if __name__ == "__main__":
    start_gui()
