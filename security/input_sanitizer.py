import re
import html

class InputSanitizer:
    """Sanitiza entradas de texto contra XSS e SQL injection"""
    
    def __init__(self):
        self.xss_pattern = re.compile(r'<script.*?>.*?</script>|<.*?javascript:.*?>', re.IGNORECASE)
        self.sql_pattern = re.compile(r'\b(union|select|insert|delete|drop|alter)\b', re.IGNORECASE)

    def sanitize(self, text: str) -> str:
        """Remove conteúdo malicioso e codifica caracteres especiais"""
        if not text:
            return text
            
        original = text.strip()
        # Remover padrões perigosos
        clean_text = self.xss_pattern.sub('', original)
        clean_text = self.sql_pattern.sub('[REMOVED]', clean_text)
        
        # Verificar se houve alteração no conteúdo
        if clean_text != original:
            raise ValueError("Conteúdo potencialmente malicioso detectado")
        
        # Codificar caracteres HTML
        return html.escape(clean_text)