import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Optional

import builtins

from extrator_sped_contribuicoes import extrair_registros_sped as extrair_sped_contribuicoes
from extrator_sped_fiscal import extrair_registros_sped as extrair_sped_fiscal


def _safe_print(*args, **kwargs):
    """
    Evita UnicodeEncodeError em consoles Windows que nao suportam emojis.
    Substitui caracteres nao representaveis por '?'.
    """
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    safe_args = []
    for arg in args:
        if isinstance(arg, str):
            safe_args.append(arg.encode(encoding, errors="replace").decode(encoding, errors="ignore"))
        else:
            safe_args.append(arg)
    builtins.print(*safe_args, **kwargs)


# Sobrescreve o print localmente neste modulo
print = _safe_print


def _decimal_para_float(obj):
    """Permite serializar Decimal em JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Objeto do tipo {type(obj).__name__} nao e serializavel em JSON")


def _identificar_tipo_sped(caminho_arquivo: Path) -> Optional[str]:
    """
    Detecta o tipo do SPED com base nos blocos encontrados:
    - Fiscal: possui blocos E ou H
    - Contribuicoes: possui blocos M ou F
    Retorna 'fiscal', 'contribuicoes' ou None se nao identificar.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as handle:
            for linha in handle:
                partes = [p.strip() for p in linha.split("|") if p.strip()]
                if not partes:
                    continue
                registro = partes[0].upper()
                if registro.startswith(("E", "H")):
                    return "fiscal"
                if registro.startswith(("M", "F")):
                    return "contribuicoes"
    except FileNotFoundError:
        return None
    return None


def converter_pasta_para_json(pasta_entrada="arquivos", pasta_saida="dados_json", extensao="*.txt"):
    """
    Le todos os arquivos TXT em `pasta_entrada`, extrai os registros SPED e
    grava cada resultado em JSON dentro de `pasta_saida`.
    """
    base_dir = Path(__file__).resolve().parent
    entrada = base_dir / pasta_entrada
    saida = base_dir / pasta_saida
    entrada.mkdir(parents=True, exist_ok=True)
    saida.mkdir(parents=True, exist_ok=True)

    arquivos = sorted(entrada.glob(extensao))
    if not arquivos:
        print(f"Nenhum arquivo '{extensao}' encontrado em {entrada}")
        return

    print(f"[info] Entrada: {entrada}")
    print(f"[info] Saida:   {saida}")
    print(f"[info] Encontrados {len(arquivos)} arquivo(s) para converter\n")

    for arquivo in arquivos:
        try:
            tipo_sped = _identificar_tipo_sped(arquivo)
            if tipo_sped == "fiscal":
                dados = extrair_sped_fiscal(str(arquivo), tratar_como_arquivo=True)
            else:
                if tipo_sped is None:
                    print(f"[aviso] Tipo do SPED nao identificado em {arquivo.name}. Assumindo Contribuicoes.")
                dados = extrair_sped_contribuicoes(str(arquivo), tratar_como_arquivo=True)

            nome_saida = saida / f"{arquivo.stem}.json"
            with open(nome_saida, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, default=_decimal_para_float)
            print(f"[ok] {arquivo.name} -> {nome_saida.name}")

            # Cria arquivo apenas com as linhas ignoradas pelo extrator, se houver
            linhas_ignoradas = dados.get("linhas_ignoradas") or []
            if linhas_ignoradas:
                nome_ignoradas = saida / f"{arquivo.stem}_LINHAS_IGNORADAS.txt"
                with open(nome_ignoradas, "w", encoding="utf-8") as f_ign:
                    for linha in linhas_ignoradas:
                        f_ign.write(linha + "\n")
                print(f"[ok] Linhas ignoradas salvas em {nome_ignoradas.name}")

        except Exception as e:
            print(f"[erro] Erro ao processar '{arquivo.name}': {e}")


if __name__ == "__main__":
    converter_pasta_para_json()
