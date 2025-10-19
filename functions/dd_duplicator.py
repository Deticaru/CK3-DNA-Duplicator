import re

def duplicate_dna(input_text):
    """
    Main function that duplicates DNA values in the complete text.
    
    Args:
        input_text (str): The complete text containing the genes section
        
    Returns:
        str: The text with duplicated values (A->B in regular genes, A1->B1 A2->B2 in colors)
    """
    try:
        # Extraer la sección de genes
        genes_section, start_pos, end_pos = _extract_genes_section(input_text)
        
        # Obtener el contenido interno de genes
        genes_content = genes_section[genes_section.find('{')+1:genes_section.rfind('}')]
        
        # Duplicar genes de color
        genes_content = _duplicate_color_genes(genes_content)
        
        # Duplicar genes regulares
        genes_content = _duplicate_regular_genes(genes_content)
        
        # Reconstruir la sección de genes
        modified_genes_section = f"genes={{{genes_content}}}"
        
        # Reemplazar en el texto original
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
