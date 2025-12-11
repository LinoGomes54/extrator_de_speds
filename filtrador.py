import chardet
import re
import os
import glob
import sys
from pathlib import Path

import builtins


def _safe_print(*args, **kwargs):
    """
    Evita UnicodeEncodeError em consoles Windows que não suportam emojis.
    Substitui caracteres não representáveis por '?'.
    """
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe_args = []
    for arg in args:
        if isinstance(arg, str):
            safe_args.append(arg.encode(encoding, errors="replace").decode(encoding, errors="ignore"))
        else:
            safe_args.append(arg)
    builtins.print(*safe_args, **kwargs)


# Sobrescreve o print localmente neste módulo
print = _safe_print

def analisar_arquivo(nome_arquivo):
    print(f"Analisando arquivo: {nome_arquivo}")
    if not os.path.exists(nome_arquivo):
        print(f"❌ Arquivo '{nome_arquivo}' não encontrado!")
        return False
    tamanho = os.path.getsize(nome_arquivo)
    print(f"📁 Tamanho do arquivo: {tamanho:,} bytes")
    with open(nome_arquivo, 'rb') as f:
        primeiros_bytes = f.read(1000)
    chars_binarios = sum(1 for b in primeiros_bytes if b < 32 and b not in [9, 10, 13])
    print(f"🔍 Caracteres de controle encontrados nos primeiros 1000 bytes: {chars_binarios}")
    texto_inicial = primeiros_bytes.decode('utf-8', errors='ignore')
    if '-----BEGIN' in texto_inicial or 'CERTIFICATE' in texto_inicial:
        print("🔐 Possível certificado digital detectado")
    return True

def tentar_ler_arquivo(nome_arquivo):
    print("\n" + "="*60)
    print("🔄 INICIANDO LEITURA DO ARQUIVO")
    print("="*60)
    try:
        print("📊 Estratégia 1: Detectando encoding...")
        with open(nome_arquivo, 'rb') as f:
            raw_data = f.read()
            resultado = chardet.detect(raw_data)
            encoding = resultado['encoding']
            confianca = resultado['confidence']
            print(f"   ✅ Encoding detectado: {encoding} (confiança: {confianca:.2%})")
            if encoding and confianca > 0.7:
                conteudo = raw_data.decode(encoding, errors='replace')
                print(f"   ✅ Leitura bem-sucedida com {encoding}")
                return conteudo, encoding
    except Exception as e:
        print(f"   ❌ Erro com chardet: {e}")
    
    print("\n📋 Estratégia 2: Testando encodings comuns...")
    encodings_para_tentar = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'windows-1252', 'cp850', 'ascii']
    for encoding in encodings_para_tentar:
        try:
            with open(nome_arquivo, 'r', encoding=encoding, errors='replace') as f:
                conteudo = f.read()
                print(f"   ✅ Sucesso com encoding: {encoding}")
                return conteudo, encoding
        except Exception as e:
            print(f"   ❌ Falhou com {encoding}: {e}")
            continue

    print("\n🧹 Estratégia 3: Limpeza agressiva...")
    try:
        with open(nome_arquivo, 'rb') as f:
            raw_data = f.read()
            conteudo = raw_data.decode('utf-8', errors='ignore')
            conteudo = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', conteudo)
            conteudo = re.sub(r'[^\x20-\x7E\r\n\t\u00A0-\uFFFF]', '', conteudo)
            print("   ✅ Arquivo lido com limpeza agressiva")
            return conteudo, "utf-8-limpo"
    except Exception as e:
        print(f"   ❌ Erro na limpeza agressiva: {e}")
    print("   ❌ Todas as estratégias falharam")
    return None, None

def limpar_certificados_e_assinaturas(conteudo):
    print("\n🔐 Removendo certificados digitais...")
    padroes_cert = [
        r'-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----',
        r'-----BEGIN.*?CERTIFICATE.*?-----.*?-----END.*?CERTIFICATE.*?-----',
        r'-----BEGIN[^-]*-----.*?-----END[^-]*-----',
        r'<ds:Signature.*?</ds:Signature>',
        r'<Signature.*?</Signature>',
        r'BEGIN PKCS7.*?END PKCS7',
        r'MII[A-Za-z0-9+/=]{100,}',
    ]
    conteudo_original = conteudo
    certificados_removidos = 0
    for padrao in padroes_cert:
        matches = re.findall(padrao, conteudo, flags=re.DOTALL | re.IGNORECASE)
        if matches:
            certificados_removidos += len(matches)
            conteudo = re.sub(padrao, '[CERTIFICADO/ASSINATURA REMOVIDA]', conteudo, flags=re.DOTALL | re.IGNORECASE)
    if certificados_removidos > 0:
        print(f"   ✅ {certificados_removidos} certificado(s)/assinatura(s) removido(s)")
        reducao = len(conteudo_original) - len(conteudo)
        print(f"   📉 Redução no tamanho: {reducao:,} caracteres")
    else:
        print("   ℹ️  Nenhum certificado/assinatura encontrado")
    return conteudo

