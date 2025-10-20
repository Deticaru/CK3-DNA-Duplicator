#!/usr/bin/env python3
"""
CK3 DNA Duplicator - Standalone CLI Version
A single-file tool for duplicating Crusader Kings III character DNA strings.
No external dependencies required - just Python 3.
"""

import re
import subprocess
import platform


# ============================================================================
# DNA DUPLICATION FUNCTIONS
# ============================================================================

def duplicate_dna(input_text):
    """
    Main function that duplicates DNA values in the complete text.
    
    Args:
        input_text (str): The complete text containing the genes section
        
    Returns:
        str: The text with duplicated values (A->B in regular genes, A1->B1 A2->B2 in colors)
    """
    try:
        # Extract the genes section
        genes_section, start_pos, end_pos = _extract_genes_section(input_text)
        
        # Get the internal genes content
        genes_content = genes_section[genes_section.find('{')+1:genes_section.rfind('}')]
        
        # Duplicate color genes
        genes_content = _duplicate_color_genes(genes_content)
        
        # Duplicate regular genes
        genes_content = _duplicate_regular_genes(genes_content)
        
        # Rebuild the genes section
        modified_genes_section = f"genes={{{genes_content}}}"
        
        # Replace in the original text
        output_text = input_text[:start_pos] + modified_genes_section + input_text[end_pos:]
        
        return output_text
        
    except Exception as e:
        return f"Error: {str(e)}"


def _extract_genes_section(input_text):
    """Extracts the genes section from the text"""
    start_pattern = r'genes\s*=\s*\{'
    match = re.search(start_pattern, input_text)
    
    if not match:
        raise ValueError("Could not find 'genes' section in input")
    
    start_pos = match.start()
    brace_start = match.end() - 1
    
    # Count braces to find the closing one
    open_braces = 1
    pos = brace_start + 1
    
    while pos < len(input_text) and open_braces > 0:
        if input_text[pos] == '{':
            open_braces += 1
        elif input_text[pos] == '}':
            open_braces -= 1
        pos += 1
    
    if open_braces > 0:
        raise ValueError("Could not find closing brace for 'genes' section")
    
    end_pos = pos
    genes_section = input_text[start_pos:end_pos]
    
    return genes_section, start_pos, end_pos


def _duplicate_color_genes(genes_content):
    """Duplicates A1->B1 and A2->B2 values for hair_color, skin_color, eye_color"""
    color_pattern = r'(hair_color|skin_color|eye_color)=\{\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\}'
    
    def color_replacer(match):
        gene_name = match.group(1)
        a1 = match.group(2)
        a2 = match.group(3)
        return f'{gene_name}={{ {a1} {a2} {a1} {a2} }}'
    
    return re.sub(color_pattern, color_replacer, genes_content)


def _duplicate_regular_genes(genes_content):
    """Duplicates the first value of each regular gene pair"""
    pattern = r'(\{\s*")([^"]+)("\s+)(\d+)(\s+")([^"]+)("\s+)(\d+)(\s*\})'
    
    def replacer(match):
        first_key = match.group(2)
        first_value = match.group(4)
        return f'{{ "{first_key}" {first_value} "{first_key}" {first_value} }}'
    
    return re.sub(pattern, replacer, genes_content)


# ============================================================================
# CLIPBOARD FUNCTIONS
# ============================================================================

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
            # For Linux use xclip or xsel
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
            # For Windows use clip
            subprocess.run(['clip'], input=text, text=True, check=True)
            return True
            
        elif system == "Darwin":  # macOS
            # For macOS use pbcopy
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            return True
        else:
            print(f"Unsupported operating system: {system}")
            return False
            
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False


# ============================================================================
# MAIN CLI INTERFACE
# ============================================================================

def main():
    """Main CLI program function"""
    print("="*60)
    print("    DNA DUPLICATOR - CRUSADER KINGS III")
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
    main()
