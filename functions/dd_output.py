import subprocess
import platform

def copy_to_clipboard(text):
    """
    Copies text to system clipboard.
    
    Args:
        text (str): The text to copy to clipboard
        
    Returns:
        bool: True if successful, False if error
    """
    try:
        system = platform.system()
        
        if system == "Linux":
            # Para Linux usa xclip o xsel
            try:
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=text, text=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(['xsel', '--clipboard', '--input'], 
                                 input=text, text=True, check=True)
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("Error: xclip or xsel not found. Install one of them:")
                    print("  sudo apt install xclip")
                    print("  or")
                    print("  sudo apt install xsel")
                    return False
                    
        elif system == "Windows":
            # Para Windows usa clip
            subprocess.run(['clip'], input=text, text=True, check=True)
            return True
            
        elif system == "Darwin":  # macOS
            # Para macOS usa pbcopy
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            return True
        else:
            print(f"Unsupported operating system: {system}")
            return False
            
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def get_from_clipboard():
    """
    Gets text from system clipboard.
    
    Returns:
        str: Text from clipboard, or None if error
    """
    try:
        system = platform.system()
        
        if system == "Linux":
            # Para Linux usa xclip o xsel
            try:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                      capture_output=True, text=True, check=True)
                return result.stdout
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    result = subprocess.run(['xsel', '--clipboard', '--output'], 
                                          capture_output=True, text=True, check=True)
                    return result.stdout
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("Error: xclip or xsel not found for reading from clipboard")
                    return None
                    
        elif system == "Windows":
            # Para Windows usa powershell
            result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout
            
        elif system == "Darwin":  # macOS
            # Para macOS usa pbpaste
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
            return result.stdout
        else:
            print(f"Unsupported operating system: {system}")
            return None
            
    except Exception as e:
        print(f"Error reading from clipboard: {e}")
        return None