def filtrar_linhas_especificas(conteudo, codigos_desejados):
    print(f"\n🔍 FILTRANDO LINHAS ESPECÍFICAS")
    print(f"   📋 Códigos desejados: {', '.join(codigos_desejados)}")
    linhas = conteudo.split('\n')
    linhas_filtradas = []
    contadores = {codigo: 0 for codigo in codigos_desejados}
    total_linhas_originais = len(linhas)

    # Pré-agrupa códigos por tamanho para acelerar a filtragem
    codigos_por_tamanho = {}
    for codigo in codigos_desejados:
        codigos_por_tamanho.setdefault(len(codigo), set()).add(codigo)

    for linha in linhas:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        for tamanho, codigos_set in codigos_por_tamanho.items():
            if len(linha_limpa) < tamanho:
                continue
            prefixo = linha_limpa[:tamanho]
            if prefixo in codigos_set:
                linhas_filtradas.append(linha)
                contadores[prefixo] += 1
                break
    print(f"   📊 RESULTADO DO FILTRO:")
    print(f"      📝 Linhas originais: {total_linhas_originais:,}")
    print(f"      ✅ Linhas filtradas: {len(linhas_filtradas):,}")
    for codigo, count in contadores.items():
        msg = f"      🏷️  {codigo}: {count:,} linhas" if count > 0 else f"      ⚠️  {codigo}: 0 linhas (não encontrado)"
        print(msg)
    percentual = (len(linhas_filtradas) / total_linhas_originais) * 100 if total_linhas_originais > 0 else 0
    print(f"      📈 Percentual mantido: {percentual:.1f}%")
    return '\n'.join(linhas_filtradas)

def salvar_arquivo_limpo(conteudo, nome_original, sufixo="_FILTRADO"):
    # Evita gerar nomes encadeados (_FILTRADO_FILTRADO)
    if sufixo and nome_original.endswith('.txt') and nome_original[:-4].endswith(sufixo):
        nome_limpo = nome_original
    else:
        nome_limpo = nome_original.replace('.txt', f'{sufixo}.txt') if sufixo else nome_original
    try:
        with open(nome_limpo, 'w', encoding='utf-8', errors='replace') as f:
            f.write(conteudo)
        print(f"\n💾 Arquivo salvo: '{nome_limpo}'")
        print(f"   📏 Tamanho do conteúdo: {len(conteudo):,} caracteres")
        return nome_limpo
    except Exception as e:
        print(f"   ❌ Erro ao salvar arquivo: {e}")
        return None

def mostrar_preview(conteudo, titulo="PREVIEW", limite=500):
    print(f"\n👀 {titulo} (primeiros {limite} caracteres):")
    print("-" * 50)
    print(conteudo[:limite])
    if len(conteudo) > limite:
        print("...")
    print("-" * 50)

def processar_arquivo(nome_arquivo, codigos_desejados, pasta_saida=None):
    print(f"\n🔥 PROCESSANDO ARQUIVO: {nome_arquivo}")
    print("=" * 80)
    if not analisar_arquivo(nome_arquivo):
        return False
    conteudo, encoding_usado = tentar_ler_arquivo(nome_arquivo)
    if conteudo:
        print(f"\n✅ SUCESSO! Arquivo lido com encoding: {encoding_usado}")
        conteudo_limpo = limpar_certificados_e_assinaturas(conteudo)
        conteudo_filtrado = filtrar_linhas_especificas(conteudo_limpo, codigos_desejados)
        print(f"\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   📏 Tamanho original: {len(conteudo):,} caracteres")
        print(f"   📏 Tamanho limpo: {len(conteudo_limpo):,} caracteres")
        print(f"   📏 Tamanho filtrado: {len(conteudo_filtrado):,} caracteres")
        print(f"   📝 Linhas filtradas: {conteudo_filtrado.count(chr(10)) + 1:,}")
        nome_base = os.path.basename(nome_arquivo)
        nome_arquivo_saida = os.path.join(pasta_saida, nome_base) if pasta_saida else nome_arquivo
        arquivo_filtrado = salvar_arquivo_limpo(conteudo_filtrado, nome_arquivo_saida, "_FILTRADO")
        if len(conteudo_filtrado.strip()) > 0:
            mostrar_preview(conteudo_filtrado, "CONTEÚDO FILTRADO", 300)
        else:
            print("\n⚠️  Nenhuma linha com os códigos especificados foi encontrada!")
        return True
    else:
        print("\n❌ FALHA: Não foi possível ler o arquivo.")
        return False

def obter_arquivos_para_processar(pasta_entrada, extensao="*.txt"):
    caminho_busca = str(Path(pasta_entrada) / extensao)
    arquivos = glob.glob(caminho_busca)
    # Evita reprocessar arquivos já filtrados
    return [arq for arq in arquivos if not arq.endswith('_FILTRADO.txt') and not arq.endswith('_FILTRADO_FILTRADO.txt')]

