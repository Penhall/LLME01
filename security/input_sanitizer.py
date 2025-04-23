import re
import html

class InputSanitizer:
    """Sanitiza entradas de texto contra XSS e SQL injection"""
    
    def __init__(self):
        # Padrões mais específicos para evitar falsos positivos
        self.xss_pattern = re.compile(
            r'(<script\b[^>]*>[\s\S]*?<\/script>|<\w+\s+.*?javascript:\s*.*?>)',
            re.IGNORECASE
        )
        self.sql_pattern = re.compile(
            r'\b(union\s+all|select\s+[\w\*,\s]+from|insert\s+into|delete\s+from|drop\s+table)\b',
            re.IGNORECASE
        )

    def sanitize(self, text: str) -> str:
        """Remove conteúdo malicioso e codifica caracteres especiais"""
        if not text:
            return text
            
        # Remover padrões perigosos sem alterar o texto original
        clean_text = self.xss_pattern.sub('', text)
        clean_text = self.sql_pattern.sub('[SQL]', clean_text)
        
        # Codificar caracteres HTML mantendo a integridade do texto
        return html.escape(clean_text)