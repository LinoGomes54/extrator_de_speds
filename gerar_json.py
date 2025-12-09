import json
from decimal import Decimal
from pathlib import Path

from extrator import extrair_registros_sped


def _decimal_para_float(obj):
    """Permite serializar Decimal em JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Objeto do tipo {type(obj).__name__} não é serializável em JSON")


def converter_pasta_para_json(pasta_entrada="arquivos", pasta_saida="dados_json", extensao="*.txt"):
    """
    Lê todos os arquivos TXT em `pasta_entrada`, extrai os registros SPED e
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

    print(f"📁 Entrada: {entrada}")
    print(f"📁 Saída:   {saida}")
    print(f"🔎 Encontrados {len(arquivos)} arquivo(s) para converter\n")

    for arquivo in arquivos:
        try:
            dados = extrair_registros_sped(str(arquivo), tratar_como_arquivo=True)
            nome_saida = saida / f"{arquivo.stem}.json"
            with open(nome_saida, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, default=_decimal_para_float)
            print(f"✅ {arquivo.name} -> {nome_saida.name}")
        except Exception as e:
            print(f"❌ Erro ao processar '{arquivo.name}': {e}")


if __name__ == "__main__":
    converter_pasta_para_json()

