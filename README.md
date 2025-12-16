# Extrator de SPEDs

Automação em Python para trabalhar com arquivos SPED, com foco em:

- extração de registros de SPED Fiscal e SPED Contribuições;
- conversão de arquivos TXT para JSON estruturado;
- filtro e higienização de arquivos (remoção de certificados/assinaturas digitais, limpeza de caracteres, etc.).

## Requisitos

- Python 3.x
- Bibliotecas da própria linguagem (`os`, `decimal`, `json`, `pathlib`, etc.)
- Biblioteca externa:
  - `chardet` (utilizada apenas por `filtrador.py`)

Instalação da dependência externa:

```bash
pip install chardet
```

## Estrutura do projeto

- `extrator_sped_fiscal.py` – funções de extração e estruturação de registros do SPED Fiscal.
- `extrator_sped_contribuicoes.py` – funções de extração e estruturação de registros do SPED Contribuições.
- `gerar_json.py` – script principal que lê TXT em `arquivos/` e gera JSON em `dados_json/`, detectando automaticamente se o arquivo é Fiscal ou Contribuições.
- `filtrador.py` – leitura em lote, remoção de certificados/assinaturas digitais e filtro de registros relevantes; grava arquivos filtrados em `filtrados/`.
- `arquivos/` – pasta de entrada para arquivos SPED (`*.txt`).
- `dados_json/` – pasta de saída dos arquivos JSON gerados.
- `Backup/`, `verificacoes/` – pastas auxiliares para testes/armazenamento temporário.

## Como usar – conversão para JSON

1. (Opcional) Crie e ative um ambiente virtual.
2. Instale a dependência externa: `pip install chardet`.
3. Copie os arquivos SPED (Fiscal ou Contribuições) para a pasta `arquivos/` (no mesmo nível dos scripts).
4. No terminal, dentro da pasta do projeto, execute:

```bash
python gerar_json.py
```

- Os arquivos JSON serão criados em `dados_json/` com o mesmo nome do arquivo de origem.
- Se o extrator encontrar linhas não reconhecidas, será criado também um arquivo `<NOME>_LINHAS_IGNORADAS.txt` com essas linhas.

## Como usar – filtro e limpeza de arquivos (opcional)

Se seus arquivos SPED estiverem muito “sujos” (certificados digitais, assinaturas, caracteres binários, etc.), você pode rodar o filtro antes da extração:

```bash
python filtrador.py
```

- Os arquivos filtrados serão salvos em uma pasta `filtrados/` com sufixo `_FILTRADO.txt`.
- Depois disso, você pode copiar/substituir esses arquivos na pasta `arquivos/` e rodar novamente `python gerar_json.py` para gerar os JSONs a partir dos arquivos já limpos.

## Uso como biblioteca (opcional)

Também é possível utilizar os extratores diretamente no seu código Python:

```python
from extrator_sped_fiscal import extrair_registros_sped
from extrator_sped_contribuicoes import extrair_registros_sped as extrair_sped_contribuicoes

dados_fiscal = extrair_registros_sped("meu_sped_fiscal.txt", tratar_como_arquivo=True)
dados_contrib = extrair_sped_contribuicoes("meu_sped_contribuicoes.txt", tratar_como_arquivo=True)
```

Cada chamada retorna um dicionário com os registros estruturados do respectivo arquivo SPED, pronto para ser serializado em JSON ou manipulado em outras rotinas.
