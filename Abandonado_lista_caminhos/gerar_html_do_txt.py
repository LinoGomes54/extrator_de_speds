import re
from pathlib import Path
from html import escape

def ler_caminhos_do_txt(arquivo_txt):
    """Lê o arquivo TXT e extrai os caminhos"""
    mapeamento = {}  # {codigo: caminho}
    
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    for linha in linhas:
        linha_original = linha
        linha = linha.strip()
        
        # Ignora linhas vazias, separadores e cabeçalhos
        if not linha or linha.startswith('=') or linha.startswith('Formato:') or linha.startswith('LISTA'):
            continue
        
        # Ignora cabeçalhos de bloco
        if linha.startswith('#') and 'Bloco' in linha:
            continue
        
        # Formato esperado: CÓDIGO | DESCRIÇÃO | CAMINHO
        # ou:   CÓDIGO | DESCRIÇÃO | CAMINHO (com indentação)
        # Pode ter 2 ou 3 partes separadas por |
        partes = [p.strip() for p in linha.split('|')]
        
        if len(partes) >= 2:
            # Primeira parte pode ter indentação + código
            primeira_parte = partes[0].strip()
            match_codigo = re.match(r'^([A-Z0-9]+)', primeira_parte)
            
            if match_codigo:
                codigo = match_codigo.group(1)
                
                # O caminho pode estar na última parte ou na segunda parte
                if len(partes) == 2:
                    # Formato: CÓDIGO | CAMINHO
                    caminho = partes[1]
                elif len(partes) == 3:
                    # Formato: CÓDIGO | DESCRIÇÃO | CAMINHO
                    caminho = partes[2]
                else:
                    # Se tiver mais partes, pega a última
                    caminho = partes[-1]
                
                caminho = caminho.strip()
                
                # Adiciona "verificacoes/" se não tiver
                if caminho and caminho != '[NÃO ENCONTRADO]':
                    if not caminho.startswith('verificacoes/'):
                        caminho = 'verificacoes/' + caminho
                    mapeamento[codigo] = caminho
    
    return mapeamento