def main():
    print("🚀 LEITOR E FILTRO DE ARQUIVOS EM LOTE COM CERTIFICADOS DIGITAIS")
    print("=" * 80)
    # Usa caminhos baseados na localização do arquivo atual, para evitar erro de diretório de trabalho
    base_dir = Path(__file__).resolve().parent
    pasta_entrada = base_dir / "arquivos"
    pasta_saida = base_dir / "filtrados"
    extensao = "*.txt"
    codigos_desejados = [
        '|0000|', '|0001|', '|0002|', '|0005|', '|0015|', '|0100|',
        '|0150|', '|0175|', '|0190|', '|0200|', '|0220|',
        '|0300|', '|0305|', '|0400|', '|0450|', '|0460|',
        '|0500|', '|0600|', '|0990|', '|B001|', '|B990|',
        '|C001|', '|C100|', '|C101|', '|C105|', '|C110|', '|C111|', '|C112|', '|C113|', '|C114|', '|C116|', '|C120|',
        '|C170|', '|C176|', '|C177|', '|C185|', '|C186|', '|C190|', '|C191|', '|C195|', '|C197|',
        '|C350|', '|C370|', '|C380|', '|C390|', '|C400|', '|C405|', '|C410|', '|C420|',
        '|C460|', '|C470|', '|C480|', '|C490|',
        '|C500|', '|C590|', '|C591|', '|C595|', '|C597|',
        '|C700|', '|C790|', '|C791|',
        '|C800|', '|C810|', '|C815|', '|C850|',
        '|C990|',
        '|D001|',
        '|D100|', '|D101|', '|D105|',
        '|D130|', '|D140|', '|D150|', '|D160|', '|D161|', '|D162|', '|D170|', '|D180|',
        '|D190|', '|D195|', '|D197|',
        '|D200|', '|D201|', '|D205|',
        '|D300|', '|D301|', '|D310|', '|D350|', '|D355|', '|D360|', '|D365|', '|D370|', '|D390|',
        '|D400|', '|D410|', '|D411|', '|D420|',
        '|D500|', '|D510|', '|D530|', '|D590|',
        '|D695|', '|D696|', '|D697|',
        '|D700|', '|D730|', '|D731|', '|D735|', '|D737|', '|D750|', '|D760|', '|D761|',
        '|D990|',
        '|E001|', '|E100|', '|E110|', '|E111|', '|E112|', '|E113|', '|E115|', '|E116|',
        '|E200|', '|E210|', '|E220|', '|E230|', '|E250|',
        '|E300|', '|E310|', '|E311|', '|E312|', '|E313|', '|E316|',
        '|E500|', '|E510|', '|E520|', '|E530|', '|E531|', '|E990|',
        '|G001|', '|G110|', '|G125|', '|G126|', '|G130|', '|G140|', '|G990|',
        '|H001|', '|H005|', '|H010|', '|H020|', '|H030|', '|H990|',
        '|K001|', '|K100|', '|K200|', '|K210|', '|K215|', '|K220|',
        '|K230|', '|K235|', '|K250|', '|K255|', '|K260|', '|K265|',
        '|K270|', '|K275|', '|K280|', '|K290|'
    ]
    os.makedirs(pasta_entrada, exist_ok=True)
    os.makedirs(pasta_saida, exist_ok=True)
    print(f"📁 Pasta de entrada: {pasta_entrada}")
    print(f"📁 Pasta de saída: {pasta_saida}")
    print(f"🔍 Extensão de arquivos: {extensao}")
    print(f"🏷️  Códigos a filtrar: {', '.join(codigos_desejados)}")
    arquivos = obter_arquivos_para_processar(pasta_entrada, extensao)
    if not arquivos:
        print(f"\n❌ Nenhum arquivo encontrado em '{pasta_entrada}' com extensão '{extensao}'")
        return
    print(f"\n📋 Encontrados {len(arquivos)} arquivo(s) para processar:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"   {i}. {os.path.basename(arquivo)}")
    total_arquivos = len(arquivos)
    arquivos_processados = 0
    arquivos_com_sucesso = 0
    arquivos_com_erro = 0
    print(f"\n🔄 INICIANDO PROCESSAMENTO EM LOTE...")
    print("=" * 80)
    for i, arquivo in enumerate(arquivos, 1):
        print(f"\n🔢 ARQUIVO {i}/{total_arquivos}")
        try:
            sucesso = processar_arquivo(arquivo, codigos_desejados, pasta_saida)
            arquivos_processados += 1
            if sucesso:
                arquivos_com_sucesso += 1
                print(f"✅ Arquivo '{os.path.basename(arquivo)}' processado com sucesso!")
            else:
                arquivos_com_erro += 1
                print(f"⚠️  Arquivo '{os.path.basename(arquivo)}' com avisos.")
        except Exception as e:
            arquivos_processados += 1
            arquivos_com_erro += 1
            print(f"❌ Erro ao processar '{os.path.basename(arquivo)}': {str(e)}")
        if i < total_arquivos:
            print("\n" + "🔸" * 80)
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO FINAL DO PROCESSAMENTO")
    print("=" * 80)
    print(f"📁 Total de arquivos encontrados: {total_arquivos}")
    print(f"🔄 Arquivos processados: {arquivos_processados}")
    print(f"✅ Com sucesso: {arquivos_com_sucesso}")
    print(f"⚠️  Com erro: {arquivos_com_erro}")

if __name__ == "__main__":
    main()
