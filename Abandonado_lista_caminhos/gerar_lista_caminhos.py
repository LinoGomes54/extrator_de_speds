import os
import re
from pathlib import Path

def mapear_pastas_por_codigo(base_path):
    """Mapeia todas as pastas por código"""
    base = Path(base_path).resolve()
    mapeamento = {}
    
    if not base.exists():
        return mapeamento
    
    def processar(diretorio, bloco, codigos_pais):
        try:
            for item in diretorio.iterdir():
                if item.is_dir():
                    nome = item.name
                    match = re.match(r'^([A-Z0-9]+)', nome)
                    if match:
                        codigo = match.group(1)
                        chave = (bloco, tuple(codigos_pais), codigo)
                        # Calcula caminho relativo
                        caminho_rel = item.relative_to(base.parent)
                        mapeamento[chave] = str(caminho_rel).replace('\\', '/')
                        processar(item, bloco, codigos_pais + [codigo])
        except (PermissionError, OSError):
            pass
    
    for bloco_dir in base.iterdir():
        if bloco_dir.is_dir():
            match = re.search(r'(\d+)\s*-\s*Bloco', bloco_dir.name)
            if match:
                num_bloco = match.group(1)
                processar(bloco_dir, num_bloco, [])
    
    return mapeamento

def extrair_registro(linha):
    """Extrai código e descrição"""
    patterns = [
        (r'^\s*##\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$', 0),
        (r'^\s*##\s*\d+\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$', 0),
        (r'^\s*\d+\s*-\s*([A-Z0-9]+)\s*-\s*(.+)$', None),
    ]
    
    for pattern, nivel in patterns:
        match = re.match(pattern, linha)
        if match:
            return match.group(1), match.group(2).strip(), nivel
    return None, None, None

def gerar_lista_caminhos(arquivo_md, base_path):
    """Gera lista de caminhos formatados para copiar"""
    
    print("Mapeando pastas...")
    mapeamento = mapear_pastas_por_codigo(base_path)
    print(f"Encontradas {len(mapeamento)} pastas")
    
    base_obj = Path(base_path).resolve()
    
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    resultado = []
    resultado.append("=" * 80)
    resultado.append("LISTA DE CAMINHOS RELATIVOS PARA COPIAR")
    resultado.append("=" * 80)
    resultado.append("")
    resultado.append("Formato: CÓDIGO | DESCRIÇÃO | CAMINHO RELATIVO")
    resultado.append("")
    resultado.append("=" * 80)
    resultado.append("")
    
    bloco_atual = None
    pilha_codigos = []
    
    for linha in linhas:
        linha_original = linha
        linha = linha.rstrip()
        
        if linha.startswith('# Bloco'):
            if bloco_atual:
                resultado.append("")
                resultado.append("-" * 80)
                resultado.append("")
            
            bloco_atual = None
            pilha_codigos = []
            match = re.search(r'# Bloco\s+([0-9A-Z]+)', linha)
            if match:
                bloco = match.group(1)
                mapeamento_blocos = {
                    '0': ('1 - Bloco 0', '1'), 'B': ('2 - Bloco B', '2'), 'C': ('3 - Bloco C', '3'),
                    'D': ('4 - Bloco D', '4'), 'E': ('5 - Bloco E', '5'), 'G': ('6 - Bloco G', '6'),
                    'H': ('7 - Bloco H', '7'), 'K': ('8 - Bloco K', '8'), '1': ('9 - Bloco 1', '9'),
                    '9': ('10 - Bloco 9', '10')
                }
                if bloco in mapeamento_blocos:
                    bloco_atual = mapeamento_blocos[bloco][0]
                    resultado.append(f"# {bloco_atual}")
                    resultado.append("")
            continue
        
        if not linha or linha.startswith('###') or linha.startswith('(') or linha.startswith('{'):
            continue
        
        codigo, descricao, _ = extrair_registro(linha)
        if not codigo or not bloco_atual:
            continue
        
        nivel_indent = len(linha_original) - len(linha_original.lstrip('\t'))
        if linha_original.lstrip().startswith('##'):
            nivel = 0
        else:
            nivel = nivel_indent + 1
        
        while len(pilha_codigos) > nivel:
            pilha_codigos.pop()
        
        num_bloco = re.search(r'(\d+)\s*-\s*Bloco', bloco_atual).group(1)
        chave = (num_bloco, tuple(pilha_codigos), codigo)
        caminho = mapeamento.get(chave)
        
        # Se não encontrou, tenta buscar recursivamente
        if not caminho and pilha_codigos:
            for i in range(len(pilha_codigos), 0, -1):
                chave_parcial = (num_bloco, tuple(pilha_codigos[:i-1]), pilha_codigos[i-1])
                caminho_pai = mapeamento.get(chave_parcial)
                if caminho_pai:
                    # Procura no diretório
                    pasta_pai = base_obj.parent / caminho_pai
                    if pasta_pai.exists():
                        for item in pasta_pai.iterdir():
                            if item.is_dir() and item.name.startswith(codigo):
                                caminho_rel = item.relative_to(base_obj.parent)
                                caminho = str(caminho_rel).replace('\\', '/')
                                mapeamento[chave] = caminho
                                break
                    break
        
        # Formata a linha
        indentacao = "  " * nivel
        if caminho:
            resultado.append(f"{indentacao}{codigo} | {descricao[:60]} | {caminho}")
        else:
            resultado.append(f"{indentacao}{codigo} | {descricao[:60]} | [NÃO ENCONTRADO]")
        
        pilha_codigos.append(codigo)
    
    return '\n'.join(resultado)

if __name__ == "__main__":
    arquivo_md = "EXTRAIR CÓDIGO - REG SPEDS FISCAL.md"
    base_path = "verificacoes/sped_fiscal"
    arquivo_saida = "lista_caminhos.txt"
    
    print("Gerando lista de caminhos...")
    lista = gerar_lista_caminhos(arquivo_md, base_path)
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(lista)
    
    print(f"✅ Lista gerada: {arquivo_saida}")
    print(f"\nAgora você pode copiar os caminhos e colar no HTML manualmente!")