def extrair_registro(linha):
    """Extrai código e descrição do markdown"""
    patterns = [
        r'^\s*##\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$',
        r'^\s*##\s*\d+\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$',
        r'^\s*\d+\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, linha)
        if match:
            return match.group(1), match.group(2).strip()
    return None, None

def gerar_html_com_caminhos(arquivo_md, arquivo_txt):
    """Gera HTML usando os caminhos do TXT"""
    
    print("Lendo caminhos do arquivo TXT...")
    mapeamento_caminhos = ler_caminhos_do_txt(arquivo_txt)
    print(f"Encontrados {len(mapeamento_caminhos)} caminhos")
    
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Navegação SPED Fiscal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 10px; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        .info { color: #7f8c8d; margin-bottom: 20px; }
        .bloco { margin: 25px 0; border: 1px solid #e0e0e0; border-radius: 5px; overflow: hidden; }
        .bloco-header { background: #3498db; color: white; padding: 15px; cursor: pointer; font-size: 1.2em; font-weight: bold; }
        .bloco-header:hover { background: #2980b9; }
        .bloco-content { padding: 15px; display: block; }
        .bloco.collapsed .bloco-content { display: none; }
        .registro { padding: 8px 5px; margin: 3px 0; border-left: 3px solid transparent; transition: all 0.2s; }
        .registro:hover { background: #f8f9fa; border-left-color: #3498db; }
        .nivel-0 { font-weight: bold; font-size: 1.1em; color: #2c3e50; }
        .nivel-1 { margin-left: 25px; color: #34495e; }
        .nivel-2 { margin-left: 50px; color: #5d6d7e; font-size: 0.95em; }
        .nivel-3 { margin-left: 75px; color: #7f8c8d; font-size: 0.9em; }
        .nivel-4 { margin-left: 100px; color: #95a5a6; font-size: 0.85em; }
        .nivel-5 { margin-left: 125px; color: #b2babb; font-size: 0.8em; }
        .nivel-6 { margin-left: 150px; color: #d5dbdb; font-size: 0.75em; }
        a { color: #3498db; text-decoration: none; cursor: pointer; display: inline-block; padding: 2px 0; }
        a:hover { color: #2980b9; text-decoration: underline; background: #f0f0f0; padding: 2px 4px; border-radius: 3px; }
        .codigo { font-weight: bold; color: #e74c3c; margin-right: 5px; }
        .sem-link { color: #95a5a6; }
        .toggle { float: right; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 Navegação SPED Fiscal</h1>
        <p class="info">Clique nos links para abrir as pastas. Clique nos cabeçalhos dos blocos para expandir/recolher.</p>
"""
    
    bloco_atual = None
    bloco_html = []
    contador_links = 0
    
    for linha in linhas:
        linha_original = linha
        linha = linha.rstrip()
        
        # Detecta bloco
        if linha.startswith('# Bloco'):
            if bloco_atual and bloco_html:
                html += ''.join(bloco_html)
                bloco_html = []
            
            bloco_atual = None
            match = re.search(r'# Bloco\s+([0-9A-Z]+)', linha)
            if match:
                bloco = match.group(1)
                mapeamento_blocos = {
                    '0': '1 - Bloco 0', 'B': '2 - Bloco B', 'C': '3 - Bloco C',
                    'D': '4 - Bloco D', 'E': '5 - Bloco E', 'G': '6 - Bloco G',
                    'H': '7 - Bloco H', 'K': '8 - Bloco K', '1': '9 - Bloco 1',
                    '9': '10 - Bloco 9'
                }
                if bloco in mapeamento_blocos:
                    bloco_atual = mapeamento_blocos[bloco]
                    bloco_html.append(f'<div class="bloco"><div class="bloco-header" onclick="toggleBloco(this)"><span>{bloco_atual}</span><span class="toggle">▼</span></div><div class="bloco-content">\n')
            continue
        
        if not linha or linha.startswith('###') or linha.startswith('(') or linha.startswith('{'):
            continue
        
        codigo, descricao = extrair_registro(linha)
        if not codigo or not bloco_atual:
            continue
        
        nivel_indent = len(linha_original) - len(linha_original.lstrip('\t'))
        nivel = 0 if linha_original.lstrip().startswith('##') else nivel_indent + 1
        
        nivel_class = f"nivel-{min(nivel, 6)}"
        
        # Busca o caminho no mapeamento
        caminho = mapeamento_caminhos.get(codigo)
        
        if caminho:
            # Escapa para JavaScript
            caminho_js = caminho.replace("'", "\\'")
            link = f'<a href="#" onclick="abrirRelativo(\'{caminho_js}\'); return false;">'
            fechar = '</a>'
            contador_links += 1
        else:
            link = '<span class="sem-link">'
            fechar = '</span>'
        
        bloco_html.append(f'<div class="registro {nivel_class}">{link}<span class="codigo">{escape(codigo)}</span>{escape(descricao)}{fechar}</div>\n')
    
    if bloco_atual and bloco_html:
        bloco_html.append('</div></div>\n')
        html += ''.join(bloco_html)
    
    html += """
    </div>
    <script>
        function toggleBloco(el) {
            const bloco = el.parentElement;
            const toggle = el.querySelector('.toggle');
            bloco.classList.toggle('collapsed');
            toggle.textContent = bloco.classList.contains('collapsed') ? '▶' : '▼';
        }
        
        function abrirRelativo(caminhoRel) {
            let caminhoAbsoluto = '';
            
            if (window.location.protocol === 'file:') {
                // Se abriu via file://, pega o caminho do arquivo HTML
                const htmlPath = decodeURIComponent(window.location.pathname);
                let basePath = htmlPath.substring(0, htmlPath.lastIndexOf('/'));
                // No Windows, remove a barra inicial se existir
                if (basePath.startsWith('/') && basePath.length > 1 && basePath[2] === ':') {
                    basePath = basePath.substring(1);
                }
                const caminhoLimpo = caminhoRel.replace(/^\.\//, '');
                caminhoAbsoluto = basePath + '/' + caminhoLimpo;
            } else {
                // Se abriu via http, constrói caminho relativo
                const htmlPath = window.location.pathname;
                const basePath = htmlPath.substring(0, htmlPath.lastIndexOf('/'));
                const caminhoLimpo = caminhoRel.replace(/^\.\//, '');
                caminhoAbsoluto = basePath + '/' + caminhoLimpo;
            }
            
            const caminhoWin = caminhoAbsoluto.replace(/\//g, '\\\\');
            
            try {
                const uri = 'file:///' + caminhoAbsoluto.replace(/ /g, '%20');
                window.open(uri);
            } catch(e) {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(caminhoWin).then(() => {
                        alert('✓ Caminho copiado!\\n\\n' + caminhoWin + '\\n\\nCole no Explorer (Win+E)');
                    });
                } else {
                    prompt('Copie o caminho:', caminhoWin);
                }
            }
        }
    </script>
</body>
</html>"""
    
    print(f"✅ {contador_links} links gerados no HTML")
    return html

if __name__ == "__main__":
    arquivo_md = "EXTRAIR CÓDIGO - REG SPEDS FISCAL.md"
    arquivo_txt = "lista_caminhos.txt"
    arquivo_html = "navegacao_sped_fiscal.html"
    
    print("Gerando HTML a partir do arquivo TXT...")
    html = gerar_html_com_caminhos(arquivo_md, arquivo_txt)
    
    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Arquivo HTML criado: {arquivo_html}")

