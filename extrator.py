import os
from decimal import Decimal, InvalidOperation


def extrair_registros_sped(txt_ou_caminho: str, tratar_como_arquivo: bool = True):
    """
    Extrai e estrutura registros SPED (0000, 0001, 0002, 0005, 0015, 0100,
    0150, 0175, 0190, 0200/0220, 0300/0305, 0400, 0450, 0460, 0500, 0600,
    0990, B001/B990, C001, C100/C101/C105/C110/C120/C170,
    C176/C177, C185/C186, C190/C191/C195/C197, C350/C370/C380/C390,
    C400/C405/C410/C420, C460/C470/C480/C490,
    C500/C590/C591/C595/C597, C700/C790/C791, C800/C810/C815/C850,
    C990, D001, D100/D101/D105, D130/D140/D150/D160/D161/D162/D170/D180,
    D190/D195/D197, D200/D201/D205,
    D300/D301/D310, D350/D355, D360/D365/D370, D390,
    D400/D410/D411/D420,
    D500/D510/D530/D590,
    D695/D696/D697,
    D700/D730/D731/D735/D737/D750/D760/D761,
    D990, E001/E100/E110/E111/E112/E113/E115/E116,
    E200/E210/E220/E230/E250, E300/E310/E311/E312/E313/E316,
    E500/E510/E520/E530/E531/E990,
    G001/G110/G125/G126/G130/G140/G990,
    H001/H005/H010/H020/H030/H990,
    K001/K100/K200/K210/K215/K220/K230/K235/K250/K255/K260/K265/K270/K275/K280/K290/K291/K292/K300/K301/K302/K990,
    1001/1010/1100/1105/1200/1210/1250/1255/1300/1310/1320,
    1390/1391/1400/1500/1510/1601/1700/1710/1800/1900/1910/1920/1921/1922,
    9001/9900/9990/9999)
    a partir de um TXT (conteúdo ou caminho do arquivo).

    Retorno:
      dict com chaves:
        - abertura (0000): dict
        - abertura_bloco0 (0001): dict
        - classificacoes (0002): list[dict]
        - dados_complementares (0005): list[dict]
        - substitutos_uf (0015): list[dict]
        - contabilistas (0100): list[dict]
        - participantes (0150): list[dict]
        - historico_participantes (0175): list[dict]
        - unidades (0190): list[dict]
        - itens (0200): list[dict] com "conversoes" (0220)
        - bens (0300): list[dict] com "usos" (0305)
        - natureza_operacao (0400): list[dict]
        - info_complementar (0450): list[dict]
        - observacoes_lancamento (0460): list[dict]
        - plano_contas (0500): list[dict]
        - centros_custos (0600): list[dict]
        - fechamento_bloco0 (0990): dict
        - abertura_bloco_b (B001): dict
        - fechamento_bloco_b (B990): dict
        - abertura_bloco_c (C001): dict
        - notas (C100): list[dict] com "itens" (C170)
        - complementos_c176 (C176): list[dict] (aninhado em C100)
        - complementos_c177 (C177): list[dict] (aninhado em C100)
        - complementos_c185 (C185): list[dict] (aninhado em C100)
        - complementos_c186 (C186): list[dict] (aninhado em C100)
        - analiticos_c190 (C190): list[dict] (aninhado em C100)
        - fcp_c191 (C191): list[dict] (aninhado em C100)
        - observacoes_c195 (C195): list[dict] (aninhado em C100)
        - ajustes_c197 (C197): list[dict] (aninhado em C100)
        - resumos_c350 (C350): list[dict] com "itens" (C370) e "analiticos" (C380/C390)
        - ecf (C400): list[dict] com "reducoes" (C405) que possuem "totais" (C410/C420)
        - documentos_ecf (C460): list[dict] com "itens" (C470), "resumos" (C480) e "analiticos" (C490)
        - servicos (C500): list[dict] com "analiticos" (C590/C591), "observacoes" (C595) e "ajustes" (C597)
        - consolidacoes (C700): list[dict] com "analiticos" (C790) e "complementos" (C791)
        - cfe (C800): list[dict] com "itens" (C810), "detalhes" (C815) e "analiticos" (C850)
        - fechamento_bloco_c (C990): dict
        - abertura_bloco_d (D001): dict
        - complementos_d130 (D130/D140/D150/D160/D161/D162/D170/D180): list[dict] (aninhado em D100 quando aplicável)
        - analiticos_d190 (D190): list[dict] (aninhado em D100)
        - observacoes_d195 (D195): list[dict] (aninhado em D100)
        - ajustes_d197 (D197): list[dict] (aninhado em D100)
        - bilhetes (D300): list[dict] com "cancelados" (D301) e "municipios" (D310)
        - ecf_d350 (D350): list[dict] com "reducoes" (D355)
        - bpe (D360): list[dict] com "itens" (D365) e "ecf_detalhe" (D370)
        - bpe_simplificado (D390): list[dict]
        - resumo_transporte (D400): list[dict] com "documentos" (D410) que têm "cancelados" (D411) e "analiticos" (D420)
        - telecom (D500): list[dict] com "itens" (D510) e "equipamentos" (D530); resumo_mensal (D590)
        - energia_comunicacao_resumo (D695): list[dict] com "itens" (D696) e "icms_outra_uf" (D697)
        - gas (D700): list[dict] com "itens" (D730), "st" (D731), "ajustes" (D737)
        - gas_resumo_clas (D735): list[dict]
        - gas_icms_outra_uf (D750): list[dict]
        - gas_resumo_mensal (D760): list[dict]
        - gas_resumo_st (D761): list[dict]
        - transportes (D100): list[dict] com "pis" (D101) e "cofins" (D105)
        - transportes_resumo (D200): list[dict] com "pis" (D201) e "cofins" (D205)
        - contadores: dict
    """


    # ------------------------
    # Helpers
    # ------------------------
    def to_decimal_br(x):
        s = ("" if x is None else str(x)).strip()
        if not s:
            return None
        s = s.replace(".", "").replace(",", ".")  # 1.234,56 -> 1234.56
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            return None

    def parse_line(line: str):
        # Remove BOM e quebra; aceita linhas com pipe inicial/final
        raw = line.strip().lstrip("\ufeff")
        if not raw:
            return None
        if "|" not in raw:
            return None
        parts = raw.split("|")
        # Se começa/termina com '|', teremos strings vazias; removemos apenas vazios laterais
        while parts and parts[0] == "":
            parts.pop(0)
        while parts and parts[-1] == "":
            parts.pop()
        if not parts:
            return None
        reg = parts[0].strip()
        if not reg:
            return None
        return reg, parts

    # ------------------------
    # Layouts (campos na ordem)
    # ------------------------
    LAYOUT_0000 = [
        "REG",
        "COD_VER",
        "COD_FIN",
        "DT_INI",
        "DT_FIN",
        "NOME",
        "CNPJ",
        "CPF",
        "UF",
        "IE",
        "COD_MUN",
        "IM",
        "SUFRAMA",
        "IND_PERFIL",
        "IND_ATIV",
    ]

    LAYOUT_0001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_0002 = [
        "REG",
        "CLAS_ESTAB_IND",
    ]

    LAYOUT_0005 = [
        "REG",
        "FANTASIA",
        "CEP",
        "END",
        "NUM",
        "COMPL",
        "BAIRRO",
        "FONE",
        "FAX",
        "EMAIL",
    ]

    LAYOUT_0015 = [
        "REG",
        "UF_ST",
        "IE_ST",
    ]

    LAYOUT_0100 = [
        "REG",
        "NOME",
        "CPF",
        "CRC",
        "CNPJ",
        "CEP",
        "END",
        "NUM",
        "COMPL",
        "BAIRRO",
        "FONE",
        "FAX",
        "EMAIL",
        "COD_MUN",
    ]

    LAYOUT_0150 = [
        "REG", "COD_PART", "NOME", "COD_PAIS", "CNPJ", "CPF", "IE", "COD_MUN",
        "SUFRAMA", "END", "NUM", "COMPL", "BAIRRO"
    ]

    LAYOUT_0175 = [
        "REG",
        "DT_ALT",
        "NR_CAMPO",
        "CONT_ANT",
    ]

    LAYOUT_0190 = [
        "REG",
        "UNID",
        "DESCR",
    ]

    LAYOUT_0200 = [
        "REG", "COD_ITEM", "DESCR_ITEM", "COD_BARRA", "COD_ANT_ITEM", "UNID_INV",
        "TIPO_ITEM", "COD_NCM", "EX_IPI", "COD_GEN", "COD_LST", "ALIQ_ICMS", "CEST"
    ]

    LAYOUT_0220 = [
        "REG",
        "UNID_CONV",
        "FAT_CONV",
    ]

    LAYOUT_0300 = [
        "REG",
        "COD_IND_BEM",
        "IDENT_MERC",
        "DESCR_ITEM",
        "COD_PRNC",
        "COD_CTA",
    ]

    LAYOUT_0305 = [
        "REG",
        "COD_CCUS",
        "FUNC",
        "VIDA_UTIL",
    ]

    LAYOUT_0400 = [
        "REG",
        "COD_NAT",
        "DESCR_NAT",
    ]

    LAYOUT_0450 = [
        "REG",
        "COD_INF",
        "TXT",
    ]

    LAYOUT_0460 = [
        "REG",
        "COD_OBS",
        "TXT",
    ]

    LAYOUT_0500 = [
        "REG",
        "DT_ALT",
        "COD_NAT_CC",
        "IND_CTA",
        "NIVEL",
        "COD_CTA",
        "NOME_CTA",
    ]

    LAYOUT_0600 = [
        "REG",
        "DT_ALT",
        "COD_CCUS",
        "CCUS",
    ]

    LAYOUT_0990 = [
        "REG",
        "QTD_LIN_0",
    ]

    LAYOUT_B001 = [
        "REG",
        "IND_DAD",
    ]

    LAYOUT_B990 = [
        "REG",
        "QTD_LIN_B",
    ]

    LAYOUT_C001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_C100 = [
        "REG","IND_OPER","IND_EMIT","COD_PART","COD_MOD","COD_SIT","SER","NUM_DOC","CHV_NFE",
        "DT_DOC","DT_E_S","VL_DOC","IND_PGTO","VL_DESC","VL_ABAT_NT","VL_MERC","IND_FRT",
        "VL_FRT","VL_SEG","VL_OUT_DA","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST",
        "VL_IPI","VL_PIS","VL_COFINS","VL_PIS_ST","VL_COFINS_ST"
    ]

    LAYOUT_C101 = [
        "REG",
        "VL_FCP_UF_DEST",
        "VL_ICMS_UF_DEST",
        "VL_ICMS_UF_REM",
    ]

    LAYOUT_C105 = [
        "REG",
        "OPER",
        "UF",
    ]

    LAYOUT_C110 = [
        "REG",
        "COD_INF",
        "TXT_COMPL",
    ]

    LAYOUT_C111 = [
        "REG",
        "NUM_PROC",
        "IND_PROC",
    ]

    LAYOUT_C112 = [
        "REG",
        "COD_DA",
        "UF",
        "NUM_DA",
        "COD_AUT",
        "VL_DA",
        "DT_VCTO",
        "DT_PGTO",
    ]

    LAYOUT_C113 = [
        "REG",
        "IND_OPER",
        "IND_EMIT",
        "COD_PART",
        "COD_MOD",
        "SER",
        "SUB",
        "NUM_DOC",
        "DT_DOC",
        "CHV_DOCe",
    ]

    LAYOUT_C114 = [
        "REG",
        "COD_MOD",
        "ECF_FAB",
        "ECF_CX",
        "NUM_DOC",
        "DT_DOC",
    ]

    LAYOUT_C116 = [
        "REG",
        "COD_MOD",
        "NR_SAT_OU_IDENT",
        "CHV_DOCe",
        "NUM_DOC",
        "DT_DOC",
    ]

    LAYOUT_C120 = [
        "REG",
        "COD_DOC_IMP",
        "NUM_DOC_IMP",
        "PIS_IMP",
        "COFINS_IMP",
        "OUTROS_1",
        "OUTROS_2",
    ]

    LAYOUT_C176 = [
        "REG",
        "COD_MOD_ULT_E",
        "NUM_DOC_ULT_E",
        "SER_ULT_E",
        "DT_ULT_E",
        "COD_PART_ULT_E",
        "QUANT_ULT_E",
        "VL_UNIT_ULT_E",
        "VL_UNIT_BC_ST",
        "CHV_NFE_ULT_E",
        "NUM_ITEM_ULT_E",
        "VL_UNIT_BC_ICMS_ULT_E",
        "ALIQ_ICMS_ULT_E",
        "VL_UNIT_LIMITE_BC_ICMS_ULT_E",
        "VL_UNIT_ICMS_ULT_E",
        "ALIQ_ST_ULT_E",
        "VL_UNIT_RES",
        "COD_RESP_RET",
        "COD_MOT_RES",
        "CHAVE_NFE_RET",
        "COD_PART_NFE_RET",
        "SER_NFE_RET",
        "NUM_NFE_RET",
        "ITEM_NFE_RET",
        "COD_DA",
        "NUM_DA",
        "VL_UNIT_RES_FCP_ST",
    ]

    LAYOUT_C177 = [
        "REG",
        "CAMPO_01",
    ]

    LAYOUT_C185 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "COD_ITEM",
        "COD_NCM",
        "VL_UNIT_ICMS_NA_OPERACAO_CONV",
        "VL_UNIT_ICMS_OP_CONV",
        "VL_UNIT_ICMS_OP_ESTOQUE_CONV",
        "VL_UNIT_ICMS_ST_ESTOQUE_CONV",
        "VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV",
        "VL_UNIT_ICMS_ST_CONV_REST",
        "VL_UNIT_FCP_ST_CONV_REST",
        "VL_UNIT_ICMS_ST_CONV_COMPL",
        "VL_UNIT_FCP_ST_CONV_COMPL",
    ]

    LAYOUT_C186 = [
        "REG",
        "NUM_DOC",
        "COD_MOD",
        "SER",
        "DT_DOC",
        "COD_ITEM",
        "VL_UNIT_ICMS_OP_CONV",
        "VL_UNIT_ICMS_OP_ESTOQUE_CONV",
        "VL_UNIT_ICMS_ST_ESTOQUE_CONV",
        "VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV",
        "CHV_NFE",
    ]

    LAYOUT_C190 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
        "VL_RED_BC",
        "VL_IPI",
        "COD_OBS",
    ]

    LAYOUT_C191 = [
        "REG",
        "VL_FCP_OP",
        "VL_FCP_ST",
        "VL_FCP_RET",
    ]

    LAYOUT_C195 = [
        "REG",
        "COD_OBS",
        "TXT_COMPL",
    ]

    LAYOUT_C197 = [
        "REG",
        "COD_AJ",
        "DESCR_COMPL_AJ",
        "COD_ITEM",
        "VL_BC_ICMS",
        "ALIQ_ICMS",
        "VL_ICMS",
        "VL_OUTROS",
    ]

    LAYOUT_C350 = [
        "REG",
        "SER",
        "SUB_SER",
        "NUM_DOC",
        "DT_DOC",
        "CNPJ_CPF",
        "VL_MERC",
        "VL_DOC",
        "VL_PIS",
        "VL_COFINS",
        "COD_CTA",
    ]

    LAYOUT_C370 = [
        "REG",
        "NUM_ITEM",
        "COD_ITEM",
        "QTD",
        "UNID",
        "VL_ITEM",
        "VL_DESC",
    ]

    LAYOUT_C380 = [
        "REG",
        "COD_ITEM",
        "VL_UNIT",
        "QUANT",
        "VL_DOC",
        "VL_DESC",
        "VL_PIS",
        "VL_COFINS",
        "COD_CTA",
    ]

    LAYOUT_C390 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_RED_BC",
        "COD_OBS",
    ]

    LAYOUT_C400 = [
        "REG",
        "COD_MOD",
        "ECF_MOD",
        "ECF_FAB",
        "ECF_CX",
    ]

    LAYOUT_C405 = [
        "REG",
        "DT_DOC",
        "CRO",
        "CRZ",
        "NUM_COO_FIN",
        "GT_FIN",
        "VL_BRT",
    ]

    LAYOUT_C410 = [
        "REG",
        "VL_PIS",
        "VL_COFINS",
    ]

    LAYOUT_C420 = [
        "REG",
        "COD_TOT_PAR",
        "VLR_ACUM_TOT",
        "NR_TOT",
        "DESCR_NR_TOT",
    ]

    LAYOUT_C460 = [
        "REG",
        "COD_MOD",
        "COD_SIT",
        "NUM_DOC",
        "DT_DOC",
        "VL_DOC",
        "VL_PIS",
        "VL_COFINS",
        "CPF_CNPJ",
        "NOM_ADQ",
    ]

    LAYOUT_C470 = [
        "REG",
        "COD_ITEM",
        "QTD",
        "QTD_CANC",
        "UNID",
        "VL_ITEM",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_BC_ICMS",
        "VL_ICMS",
        "COD_OBS",
    ]

    LAYOUT_C480 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "COD_OBS",
    ]

    LAYOUT_C490 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_RED_BC",
        "COD_OBS",
    ]

    LAYOUT_C500 = [
        "REG","IND_OPER","IND_EMIT","COD_PART","COD_MOD","COD_SIT","SER","SUB","NUM_DOC",
        "DT_DOC","DT_E_S","VL_DOC","VL_DESC","VL_FORN","VL_SERV_NT","VL_TERC","VL_DA",
        "VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST","COD_INF","VL_PIS","VL_COFINS",
    ]

    LAYOUT_C590 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
        "VL_RED_BC",
        "COD_OBS",
    ]

    LAYOUT_C591 = [
        "REG",
        "VL_FCP_OP",
        "VL_FCP_ST",
        "VL_FCP_RET",
    ]

    LAYOUT_C595 = [
        "REG",
        "COD_OBS",
        "TXT_COMPL",
    ]

    LAYOUT_C597 = [
        "REG",
        "COD_AJ",
        "DESCR_COMPL_AJ",
        "VL_BC_ICMS",
        "ALIQ_ICMS",
        "VL_ICMS",
        "VL_OUTROS",
    ]

    LAYOUT_C700 = [
        "REG",
        "COD_MOD",
        "SER",
        "NRO_ORD_INI",
        "NRO_ORD_FIN",
        "DT_DOC_INI",
        "DT_DOC_FIN",
        "VL_DOC",
        "VL_DESC",
    ]

    LAYOUT_C790 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
        "VL_RED_BC",
        "COD_OBS",
    ]

    LAYOUT_C791 = [
        "REG",
        "UF",
        "VL_FCP",
        "VL_ICMS",
    ]

    LAYOUT_C800 = [
        "REG",
        "COD_MOD",
        "COD_SIT",
        "NUM_CFE",
        "DT_DOC",
        "VL_CFE",
        "VL_PIS",
        "VL_COFINS",
        "CHV_CFE",
        "CPF_CNPJ",
        "NOM_ADQ",
    ]

    LAYOUT_C810 = [
        "REG",
        "CFOP",
        "VL_OPR",
        "VL_DESC",
        "CST_ICMS",
        "VL_BC_ICMS",
        "ALIQ_ICMS",
        "VL_ICMS",
        "COD_OBS",
    ]

    LAYOUT_C815 = [
        "REG",
        "CST_PIS",
        "VL_BC_PIS",
        "ALIQ_PIS",
        "VL_PIS",
        "CST_COFINS",
        "VL_BC_COFINS",
        "ALIQ_COFINS",
        "VL_COFINS",
    ]

    LAYOUT_C850 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "COD_OBS",
    ]

    LAYOUT_C990 = [
        "REG",
        "QTD_LIN_C",
    ]

    LAYOUT_D001 = [
        "REG",
        "IND_MOV",
    ]

    # Campos genéricos para complementos do bloco D (posicionais)
    GENERIC_D_FIELDS = [
        "CAMPO_01","CAMPO_02","CAMPO_03","CAMPO_04","CAMPO_05","CAMPO_06","CAMPO_07","CAMPO_08","CAMPO_09","CAMPO_10",
        "CAMPO_11","CAMPO_12","CAMPO_13","CAMPO_14","CAMPO_15","CAMPO_16","CAMPO_17","CAMPO_18","CAMPO_19","CAMPO_20",
    ]

    LAYOUT_D130 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D140 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D150 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D160 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D161 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D162 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D170 = ["REG", *GENERIC_D_FIELDS]
    LAYOUT_D180 = ["REG", *GENERIC_D_FIELDS]

    LAYOUT_D190 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_RED_BC",
        "COD_OBS",
    ]

    LAYOUT_D195 = [
        "REG",
        "COD_OBS",
        "TXT_COMPL",
    ]

    LAYOUT_D197 = [
        "REG",
        "COD_AJ",
        "DESCR_COMPL_AJ",
        "COD_ITEM",
        "VL_BC_ICMS",
        "ALIQ_ICMS",
        "VL_ICMS",
        "VL_OUTROS",
    ]

    LAYOUT_D300 = [
        "REG",
        "COD_MOD",
        "SER",
        "SUB",
        "NUM_DOC_INI",
        "NUM_DOC_FIN",
        "DT_DOC",
        "VL_DOC",
        "VL_ICMS",
        "CST_ICMS",
        "CFOP",
    ]

    LAYOUT_D301 = [
        "REG",
        "NUM_DOC_CANC",
    ]

    LAYOUT_D310 = [
        "REG",
        "COD_MUN_ORIG",
        "COD_MUN_DEST",
        "VL_DOC",
    ]

    LAYOUT_D350 = [
        "REG",
        "COD_MOD",
        "ECF_MOD",
        "ECF_FAB",
        "ECF_CX",
    ]

    LAYOUT_D355 = [
        "REG",
        "DT_DOC",
        "HR_DOC",
        "COO_INI",
        "COO_FIN",
        "VL_BRT",
    ]

    LAYOUT_D360 = [
        "REG",
        "COD_MOD",
        "CHV_DOC",
        "VL_DOC",
        "VL_ICMS",
        "CST_ICMS",
        "CFOP",
    ]

    LAYOUT_D365 = [
        "REG",
        "NUM_ITEM",
        "COD_ITEM",
        "VL_ITEM",
    ]

    LAYOUT_D370 = [
        "REG",
        "ECF_FAB",
        "ECF_CX",
    ]

    LAYOUT_D390 = [
        "REG",
        "COD_MOD",
        "NUM_DOC_INI",
        "NUM_DOC_FIN",
        "VL_DOC",
    ]

    LAYOUT_D400 = [
        "REG",
        "COD_PART",
        "COD_MOD",
        "DT_DOC",
        "VL_DOC",
        "VL_SERV",
        "VL_BC_ICMS",
    ]

    LAYOUT_D410 = [
        "REG",
        "COD_MOD",
        "CHV_CTE",
        "NUM_DOC",
        "COD_PART",
        "VL_DOC",
        "VL_ICMS",
    ]

    LAYOUT_D411 = [
        "REG",
        "NUM_DOC_CANC",
    ]

    LAYOUT_D420 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
    ]

    LAYOUT_D500 = [
        "REG","IND_OPER","IND_EMIT","COD_PART","COD_MOD","COD_SIT","SER","SUB","NUM_DOC","CHV_CTE",
        "DT_DOC","DT_E_S","VL_DOC","VL_DESC","VL_SERV","VL_BC_ICMS","VL_ICMS","VL_PIS","VL_COFINS","COD_INF",
    ]

    LAYOUT_D510 = [
        "REG",
        "NUM_ITEM",
        "COD_ITEM",
        "VL_ITEM",
        "CST_ICMS",
        "CFOP",
        "VL_BC_ICMS",
        "ALIQ_ICMS",
    ]

    LAYOUT_D530 = [
        "REG",
        "IND_SERV",
        "DT_INI_SERV",
        "DT_FIN_SERV",
        "PERIODO_FISCAL",
        "QTD_UTIL",
        "COD_AREA",
        "COD_MOD",
    ]

    LAYOUT_D590 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "ALIQ_ICMS",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
    ]

    LAYOUT_D695 = [
        "REG",
        "COD_MOD",
        "SER",
        "SUB",
        "CFOP",
        "VL_OPR",
        "VL_ICMS",
        "DT_E_INI",
        "DT_E_FIN",
    ]

    LAYOUT_D696 = [
        "REG",
        "COD_CLAS",
        "COD_ITEM",
        "QTD",
        "VL_ITEM",
        "VL_BC_ICMS",
    ]

    LAYOUT_D697 = [
        "REG",
        "UF",
        "VL_ICMS",
        "VL_BC_ICMS",
    ]

    LAYOUT_D700 = [
        "REG","IND_OPER","COD_MOD","COD_SIT","SER","SUB","NUM_DOC","DT_DOC","VL_DOC","VL_BC_ICMS",
    ]

    LAYOUT_D730 = [
        "REG",
        "NUM_ITEM",
        "COD_ITEM",
        "VL_ITEM",
        "CST_ICMS",
        "QTD",
        "UNID",
    ]

    LAYOUT_D731 = [
        "REG",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
    ]

    LAYOUT_D735 = [
        "REG",
        "COD_CLAS",
        "VL_FORN",
        "VL_BC_ICMS",
        "VL_ICMS",
    ]

    LAYOUT_D737 = [
        "REG",
        "COD_AJ",
        "VL_AJ",
        "DESCR_COMPL",
    ]

    LAYOUT_D750 = [
        "REG",
        "UF",
        "VL_ICMS",
    ]

    LAYOUT_D760 = [
        "REG",
        "CST_ICMS",
        "CFOP",
        "VL_OPR",
        "VL_BC_ICMS",
        "VL_ICMS",
    ]

    LAYOUT_D761 = [
        "REG",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
    ]

    LAYOUT_D990 = [
        "REG",
        "QTD_LIN_D",
    ]

    LAYOUT_E001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_E100 = [
        "REG",
        "DT_INI",
        "DT_FIN",
    ]

    LAYOUT_E110 = [
        "REG",
        "VL_SLD_CRED_ANT",
        "VL_TOT_DEB",
        "VL_AJUS_DEB",
        "VL_TOT_CRED",
        "VL_AJUS_CRED",
        "VL_SLD_DEVEDOR",
        "VL_DED",
        "VL_RECOL",
    ]

    LAYOUT_E111 = [
        "REG",
        "COD_AJ_APUR",
        "DESCR_COMPL_AJ",
        "VL_AJ_APUR",
    ]

    LAYOUT_E112 = [
        "REG",
        "NUM_DA",
        "NUM_PROC",
        "IND_PROC",
        "DT_VENCTO",
        "VL_TOT_CHAM",
    ]

    LAYOUT_E113 = [
        "REG",
        "COD_PART",
        "COD_MOD",
        "NUM_DOC",
        "CHV_NFE",
        "VL_DA",
    ]

    LAYOUT_E115 = [
        "REG",
        "COD_INF_ADIC",
        "VL_INF_ADIC",
        "DESCR_COMPL_AJ",
    ]

    LAYOUT_E116 = [
        "REG",
        "COD_OR",
        "VL_OR",
        "DT_VCTO",
        "COD_REC",
        "NUM_PROC",
    ]

    LAYOUT_E200 = [
        "REG",
        "UF",
        "DT_INI",
        "DT_FIN",
    ]

    LAYOUT_E210 = [
        "REG",
        "IND_MOV",
        "VL_SLD_CRED_ANT_ST",
        "VL_TOT_DEB_ST",
        "VL_SLD_DEV_ST",
    ]

    LAYOUT_E220 = [
        "REG",
        "COD_AJ_APUR",
        "VL_AJ_APUR",
    ]

    LAYOUT_E230 = [
        "REG",
        "CHV_NFE",
        "NUM_DOC",
        "VL_DA",
    ]

    LAYOUT_E250 = [
        "REG",
        "COD_OR",
        "VL_OR",
        "DT_VCTO",
        "NUM_DA",
    ]

    LAYOUT_E300 = [
        "REG",
        "UF",
        "DT_INI",
    ]

    LAYOUT_E310 = [
        "REG",
        "VL_SLD_DEV",
        "VL_TOT_DEB",
    ]

    LAYOUT_E311 = [
        "REG",
        "COD_AJ_APUR",
        "VL_AJ_APUR",
    ]

    LAYOUT_E312 = [
        "REG",
        "NUM_DA",
        "VL_TOT_CHAM",
    ]

    LAYOUT_E313 = [
        "REG",
        "CHV_NFE",
        "NUM_DOC",
    ]

    LAYOUT_E316 = [
        "REG",
        "COD_OR",
        "VL_OR",
    ]

    LAYOUT_E500 = [
        "REG",
        "IND_APUR",
        "DT_INI",
        "VL_SLD_CRED_ANT",
    ]

    LAYOUT_E510 = [
        "REG",
        "CFOP",
        "CST_IPI",
        "VL_CONT_IPI",
        "VL_BC_IPI",
        "VL_IPI",
    ]

    LAYOUT_E520 = [
        "REG",
        "VL_SDO_CRED_ANT",
        "VL_DEB_TOTAL",
        "VL_CRED_TOTAL",
        "VL_SDO_DEVEDOR",
        "VL_RECOL",
    ]

    LAYOUT_E530 = [
        "REG",
        "IND_AJ",
        "VL_AJ",
        "COD_AJ",
        "CHV_DOC",
    ]

    LAYOUT_E531 = [
        "REG",
        "COD_REC",
        "VL_OR",
        "DT_VCTO",
        "NUM_PROC",
    ]

    LAYOUT_E990 = [
        "REG",
        "QTD_LIN_E",
    ]

    LAYOUT_G001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_G110 = [
        "REG",
        "DT_INI",
        "DT_FIN",
        "SLD_ICMS_ANT",
        "VL_ENTRADA",
        "VL_CRED_TOT",
        "VL_CRED_PER",
    ]

    LAYOUT_G125 = [
        "REG",
        "COD_IND_BEM",
        "DT_MOV",
        "TIPO_MOV",
        "VL_OPR_AQUIS",
        "VL_ICMS_OPR",
    ]

    LAYOUT_G126 = [
        "REG",
        "COD_IND_BEM",
        "DT_INI_AP",
        "NUM_PARC",
        "VL_PARC_PASS",
    ]

    LAYOUT_G130 = [
        "REG",
        "IND_EMIT",
        "COD_PART",
        "COD_MOD",
        "NUM_DOC",
        "CHV_NFE",
    ]

    LAYOUT_G140 = [
        "REG",
        "COD_ITEM",
        "VL_ICMS_TOT",
        "VL_ICMS_UTIL",
    ]

    LAYOUT_G990 = [
        "REG",
        "QTD_LIN_G",
    ]

    LAYOUT_H001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_H005 = [
        "REG",
        "DT_INV",
        "VL_INV",
        "MOTIVO",
    ]

    LAYOUT_H010 = [
        "REG",
        "COD_ITEM",
        "UNID",
        "QTD",
        "VL_UNIT",
        "VL_ITEM",
        "IND_PROP",
        "COD_PART",
        "CST_ICMS",
    ]

    LAYOUT_H020 = [
        "REG",
        "CST_ICMS",
        "VL_BC_ICMS",
        "VL_ICMS",
        "VL_BC_ICMS_ST",
        "VL_ICMS_ST",
    ]

    LAYOUT_H030 = [
        "REG",
        "IND_BEM",
        "QTD_BEM",
        "DT_REF",
    ]

    LAYOUT_H990 = [
        "REG",
        "QTD_LIN_H",
    ]

    LAYOUT_K001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_K100 = [
        "REG",
        "DT_INI",
        "DT_FIN",
    ]

    LAYOUT_K200 = [
        "REG",
        "DT_EST",
        "COD_ITEM",
        "QTD",
        "IND_EST",
        "COD_PART",
    ]

    LAYOUT_K210 = [
        "REG",
        "DT_INI_OS",
        "DT_FIN_OS",
        "COD_DOC_OS",
        "COD_ITEM_ORI",
        "QTD_ORI",
    ]

    LAYOUT_K215 = [
        "REG",
        "COD_ITEM_DEST",
        "QTD_DEST",
    ]

    LAYOUT_K220 = [
        "REG",
        "DT_MOV",
        "COD_ITEM_ORI",
        "COD_ITEM_DEST",
        "QTD_ORI",
        "QTD_DEST",
    ]

    LAYOUT_K230 = [
        "REG",
        "DT_INI_OP",
        "DT_FIN_OP",
        "COD_DOC_OP",
        "COD_ITEM",
        "QTD_ENC",
    ]

    LAYOUT_K235 = [
        "REG",
        "DT_SAIDA",
        "COD_ITEM",
        "QTD",
        "COD_INS_SUBST",
    ]

    LAYOUT_K250 = [
        "REG",
        "DT_PROD",
        "COD_ITEM",
        "QTD",
    ]

    LAYOUT_K255 = [
        "REG",
        "DT_CONS",
        "COD_ITEM",
        "QTD",
        "COD_INS_SUBST",
    ]

    LAYOUT_K260 = [
        "REG",
        "COD_OP_OS",
        "COD_ITEM",
        "DT_SAIDA",
        "QTD_SAIDA",
        "DT_RET",
        "QTD_RET",
    ]

    LAYOUT_K265 = [
        "REG",
        "COD_ITEM",
        "QTD_CONS",
        "QTD_RET",
        "COD_INS_SUBST",
    ]

    LAYOUT_K270 = [
        "REG",
        "DT_INI_OP",
        "DT_FIN_OP",
        "COD_OP_OS",
        "COD_ITEM",
        "QTD_COR_POS",
        "QTD_COR_NEG",
        "ORIGEM",
    ]

    LAYOUT_K275 = [
        "REG",
        "COD_ITEM",
        "QTD_COR_POS",
        "QTD_COR_NEG",
        "COD_INS_SUBST",
    ]

    LAYOUT_K280 = [
        "REG",
        "DT_EST",
        "COD_ITEM",
        "QTD_COR_POS",
        "QTD_COR_NEG",
        "IND_EST",
        "COD_PART",
    ]

    LAYOUT_K290 = [
        "REG",
        "DT_INI_OP",
        "DT_FIN_OP",
        "COD_DOC_OP",
        "COD_ITEM",
    ]

    LAYOUT_K291 = [
        "REG",
        "COD_ITEM",
        "QTD",
    ]

    LAYOUT_K292 = [
        "REG",
        "COD_ITEM",
        "QTD",
    ]

    LAYOUT_K300 = [
        "REG",
        "DT_PROD",
    ]

    LAYOUT_K301 = [
        "REG",
        "COD_ITEM",
        "QTD",
    ]

    LAYOUT_K302 = [
        "REG",
        "COD_ITEM",
        "QTD",
    ]

    LAYOUT_K990 = [
        "REG",
        "QTD_LIN_K",
    ]

    LAYOUT_1001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_1010 = [
        "REG",
        "IND_EXP","IND_CCRF","IND_COMB","IND_USINA","IND_VA","IND_EE","IND_CART","IND_FORM","IND_AER","IND_GIAF",
    ]

    LAYOUT_1100 = [
        "REG",
        "IND_DOC",
        "NRO_DE",
        "DT_DE",
        "NAT_EXP",
        "NRO_RE",
        "DT_RE",
        "CHC_EMB",
        "DT_CHC",
        "DT_AVB",
        "TP_CHC",
        "PAIS",
    ]

    LAYOUT_1105 = [
        "REG",
        "COD_MOD",
        "SER",
        "NUM_DOC",
        "CHV_NFE",
        "DT_DOC",
        "COD_ITEM",
    ]

    LAYOUT_1200 = [
        "REG",
        "COD_AJ_APUR",
        "SLD_CRED",
        "CRED_APR",
        "CRED_RECEB",
        "CRED_UTIL",
        "SLD_CRED_FIM",
    ]

    LAYOUT_1210 = [
        "REG",
        "TIPO_UTIL",
        "NR_DOC",
        "VL_CRED_UTIL",
    ]

    LAYOUT_1250 = [
        "REG",
        "VL_SLD_CRED_ANT",
        "VL_TOT_CRED_ENTR",
        "VL_TOT_CRED_UTIL",
        "VL_SLD_CRED_FIM",
    ]

    LAYOUT_1255 = [
        "REG",
        "COD_MOT_REST_COMPL",
        "VL_CRED",
        "VL_CRED_UTIL",
    ]

    LAYOUT_1300 = [
        "REG",
        "COD_ITEM",
        "DT_FECH",
        "ESTQ_ABERT",
        "VOL_ENTR",
        "VOL_DISP",
        "VOL_SAID",
        "ESTQ_ESCR",
        "VAL_AJ_PERDA",
        "VAL_AJ_GANHO",
        "FECH_FISICO",
    ]

    LAYOUT_1310 = [
        "REG",
        "NUM_TANQUE",
        "ESTQ_ABERT",
        "VOL_ENTR",
        "VOL_DISP",
        "VOL_SAID",
        "ESTQ_ESCR",
        "VAL_AJ_PERDA",
        "VAL_AJ_GANHO",
        "FECH_FISICO",
    ]

    LAYOUT_1320 = [
        "REG",
        "NUM_BICO",
        "NR_INTERV",
        "MOT_INTERV",
        "NOM_INTERV",
        "CNPJ_INTERV",
        "CPF_INTERV",
        "VAL_FECHA",
        "VAL_ABERT",
        "VOL_AFERI",
        "VOL_VENDAS",
    ]

    LAYOUT_1390 = [
        "REG",
        "COD_PROD",
        "VOL_INI",
        "VOL_PROD",
        "VOL_ENTR",
        "VOL_SAID",
        "VOL_FIN",
        "EST_ESCR",
    ]

    LAYOUT_1391 = [
        "REG",
        "DT_REGISTRO",
        "COD_ITEM",
        "QTD",
        "TP_RESIDUO",
        "QTD_RESIDUO",
    ]

    LAYOUT_1400 = [
        "REG",
        "COD_ITEM_IPM",
        "MUN",
        "VALOR",
    ]

    LAYOUT_1500 = [
        "REG","IND_OPER","COD_PART","COD_MOD","COD_SIT","SER","SUB","COD_CONS","NUM_DOC","DT_DOC","DT_E_S",
        "VL_DOC","VL_DESC","VL_FORN","VL_SERV_NT","VL_TERC","VL_DA","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST",
    ]

    LAYOUT_1510 = [
        "REG","NUM_ITEM","COD_ITEM","COD_CLASS","QTD","UNID","VL_ITEM","VL_DESC","CST_ICMS","CFOP","VL_BC_ICMS","ALIQ_ICMS",
        "VL_ICMS","VL_BC_ICMS_ST","ALIQ_ST","VL_ICMS_ST","IND_REC","COD_PART","VL_PIS","VL_COFINS","COD_CTA",
    ]

    LAYOUT_1601 = [
        "REG",
        "COD_PART_IP",
        "TOT_VS",
        "TOT_ISS",
        "TOT_OUTROS",
    ]

    LAYOUT_1700 = [
        "REG",
        "COD_DISP",
        "COD_MOD",
        "SER",
        "SUB",
        "NUM_DOC_INI",
        "NUM_DOC_FIN",
        "NUM_AUT",
    ]

    LAYOUT_1710 = [
        "REG",
        "NUM_DOC_INI",
        "NUM_DOC_FIN",
    ]

    LAYOUT_1800 = [
        "REG",
        "VL_CARGA",
        "VL_PASS",
        "VL_FAT",
        "IND_RAT",
        "VL_ICMS_ANT",
        "VL_BC_ICMS",
        "VL_ICMS_APUR",
        "VL_BC_ICMS_APUR",
        "VL_DIF",
    ]

    LAYOUT_1900 = [
        "REG",
        "IND_APUR_ICMS",
        "DESCR_COMPL_OUT_APUR",
    ]

    LAYOUT_1910 = [
        "REG",
        "DT_INI",
        "DT_FIN",
    ]

    LAYOUT_1920 = [
        "REG",
        "VL_TOT_TRANSF_DEBITOS_OA",
        "VL_TOT_AJ_DEBITOS_OA",
        "VL_TOT_AJ_CREDITOS_OA",
        "VL_TOT_TRANSF_CREDITOS_OA",
        "VL_SLD_CRED_ANT_OA",
        "VL_SLD_APUR_OA",
        "VL_SLD_CRED_TRANSPORTAR_OA",
        "DEB_ESP_OA",
    ]

    LAYOUT_1921 = [
        "REG",
        "COD_AJ_APUR",
        "DESCR_COMPL_AJ",
        "VL_AJ_APUR",
    ]

    LAYOUT_1922 = [
        "REG",
        "NUM_DA",
        "COD_OR",
        "VL_OR",
        "DT_VCTO",
        "COD_REC",
    ]

    LAYOUT_9001 = [
        "REG",
        "IND_MOV",
    ]

    LAYOUT_9900 = [
        "REG",
        "REG_BLC",
        "QTD_REG_BLC",
    ]

    LAYOUT_9990 = [
        "REG",
        "QTD_LIN_9",
    ]

    LAYOUT_9999 = [
        "REG",
        "QTD_LIN",
    ]

    LAYOUT_C170 = [
        "REG","NUM_ITEM","COD_ITEM","DESCR_COMPL","QTD","UNID","VL_ITEM","VL_DESC","IND_MOV",
        "CST_ICMS","CFOP","COD_NAT","VL_BC_ICMS","ALIQ_ICMS","VL_ICMS","VL_BC_ICMS_ST","ALIQ_ST",
        "VL_ICMS_ST","IND_APUR","CST_IPI","COD_ENQ","VL_BC_IPI","ALIQ_IPI","VL_IPI",
        "CST_PIS","VL_BC_PIS","ALIQ_PIS","QUANT_BC_PIS","ALIQ_PIS_R","VL_PIS",
        "CST_COFINS","VL_BC_COFINS","ALIQ_COFINS","QUANT_BC_COFINS","ALIQ_COFINS_R","VL_COFINS",
        "COD_CTA"
    ]

    LAYOUT_D100 = [
        "REG","IND_OPER","IND_EMIT","COD_PART","COD_MOD","COD_SIT","SER","SUB","NUM_DOC","CHV_CTE",
        "DT_DOC","DT_A_P","TP_CTE","CHV_CTE_REF","VL_DOC","VL_DESC","IND_FRT","VL_SERV","VL_BC_ICMS",
        "VL_ICMS","VL_NT","COD_INF","COD_CTA"
    ]

    LAYOUT_D101 = ["REG","IND_NAT_FRT","VL_ITEM","CST_PIS","NAT_BC_CRED","VL_BC_PIS","ALIQ_PIS","VL_PIS","COD_CTA"]
    LAYOUT_D105 = ["REG","IND_NAT_FRT","VL_ITEM","CST_COFINS","NAT_BC_CRED","VL_BC_COFINS","ALIQ_COFINS","VL_COFINS","COD_CTA"]

    LAYOUT_D200 = ["REG","COD_MOD","COD_SIT","SER","SUB","NUM_DOC_INI","NUM_DOC_FIN","CFOP","DT_REF","VL_DOC","VL_DESC"]
    LAYOUT_D201 = ["REG","CST_PIS","VL_ITEM","VL_BC_PIS","ALIQ_PIS","VL_PIS","COD_CTA"]
    LAYOUT_D205 = ["REG","CST_COFINS","VL_ITEM","VL_BC_COFINS","ALIQ_COFINS","VL_COFINS","COD_CTA"]

    LAYOUTS = {
        "0000": LAYOUT_0000,
        "0001": LAYOUT_0001,
        "0002": LAYOUT_0002,
        "0005": LAYOUT_0005,
        "0015": LAYOUT_0015,
        "0100": LAYOUT_0100,
        "0150": LAYOUT_0150,
        "0175": LAYOUT_0175,
        "0190": LAYOUT_0190,
        "0200": LAYOUT_0200,
        "0220": LAYOUT_0220,
        "0300": LAYOUT_0300,
        "0305": LAYOUT_0305,
        "0400": LAYOUT_0400,
        "0450": LAYOUT_0450,
        "0460": LAYOUT_0460,
        "0500": LAYOUT_0500,
        "0600": LAYOUT_0600,
        "0990": LAYOUT_0990,
        "B001": LAYOUT_B001,
        "B990": LAYOUT_B990,
        "C001": LAYOUT_C001,
        "C100": LAYOUT_C100,
        "C101": LAYOUT_C101,
        "C105": LAYOUT_C105,
        "C110": LAYOUT_C110,
        "C111": LAYOUT_C111,
        "C112": LAYOUT_C112,
        "C113": LAYOUT_C113,
        "C114": LAYOUT_C114,
        "C116": LAYOUT_C116,
        "C120": LAYOUT_C120,
        "C176": LAYOUT_C176,
        "C177": LAYOUT_C177,
        "C185": LAYOUT_C185,
        "C186": LAYOUT_C186,
        "C190": LAYOUT_C190,
        "C191": LAYOUT_C191,
        "C195": LAYOUT_C195,
        "C197": LAYOUT_C197,
        "C350": LAYOUT_C350,
        "C370": LAYOUT_C370,
        "C380": LAYOUT_C380,
        "C390": LAYOUT_C390,
        "C400": LAYOUT_C400,
        "C405": LAYOUT_C405,
        "C410": LAYOUT_C410,
        "C420": LAYOUT_C420,
        "C460": LAYOUT_C460,
        "C470": LAYOUT_C470,
        "C480": LAYOUT_C480,
        "C490": LAYOUT_C490,
        "C500": LAYOUT_C500,
        "C590": LAYOUT_C590,
        "C591": LAYOUT_C591,
        "C595": LAYOUT_C595,
        "C597": LAYOUT_C597,
        "C700": LAYOUT_C700,
        "C790": LAYOUT_C790,
        "C791": LAYOUT_C791,
        "C800": LAYOUT_C800,
        "C810": LAYOUT_C810,
        "C815": LAYOUT_C815,
        "C850": LAYOUT_C850,
        "C990": LAYOUT_C990,
        "D001": LAYOUT_D001,
        "D130": LAYOUT_D130,
        "D140": LAYOUT_D140,
        "D150": LAYOUT_D150,
        "D160": LAYOUT_D160,
        "D161": LAYOUT_D161,
        "D162": LAYOUT_D162,
        "D170": LAYOUT_D170,
        "D180": LAYOUT_D180,
        "D190": LAYOUT_D190,
        "D195": LAYOUT_D195,
        "D197": LAYOUT_D197,
        "D300": LAYOUT_D300,
        "D301": LAYOUT_D301,
        "D310": LAYOUT_D310,
        "D350": LAYOUT_D350,
        "D355": LAYOUT_D355,
        "D360": LAYOUT_D360,
        "D365": LAYOUT_D365,
        "D370": LAYOUT_D370,
        "D390": LAYOUT_D390,
        "D400": LAYOUT_D400,
        "D410": LAYOUT_D410,
        "D411": LAYOUT_D411,
        "D420": LAYOUT_D420,
        "D500": LAYOUT_D500,
        "D510": LAYOUT_D510,
        "D530": LAYOUT_D530,
        "D590": LAYOUT_D590,
        "D695": LAYOUT_D695,
        "D696": LAYOUT_D696,
        "D697": LAYOUT_D697,
        "D700": LAYOUT_D700,
        "D730": LAYOUT_D730,
        "D731": LAYOUT_D731,
        "D735": LAYOUT_D735,
        "D737": LAYOUT_D737,
        "D750": LAYOUT_D750,
        "D760": LAYOUT_D760,
        "D761": LAYOUT_D761,
        "D990": LAYOUT_D990,
        "E001": LAYOUT_E001,
        "E100": LAYOUT_E100,
        "E110": LAYOUT_E110,
        "E111": LAYOUT_E111,
        "E112": LAYOUT_E112,
        "E113": LAYOUT_E113,
        "E115": LAYOUT_E115,
        "E116": LAYOUT_E116,
        "E200": LAYOUT_E200,
        "E210": LAYOUT_E210,
        "E220": LAYOUT_E220,
        "E230": LAYOUT_E230,
        "E250": LAYOUT_E250,
        "E300": LAYOUT_E300,
        "E310": LAYOUT_E310,
        "E311": LAYOUT_E311,
        "E312": LAYOUT_E312,
        "E313": LAYOUT_E313,
        "E316": LAYOUT_E316,
        "E500": LAYOUT_E500,
        "E510": LAYOUT_E510,
        "E520": LAYOUT_E520,
        "E530": LAYOUT_E530,
        "E531": LAYOUT_E531,
        "E990": LAYOUT_E990,
        "G001": LAYOUT_G001,
        "G110": LAYOUT_G110,
        "G125": LAYOUT_G125,
        "G126": LAYOUT_G126,
        "G130": LAYOUT_G130,
        "G140": LAYOUT_G140,
        "G990": LAYOUT_G990,
        "H001": LAYOUT_H001,
        "H005": LAYOUT_H005,
        "H010": LAYOUT_H010,
        "H020": LAYOUT_H020,
        "H030": LAYOUT_H030,
        "H990": LAYOUT_H990,
        "K001": LAYOUT_K001,
        "K100": LAYOUT_K100,
        "K200": LAYOUT_K200,
        "K210": LAYOUT_K210,
        "K215": LAYOUT_K215,
        "K220": LAYOUT_K220,
        "K230": LAYOUT_K230,
        "K235": LAYOUT_K235,
        "K250": LAYOUT_K250,
        "K255": LAYOUT_K255,
        "K260": LAYOUT_K260,
        "K265": LAYOUT_K265,
        "K270": LAYOUT_K270,
        "K275": LAYOUT_K275,
        "K280": LAYOUT_K280,
        "K290": LAYOUT_K290,
        "K291": LAYOUT_K291,
        "K292": LAYOUT_K292,
        "K300": LAYOUT_K300,
        "K301": LAYOUT_K301,
        "K302": LAYOUT_K302,
        "K990": LAYOUT_K990,
        "1001": LAYOUT_1001,
        "1010": LAYOUT_1010,
        "1100": LAYOUT_1100,
        "1105": LAYOUT_1105,
        "1200": LAYOUT_1200,
        "1210": LAYOUT_1210,
        "1250": LAYOUT_1250,
        "1255": LAYOUT_1255,
        "1300": LAYOUT_1300,
        "1310": LAYOUT_1310,
        "1320": LAYOUT_1320,
        "1390": LAYOUT_1390,
        "1391": LAYOUT_1391,
        "1400": LAYOUT_1400,
        "1500": LAYOUT_1500,
        "1510": LAYOUT_1510,
        "1601": LAYOUT_1601,
        "1700": LAYOUT_1700,
        "1710": LAYOUT_1710,
        "1800": LAYOUT_1800,
        "1900": LAYOUT_1900,
        "1910": LAYOUT_1910,
        "1920": LAYOUT_1920,
        "1921": LAYOUT_1921,
        "1922": LAYOUT_1922,
        "9001": LAYOUT_9001,
        "9900": LAYOUT_9900,
        "9990": LAYOUT_9990,
        "9999": LAYOUT_9999,
        "C170": LAYOUT_C170,
        "D100": LAYOUT_D100,
        "D101": LAYOUT_D101,
        "D105": LAYOUT_D105,
        "D200": LAYOUT_D200,
        "D201": LAYOUT_D201,
        "D205": LAYOUT_D205,
    }

    DECIMAL_FIELDS = {
        # C100
        "VL_DOC","VL_DESC","VL_ABAT_NT","VL_MERC","VL_FRT","VL_SEG","VL_OUT_DA","VL_BC_ICMS","VL_ICMS",
        "VL_BC_ICMS_ST","VL_ICMS_ST","VL_IPI","VL_PIS","VL_COFINS","VL_PIS_ST","VL_COFINS_ST",
        # C170
        "QTD","VL_ITEM","VL_DESC","VL_BC_ICMS","ALIQ_ICMS","VL_ICMS","VL_BC_ICMS_ST","ALIQ_ST","VL_ICMS_ST",
        "VL_BC_IPI","ALIQ_IPI","VL_IPI","VL_BC_PIS","ALIQ_PIS","VL_PIS","VL_BC_COFINS","ALIQ_COFINS","VL_COFINS",
        # D100/D200 etc
        "VL_DOC","VL_SERV","VL_BC_ICMS","VL_ICMS","VL_NT",
        "VL_ITEM","VL_BC_PIS","ALIQ_PIS","VL_PIS","VL_BC_COFINS","ALIQ_COFINS","VL_COFINS",
        "VL_DESC",
        # 0220
        "FAT_CONV",
        # 0305
        "VIDA_UTIL",
        # C101
        "VL_FCP_UF_DEST","VL_ICMS_UF_DEST","VL_ICMS_UF_REM",
        # C112
        "VL_DA",
        # C190
        "ALIQ_ICMS","VL_OPR","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST","VL_RED_BC","VL_IPI",
        # C191
        "VL_FCP_OP","VL_FCP_ST","VL_FCP_RET",
        # C197
        "VL_BC_ICMS","VL_ICMS","VL_OUTROS",
        # C370
        "QTD","VL_ITEM","VL_DESC",
        # C390
        "ALIQ_ICMS","VL_OPR","VL_BC_ICMS","VL_ICMS","VL_RED_BC",
        # C405
        "GT_FIN","VL_BRT",
        # C410
        "VL_PIS","VL_COFINS",
        # C420
        "VLR_ACUM_TOT",
        # C460
        "VL_DOC","VL_PIS","VL_COFINS",
        # C470
        "QTD","QTD_CANC","VL_ITEM","ALIQ_ICMS","VL_BC_ICMS","VL_ICMS",
        # C480/C490
        "ALIQ_ICMS","VL_OPR","VL_BC_ICMS","VL_ICMS","VL_RED_BC",
        # C500/C590
        "VL_FORN","VL_SERV_NT","VL_TERC","VL_DA","VL_PIS","VL_COFINS",
        "VL_BC_ICMS_ST","VL_ICMS_ST",
        # C591
        "VL_FCP_OP","VL_FCP_ST","VL_FCP_RET",
        # C597
        "VL_BC_ICMS","VL_ICMS","VL_OUTROS",
        # C700
        "VL_DOC","VL_DESC",
        # C790
        "VL_OPR","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST","VL_RED_BC",
        # C791
        "VL_FCP","VL_ICMS",
        # C800
        "VL_CFE","VL_PIS","VL_COFINS",
        # C810
        "VL_OPR","VL_DESC","VL_BC_ICMS","ALIQ_ICMS","VL_ICMS",
        # C815
        "VL_BC_PIS","ALIQ_PIS","VL_PIS","VL_BC_COFINS","ALIQ_COFINS","VL_COFINS",
        # C850
        "ALIQ_ICMS","VL_OPR","VL_BC_ICMS","VL_ICMS",
        # C590 again ensure
        "VL_BC_ICMS","VL_ICMS",
        # C176
        "QUANT_ULT_E","VL_UNIT_ULT_E","VL_UNIT_BC_ST","VL_UNIT_BC_ICMS_ULT_E","ALIQ_ICMS_ULT_E","VL_UNIT_LIMITE_BC_ICMS_ULT_E","VL_UNIT_ICMS_ULT_E","ALIQ_ST_ULT_E","VL_UNIT_RES","VL_UNIT_RES_FCP_ST",
        # C185
        "VL_UNIT_ICMS_NA_OPERACAO_CONV","VL_UNIT_ICMS_OP_CONV","VL_UNIT_ICMS_OP_ESTOQUE_CONV","VL_UNIT_ICMS_ST_ESTOQUE_CONV","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV","VL_UNIT_ICMS_ST_CONV_REST","VL_UNIT_FCP_ST_CONV_REST","VL_UNIT_ICMS_ST_CONV_COMPL","VL_UNIT_FCP_ST_CONV_COMPL",
        # C186
        "VL_UNIT_ICMS_OP_CONV","VL_UNIT_ICMS_OP_ESTOQUE_CONV","VL_UNIT_ICMS_ST_ESTOQUE_CONV","VL_UNIT_FCP_ICMS_ST_ESTOQUE_CONV",
        # C350
        "VL_MERC","VL_DOC","VL_PIS","VL_COFINS",
        # C380
        "VL_UNIT","QUANT","VL_DOC","VL_DESC","VL_PIS","VL_COFINS",
        # D190
        "ALIQ_ICMS","VL_OPR","VL_BC_ICMS","VL_ICMS","VL_RED_BC",
        # D197
        "VL_BC_ICMS","ALIQ_ICMS","VL_ICMS","VL_OUTROS",
        # D300/D310/D360/D390/D400/D410/D420
        "VL_DOC","VL_ICMS","VL_BRT","VL_SERV",
        # D500/D510/D590
        "VL_BC_ICMS_ST","VL_ICMS_ST","VL_ITEM","ALIQ_ICMS","VL_BC_ICMS","VL_OPR","VL_ICMS",
        "VL_DOC","VL_DESC","VL_SERV","VL_PIS","VL_COFINS",
        # D530
        "QTD_UTIL",
        # D695/D696/D697
        "VL_BC_ICMS","VL_ITEM","QTD",
        # D700/D730/D731/D735/D737/D750/D760/D761
        "VL_BC_ICMS","VL_ITEM","VL_BC_ICMS_ST","VL_ICMS_ST","VL_FORN","VL_AJ","VL_OPR",
        # E110
        "VL_SLD_CRED_ANT","VL_TOT_DEB","VL_AJUS_DEB","VL_TOT_CRED","VL_AJUS_CRED","VL_SLD_DEVEDOR","VL_DED","VL_RECOL",
        # E111/E220/E311
        "VL_AJ_APUR",
        # E112/E312
        "VL_TOT_CHAM",
        # E113
        "VL_DA",
        # E115
        "VL_INF_ADIC",
        # E116/E250/E316
        "VL_OR",
        # E210
        "VL_SLD_CRED_ANT_ST","VL_TOT_DEB_ST","VL_SLD_DEV_ST",
        # E310
        "VL_SLD_DEV","VL_TOT_DEB",
        # E500
        "VL_SLD_CRED_ANT",
        # E510
        "VL_CONT_IPI","VL_BC_IPI","VL_IPI",
        # E520
        "VL_SDO_CRED_ANT","VL_DEB_TOTAL","VL_CRED_TOTAL","VL_SDO_DEVEDOR","VL_RECOL",
        # E530
        "VL_AJ",
        # E531
        "VL_OR",
        # G110
        "SLD_ICMS_ANT","VL_ENTRADA","VL_CRED_TOT","VL_CRED_PER",
        # G125
        "VL_OPR_AQUIS","VL_ICMS_OPR",
        # G126
        "VL_PARC_PASS",
        # G140
        "VL_ICMS_TOT","VL_ICMS_UTIL",
        # H005
        "VL_INV",
        # H010
        "QTD","VL_UNIT","VL_ITEM",
        # H020
        "VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST",
        # H030
        "QTD_BEM",
        # K200
        "QTD",
        # K210/K215/K220
        "QTD_ORI","QTD_DEST",
        # K230
        "QTD_ENC",
        # K235/K250/K255
        "QTD",
        # K260
        "QTD_SAIDA","QTD_RET",
        # K265
        "QTD_CONS",
        # K270/K275/K280
        "QTD_COR_POS","QTD_COR_NEG",
        # K291/K292/K301/K302
        "QTD",
        # 1200/1210/1250/1255
        "SLD_CRED","CRED_APR","CRED_RECEB","CRED_UTIL","SLD_CRED_FIM","VL_CRED_UTIL","VL_CRED","VL_TOT_CRED_ENTR","VL_TOT_CRED_UTIL","VL_SLD_CRED_FIM",
        # 1300/1310/1320
        "ESTQ_ABERT","VOL_ENTR","VOL_DISP","VOL_SAID","ESTQ_ESCR","VAL_AJ_PERDA","VAL_AJ_GANHO","FECH_FISICO",
        "VAL_FECHA","VAL_ABERT","VOL_AFERI","VOL_VENDAS",
        # 1390/1391
        "VOL_INI","VOL_PROD","VOL_ENTR","VOL_SAID","VOL_FIN","EST_ESCR","QTD","QTD_RESIDUO",
        # 1400
        "VALOR",
        # 1500/1510
        "VL_DESC","VL_FORN","VL_SERV_NT","VL_TERC","VL_DA","VL_BC_ICMS","VL_ICMS","VL_BC_ICMS_ST","VL_ICMS_ST","VL_ITEM","ALIQ_ICMS","VL_PIS","VL_COFINS",
        "VL_BC_ICMS_ST","ALIQ_ST","VL_ICMS_ST",
        # 1601
        "TOT_VS","TOT_ISS","TOT_OUTROS",
        # 1700/1710
        "NUM_DOC_INI","NUM_DOC_FIN",
        # 1800
        "VL_CARGA","VL_PASS","VL_FAT","IND_RAT","VL_ICMS_ANT","VL_BC_ICMS","VL_ICMS_APUR","VL_BC_ICMS_APUR","VL_DIF",
        # 1920/1921/1922
        "VL_TOT_TRANSF_DEBITOS_OA","VL_TOT_AJ_DEBITOS_OA","VL_TOT_AJ_CREDITOS_OA","VL_TOT_TRANSF_CREDITOS_OA",
        "VL_SLD_CRED_ANT_OA","VL_SLD_APUR_OA","VL_SLD_CRED_TRANSPORTAR_OA","DEB_ESP_OA","VL_AJ_APUR","VL_OR",
    }

    def build_dict(parts, layout):
        d = {}
        # parts inclui REG na posição 0
        for i, key in enumerate(layout):
            val = parts[i] if i < len(parts) else ""
            val = ("" if val is None else str(val)).strip()

            if key in DECIMAL_FIELDS:
                d[key] = to_decimal_br(val)
            else:
                d[key] = val if val != "" else None
        return d

    # ------------------------
    # Ler conteúdo
    # ------------------------
    if tratar_como_arquivo and os.path.exists(txt_ou_caminho):
        # tenta utf-8; se falhar, cai para latin-1 (comum em SPED)
        try:
            with open(txt_ou_caminho, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(txt_ou_caminho, "r", encoding="latin-1") as f:
                content = f.read()
    else:
        content = txt_ou_caminho

    # ------------------------
    # Parse + estrutura hierárquica
    # ------------------------
    abertura = None
    abertura_bloco0 = None
    classificacoes = []
    dados_complementares = []
    substitutos_uf = []
    contabilistas = []
    participantes = []
    historico_participantes = []
    unidades = []
    conversoes = []
    bens = []
    natureza_operacao = []
    info_complementar = []
    observacoes_lancamento = []
    plano_contas = []
    centros_custos = []
    complementos_c176 = []
    complementos_c177 = []
    complementos_c185 = []
    complementos_c186 = []
    analiticos_c190 = []
    fcp_c191 = []
    observacoes_c195 = []
    ajustes_c197 = []
    resumos_c350 = []
    ecf = []
    documentos_ecf = []
    servicos = []
    consolidacoes = []
    cfe = []
    complementos_d130 = []
    complementos_d140 = []
    complementos_d150 = []
    complementos_d160 = []
    complementos_d161 = []
    complementos_d162 = []
    complementos_d170 = []
    complementos_d180 = []
    analiticos_d190 = []
    observacoes_d195 = []
    ajustes_d197 = []
    bilhetes = []
    ecf_d350 = []
    bpe = []
    bpe_simplificado = []
    resumo_transporte = []
    telecom = []
    telecom_resumo = []
    energia_comunicacao_resumo = []
    gas = []
    gas_resumo_clas = []
    gas_icms_outra_uf = []
    gas_resumo_mensal = []
    gas_resumo_st = []
    abertura_bloco_e = None
    e_periodos_icms = []
    e_apuracoes_icms = []
    e_ajustes_icms = []
    e_obrigacoes_icms = []
    e_info_doc_icms = []
    e_info_adic_icms = []
    e_recolhimentos_icms = []
    e_periodos_st = []
    e_apuracoes_st = []
    e_ajustes_st = []
    e_info_doc_st = []
    e_recolhimentos_st = []
    e_periodos_dif = []
    e_apuracoes_dif = []
    e_ajustes_dif = []
    e_obrigacoes_dif = []
    e_info_doc_dif = []
    e_recolhimentos_dif = []
    e_ipi = []
    e_ipi_detalhes = []
    e_ipi_saldo = None
    e_ipi_ajustes = []
    e_ipi_recolhimentos = []
    abertura_bloco_g = None
    g_resumos = []
    g_bens = []
    g_saldos = []
    g_docs = []
    g_icms_util = []
    abertura_bloco_h = None
    inventario = []
    inventario_itens = []
    inventario_impostos = []
    inventario_complemento = []
    fechamento_bloco_h = None
    abertura_bloco_k = None
    k_periodos = []
    k_estoques = []
    k_desmontagens = []
    k_movimentacoes = []
    k_producoes = []
    k_insumos = []
    k_industrializacao_terceiros = []
    k_industrializacao_insumos = []
    k_reprocesso = []
    k_reprocesso_insumos = []
    k_correcao_ordem = []
    k_correcao_insumos = []
    k_correcao_estoque = []
    k_producao_conjunta = []
    k_producao_conjunta_itens = []
    k_producao_conjunta_insumos = []
    k_producao_terceiros = []
    k_producao_terceiros_itens = []
    k_producao_terceiros_insumos = []
    fechamento_bloco_k = None
    abertura_bloco_1 = None
    obrigatoriedades_1010 = []
    exportacoes_1100 = []
    exportacoes_docs = []
    creditos_icms = []
    creditos_icms_utilizacao = []
    creditos_icms_rest = []
    creditos_icms_rest_det = []
    combustiveis_mov = []
    combustiveis_tanques = []
    combustiveis_bicos = []
    usina_controle = []
    usina_insumos = []
    valor_adicionado = []
    energia_interestadual = []
    energia_itens = []
    pagamentos_eletronicos = []
    documentos_utilizados = []
    documentos_cancelados = []
    transporte_aereo = []
    subapuracoes = []
    subapuracoes_periodos = []
    subapuracoes_resumo = []
    subapuracoes_ajustes = []
    subapuracoes_obrigacoes = []
    abertura_bloco_9 = None
    registros_9900 = []
    fechamento_bloco_9 = None
    fechamento_sped = None
    fechamento_bloco_1 = None
    fechamento_bloco_d = None
    fechamento_bloco0 = None
    abertura_bloco_b = None
    fechamento_bloco_b = None
    abertura_bloco_c = None
    fechamento_bloco_c = None
    abertura_bloco_d = None
    itens = []
    notas = []
    transportes = []
    transportes_resumo = []

    current_c100 = None
    current_c110 = None
    current_c350 = None
    current_c400 = None
    current_c405 = None
    current_c460 = None
    current_c500 = None
    current_c700 = None
    current_c800 = None
    current_d160 = None
    current_d100 = None
    current_d200 = None
    current_d300 = None
    current_d350 = None
    current_d360 = None
    current_d400 = None
    current_d410 = None
    current_d500 = None
    current_d695 = None
    current_d700 = None
    current_e100 = None
    current_e110 = None
    current_e200 = None
    current_e210 = None
    current_e300 = None
    current_e310 = None
    current_e500 = None
    current_g110 = None
    current_g125 = None
    current_h005 = None
    current_h010 = None
    current_k210 = None
    current_k230 = None
    current_k250 = None
    current_k260 = None
    current_k300 = None
    current_k301 = None
    current_1500 = None
    current_1900 = None
    current_1920 = None
    current_1300 = None
    current_1310 = None
    current_1921 = None
    current_1960 = None
    current_1970 = None
    current_1100 = None
    current_1200 = None
    current_1250 = None
    current_1300 = None
    current_1310 = None
    current_1700 = None
    current_c170 = None
    current_c185 = None
    current_c350 = None
    current_0200 = None
    current_0300 = None

    contadores = {k: 0 for k in LAYOUTS.keys()}
    contadores["linhas_ignoradas"] = 0

    for line in content.splitlines():
        parsed = parse_line(line)
        if not parsed:
            contadores["linhas_ignoradas"] += 1
            continue

        reg, parts = parsed
        if reg not in LAYOUTS:
            continue  # ignora outros registros

        contadores[reg] += 1
        d = build_dict(parts, LAYOUTS[reg])

        # Estrutura por tipo
        if reg == "0000":
            abertura = d

        elif reg == "0001":
            abertura_bloco0 = d

        elif reg == "0002":
            classificacoes.append(d)

        elif reg == "0005":
            dados_complementares.append(d)

        elif reg == "0015":
            substitutos_uf.append(d)

        elif reg == "0100":
            contabilistas.append(d)

        elif reg == "0150":
            participantes.append(d)

        elif reg == "0175":
            historico_participantes.append(d)

        elif reg == "0190":
            unidades.append(d)
        
        elif reg == "0200":
            itens.append(d)
            current_0200 = d
            current_0200["conversoes"] = []

        elif reg == "0220":
            if current_0200 is None:
                d["_erro"] = "0220_sem_0200"
                conversoes.append(d)
            else:
                current_0200["conversoes"].append(d)
                conversoes.append(d)

        elif reg == "0300":
            current_0300 = d
            current_0300["usos"] = []
            bens.append(current_0300)

        elif reg == "0305":
            if current_0300 is None:
                d["_erro"] = "0305_sem_0300"
                bens.append({"_erro": "0300_ausente", "usos": [d]})
            else:
                current_0300["usos"].append(d)

        elif reg == "0400":
            natureza_operacao.append(d)

        elif reg == "0450":
            info_complementar.append(d)

        elif reg == "0460":
            observacoes_lancamento.append(d)

        elif reg == "0500":
            plano_contas.append(d)

        elif reg == "0600":
            centros_custos.append(d)

        elif reg == "0990":
            fechamento_bloco0 = d

        elif reg == "B001":
            abertura_bloco_b = d

        elif reg == "B990":
            fechamento_bloco_b = d

        elif reg == "C001":
            abertura_bloco_c = d

        elif reg == "C100":
            current_c100 = d
            current_c110 = None
            current_c100["itens"] = []
            current_c100["c101"] = []
            current_c100["c105"] = []
            current_c100["c110"] = []
            current_c100["c120"] = []
            current_c100["c176"] = []
            current_c100["c177"] = []
            current_c100["c185"] = []
            current_c100["c186"] = []
            current_c100["c190"] = []
            current_c100["c191"] = []
            current_c100["c195"] = []
            current_c100["c197"] = []
            notas.append(current_c100)

        elif reg == "C101":
            if current_c100 is None:
                d["_erro"] = "C101_sem_C100"
                notas.append({"_erro": "C100_ausente", "c101": [d], "itens": []})
            else:
                current_c100["c101"].append(d)

        elif reg == "C105":
            if current_c100 is None:
                d["_erro"] = "C105_sem_C100"
                notas.append({"_erro": "C100_ausente", "c105": [d], "itens": []})
            else:
                current_c100["c105"].append(d)

        elif reg == "C110":
            current_c110 = d
            current_c110["c111"] = []
            current_c110["c112"] = []
            current_c110["c113"] = []
            current_c110["c114"] = []
            current_c110["c116"] = []
            if current_c100 is None:
                d["_erro"] = "C110_sem_C100"
                notas.append({"_erro": "C100_ausente", "c110": [current_c110], "itens": []})
            else:
                current_c100["c110"].append(current_c110)

        elif reg == "C111":
            if current_c110 is None:
                d["_erro"] = "C111_sem_C110"
                notas.append({"_erro": "C110_ausente", "c111": [d], "itens": []})
            else:
                current_c110["c111"].append(d)

        elif reg == "C112":
            if current_c110 is None:
                d["_erro"] = "C112_sem_C110"
                notas.append({"_erro": "C110_ausente", "c112": [d], "itens": []})
            else:
                current_c110["c112"].append(d)

        elif reg == "C113":
            if current_c110 is None:
                d["_erro"] = "C113_sem_C110"
                notas.append({"_erro": "C110_ausente", "c113": [d], "itens": []})
            else:
                current_c110["c113"].append(d)

        elif reg == "C114":
            if current_c110 is None:
                d["_erro"] = "C114_sem_C110"
                notas.append({"_erro": "C110_ausente", "c114": [d], "itens": []})
            else:
                current_c110["c114"].append(d)

        elif reg == "C116":
            if current_c110 is None:
                d["_erro"] = "C116_sem_C110"
                notas.append({"_erro": "C110_ausente", "c116": [d], "itens": []})
            else:
                current_c110["c116"].append(d)

        elif reg == "C120":
            if current_c100 is None:
                d["_erro"] = "C120_sem_C100"
                notas.append({"_erro": "C100_ausente", "c120": [d], "itens": []})
            else:
                current_c100["c120"].append(d)

        elif reg == "C176":
            if current_c100 is None:
                d["_erro"] = "C176_sem_C100"
                notas.append({"_erro": "C100_ausente", "c176": [d], "itens": []})
            else:
                current_c100["c176"].append(d)
            complementos_c176.append(d)

        elif reg == "C177":
            if current_c100 is None:
                d["_erro"] = "C177_sem_C100"
                notas.append({"_erro": "C100_ausente", "c177": [d], "itens": []})
            else:
                current_c100["c177"].append(d)
            complementos_c177.append(d)

        elif reg == "C185":
            if current_c100 is None:
                d["_erro"] = "C185_sem_C100"
                notas.append({"_erro": "C100_ausente", "c185": [d], "itens": []})
            else:
                current_c100["c185"].append(d)
            complementos_c185.append(d)

        elif reg == "C186":
            if current_c100 is None:
                d["_erro"] = "C186_sem_C100"
                notas.append({"_erro": "C100_ausente", "c186": [d], "itens": []})
            else:
                current_c100["c186"].append(d)
            complementos_c186.append(d)

        elif reg == "C190":
            if current_c100 is None:
                d["_erro"] = "C190_sem_C100"
                notas.append({"_erro": "C100_ausente", "c190": [d], "itens": []})
            else:
                current_c100["c190"].append(d)
            analiticos_c190.append(d)

        elif reg == "C191":
            if current_c100 is None:
                d["_erro"] = "C191_sem_C100"
                notas.append({"_erro": "C100_ausente", "c191": [d], "itens": []})
            else:
                current_c100["c191"].append(d)
            fcp_c191.append(d)

        elif reg == "C195":
            if current_c100 is None:
                d["_erro"] = "C195_sem_C100"
                notas.append({"_erro": "C100_ausente", "c195": [d], "itens": []})
            else:
                current_c100["c195"].append(d)
            observacoes_c195.append(d)

        elif reg == "C197":
            if current_c100 is None:
                d["_erro"] = "C197_sem_C100"
                notas.append({"_erro": "C100_ausente", "c197": [d], "itens": []})
            else:
                current_c100["c197"].append(d)
            ajustes_c197.append(d)

        elif reg == "C170":
            if current_c100 is None:
                # item sem pai; ainda assim guardamos solto para diagnóstico
                d["_erro"] = "C170_sem_C100"
                notas.append({"_erro": "C100_ausente", "itens": [d]})
            else:
                current_c100["itens"].append(d)
                current_c170 = d

        elif reg == "C176":
            if current_c170 is None:
                d["_erro"] = "C176_sem_C170"
                notas.append({"_erro": "C170_ausente", "itens": [d]})
            else:
                current_c170.setdefault("c176", []).append(d)
            complementos_c176.append(d)

        elif reg == "C185":
            if current_c100 is None:
                d["_erro"] = "C185_sem_C100"
                notas.append({"_erro": "C100_ausente", "c185": [d], "itens": []})
            else:
                current_c100.setdefault("c185", []).append(d)
            complementos_c185.append(d)
            current_c185 = d

        elif reg == "C186":
            if current_c185 is None:
                d["_erro"] = "C186_sem_C185"
                complementos_c186.append(d)
            else:
                current_c185.setdefault("c186", []).append(d)
                complementos_c186.append(d)

        elif reg == "C350":
            current_c350 = d
            current_c350["c370"] = []
            current_c350["c380"] = []
            current_c350["c390"] = []
            resumos_c350.append(current_c350)

        elif reg == "C370":
            if current_c350 is None:
                d["_erro"] = "C370_sem_C350"
                resumos_c350.append({"_erro": "C350_ausente", "c370": [d], "c380": [], "c390": []})
            else:
                current_c350["c370"].append(d)

        elif reg == "C380":
            if current_c350 is None:
                d["_erro"] = "C380_sem_C350"
                resumos_c350.append({"_erro": "C350_ausente", "c370": [], "c380": [d], "c390": []})
            else:
                current_c350["c380"].append(d)

        elif reg == "C390":
            if current_c350 is None:
                d["_erro"] = "C390_sem_C350"
                resumos_c350.append({"_erro": "C350_ausente", "c370": [], "c380": [], "c390": [d]})
            else:
                current_c350["c390"].append(d)

        elif reg == "C400":
            current_c400 = d
            current_c405 = None
            current_c400["reducoes"] = []
            ecf.append(current_c400)

        elif reg == "C405":
            current_c405 = d
            current_c405["c410"] = []
            current_c405["c420"] = []
            if current_c400 is None:
                d["_erro"] = "C405_sem_C400"
                ecf.append({"_erro": "C400_ausente", "reducoes": [current_c405]})
            else:
                current_c400["reducoes"].append(current_c405)

        elif reg == "C410":
            if current_c405 is None:
                d["_erro"] = "C410_sem_C405"
                ecf.append({"_erro": "C405_ausente", "reducoes": [{"c410": [d], "c420": []}]})
            else:
                current_c405["c410"].append(d)

        elif reg == "C420":
            if current_c405 is None:
                d["_erro"] = "C420_sem_C405"
                ecf.append({"_erro": "C405_ausente", "reducoes": [{"c410": [], "c420": [d]}]})
            else:
                current_c405["c420"].append(d)

        elif reg == "C460":
            current_c460 = d
            current_c460["c470"] = []
            current_c460["c480"] = []
            current_c460["c490"] = []
            documentos_ecf.append(current_c460)

        elif reg == "C470":
            if current_c460 is None:
                d["_erro"] = "C470_sem_C460"
                documentos_ecf.append({"_erro": "C460_ausente", "c470": [d], "c480": [], "c490": []})
            else:
                current_c460["c470"].append(d)

        elif reg == "C480":
            if current_c460 is None:
                d["_erro"] = "C480_sem_C460"
                documentos_ecf.append({"_erro": "C460_ausente", "c470": [], "c480": [d], "c490": []})
            else:
                current_c460["c480"].append(d)

        elif reg == "C490":
            if current_c460 is None:
                d["_erro"] = "C490_sem_C460"
                documentos_ecf.append({"_erro": "C460_ausente", "c470": [], "c480": [], "c490": [d]})
            else:
                current_c460["c490"].append(d)

        elif reg == "C500":
            current_c500 = d
            current_c500["c590"] = []
            current_c500["c591"] = []
            current_c500["c595"] = []
            current_c500["c597"] = []
            servicos.append(current_c500)

        elif reg == "C590":
            if current_c500 is None:
                d["_erro"] = "C590_sem_C500"
                servicos.append({"_erro": "C500_ausente", "c590": [d], "c591": [], "c595": [], "c597": []})
            else:
                current_c500["c590"].append(d)

        elif reg == "C591":
            if current_c500 is None:
                d["_erro"] = "C591_sem_C500"
                servicos.append({"_erro": "C500_ausente", "c590": [], "c591": [d], "c595": [], "c597": []})
            else:
                current_c500["c591"].append(d)

        elif reg == "C595":
            if current_c500 is None:
                d["_erro"] = "C595_sem_C500"
                servicos.append({"_erro": "C500_ausente", "c590": [], "c591": [], "c595": [d], "c597": []})
            else:
                current_c500["c595"].append(d)

        elif reg == "C597":
            if current_c500 is None:
                d["_erro"] = "C597_sem_C500"
                servicos.append({"_erro": "C500_ausente", "c590": [], "c591": [], "c595": [], "c597": [d]})
            else:
                current_c500["c597"].append(d)

        elif reg == "C700":
            current_c700 = d
            current_c700["c790"] = []
            current_c700["c791"] = []
            consolidacoes.append(current_c700)

        elif reg == "C790":
            if current_c700 is None:
                d["_erro"] = "C790_sem_C700"
                consolidacoes.append({"_erro": "C700_ausente", "c790": [d], "c791": []})
            else:
                current_c700["c790"].append(d)

        elif reg == "C791":
            if current_c700 is None:
                d["_erro"] = "C791_sem_C700"
                consolidacoes.append({"_erro": "C700_ausente", "c790": [], "c791": [d]})
            else:
                current_c700["c791"].append(d)

        elif reg == "C800":
            current_c800 = d
            current_c800["c810"] = []
            current_c800["c815"] = []
            current_c800["c850"] = []
            cfe.append(current_c800)

        elif reg == "C810":
            if current_c800 is None:
                d["_erro"] = "C810_sem_C800"
                cfe.append({"_erro": "C800_ausente", "c810": [d], "c815": [], "c850": []})
            else:
                current_c800["c810"].append(d)

        elif reg == "C815":
            if current_c800 is None:
                d["_erro"] = "C815_sem_C800"
                cfe.append({"_erro": "C800_ausente", "c810": [], "c815": [d], "c850": []})
            else:
                current_c800["c815"].append(d)

        elif reg == "C850":
            if current_c800 is None:
                d["_erro"] = "C850_sem_C800"
                cfe.append({"_erro": "C800_ausente", "c810": [], "c815": [], "c850": [d]})
            else:
                current_c800["c850"].append(d)

        elif reg == "C990":
            fechamento_bloco_c = d

        elif reg == "D001":
            abertura_bloco_d = d

        elif reg == "D100":
            current_d100 = d
            current_d100["pis"] = None
            current_d100["cofins"] = None
            current_d100["d130"] = []
            current_d100["d140"] = []
            current_d100["d150"] = []
            current_d100["d160"] = []
            current_d100["d170"] = []
            current_d100["d180"] = []
            current_d100["d190"] = []
            current_d100["d195"] = []
            current_d100["d197"] = []
            transportes.append(current_d100)

        elif reg == "D101":
            if current_d100 is None:
                d["_erro"] = "D101_sem_D100"
                transportes.append({"_erro": "D100_ausente", "pis": d, "cofins": None})
            else:
                current_d100["pis"] = d

        elif reg == "D105":
            if current_d100 is None:
                d["_erro"] = "D105_sem_D100"
                transportes.append({"_erro": "D100_ausente", "pis": None, "cofins": d})
            else:
                current_d100["cofins"] = d

        elif reg == "D130":
            if current_d100 is None:
                d["_erro"] = "D130_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d130": [d], "pis": None, "cofins": None})
            else:
                current_d100["d130"].append(d)
            complementos_d130.append(d)

        elif reg == "D140":
            if current_d100 is None:
                d["_erro"] = "D140_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d140": [d], "pis": None, "cofins": None})
            else:
                current_d100["d140"].append(d)
            complementos_d140.append(d)

        elif reg == "D150":
            if current_d100 is None:
                d["_erro"] = "D150_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d150": [d], "pis": None, "cofins": None})
            else:
                current_d100["d150"].append(d)
            complementos_d150.append(d)

        elif reg == "D160":
            current_d160 = d
            current_d160["d161"] = []
            current_d160["d162"] = []
            if current_d100 is None:
                d["_erro"] = "D160_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d160": [current_d160], "pis": None, "cofins": None})
            else:
                current_d100["d160"].append(current_d160)
            complementos_d160.append(current_d160)

        elif reg == "D161":
            if current_d160 is None:
                d["_erro"] = "D161_sem_D160"
                complementos_d161.append(d)
            else:
                current_d160["d161"].append(d)
                complementos_d161.append(d)

        elif reg == "D162":
            if current_d160 is None:
                d["_erro"] = "D162_sem_D160"
                complementos_d162.append(d)
            else:
                current_d160["d162"].append(d)
                complementos_d162.append(d)

        elif reg == "D170":
            if current_d100 is None:
                d["_erro"] = "D170_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d170": [d], "pis": None, "cofins": None})
            else:
                current_d100["d170"].append(d)
            complementos_d170.append(d)

        elif reg == "D180":
            if current_d100 is None:
                d["_erro"] = "D180_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d180": [d], "pis": None, "cofins": None})
            else:
                current_d100["d180"].append(d)
            complementos_d180.append(d)

        elif reg == "D190":
            if current_d100 is None:
                d["_erro"] = "D190_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d190": [d], "pis": None, "cofins": None})
            else:
                current_d100["d190"].append(d)
            analiticos_d190.append(d)

        elif reg == "D195":
            if current_d100 is None:
                d["_erro"] = "D195_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d195": [d], "pis": None, "cofins": None})
            else:
                current_d100["d195"].append(d)
            observacoes_d195.append(d)

        elif reg == "D197":
            if current_d100 is None:
                d["_erro"] = "D197_sem_D100"
                transportes.append({"_erro": "D100_ausente", "d197": [d], "pis": None, "cofins": None})
            else:
                current_d100["d197"].append(d)
            ajustes_d197.append(d)

        elif reg == "D200":
            current_d200 = d
            current_d200["pis"] = None
            current_d200["cofins"] = None
            transportes_resumo.append(current_d200)

        elif reg == "D201":
            if current_d200 is None:
                d["_erro"] = "D201_sem_D200"
                transportes_resumo.append({"_erro": "D200_ausente", "pis": d, "cofins": None})
            else:
                current_d200["pis"] = d

        elif reg == "D205":
            if current_d200 is None:
                d["_erro"] = "D205_sem_D200"
                transportes_resumo.append({"_erro": "D200_ausente", "pis": None, "cofins": d})
            else:
                current_d200["cofins"] = d

        elif reg == "D300":
            current_d300 = d
            current_d300["d301"] = []
            current_d300["d310"] = []
            bilhetes.append(current_d300)

        elif reg == "D301":
            if current_d300 is None:
                d["_erro"] = "D301_sem_D300"
                bilhetes.append({"_erro": "D300_ausente", "d301": [d], "d310": []})
            else:
                current_d300["d301"].append(d)

        elif reg == "D310":
            if current_d300 is None:
                d["_erro"] = "D310_sem_D300"
                bilhetes.append({"_erro": "D300_ausente", "d301": [], "d310": [d]})
            else:
                current_d300["d310"].append(d)

        elif reg == "D350":
            current_d350 = d
            current_d350["d355"] = []
            ecf_d350.append(current_d350)

        elif reg == "D355":
            if current_d350 is None:
                d["_erro"] = "D355_sem_D350"
                ecf_d350.append({"_erro": "D350_ausente", "d355": [d]})
            else:
                current_d350["d355"].append(d)

        elif reg == "D360":
            current_d360 = d
            current_d360["d365"] = []
            current_d360["d370"] = []
            bpe.append(current_d360)

        elif reg == "D365":
            if current_d360 is None:
                d["_erro"] = "D365_sem_D360"
                bpe.append({"_erro": "D360_ausente", "d365": [d], "d370": []})
            else:
                current_d360["d365"].append(d)

        elif reg == "D370":
            if current_d360 is None:
                d["_erro"] = "D370_sem_D360"
                bpe.append({"_erro": "D360_ausente", "d365": [], "d370": [d]})
            else:
                current_d360["d370"].append(d)

        elif reg == "D390":
            bpe_simplificado.append(d)

        elif reg == "D400":
            current_d400 = d
            current_d400["d410"] = []
            resumo_transporte.append(current_d400)

        elif reg == "D410":
            current_d410 = d
            current_d410["d411"] = []
            current_d410["d420"] = []
            if current_d400 is None:
                d["_erro"] = "D410_sem_D400"
                resumo_transporte.append({"_erro": "D400_ausente", "d410": [current_d410]})
            else:
                current_d400["d410"].append(current_d410)

        elif reg == "D411":
            if current_d410 is None:
                d["_erro"] = "D411_sem_D410"
                resumo_transporte.append({"_erro": "D410_ausente", "d411": [d]})
            else:
                current_d410["d411"].append(d)

        elif reg == "D420":
            if current_d410 is None:
                d["_erro"] = "D420_sem_D410"
                resumo_transporte.append({"_erro": "D410_ausente", "d420": [d]})
            else:
                current_d410["d420"].append(d)

        elif reg == "D500":
            current_d500 = d
            current_d500["d510"] = []
            current_d500["d530"] = []
            telecom.append(current_d500)

        elif reg == "D510":
            if current_d500 is None:
                d["_erro"] = "D510_sem_D500"
                telecom.append({"_erro": "D500_ausente", "d510": [d], "d530": []})
            else:
                current_d500["d510"].append(d)

        elif reg == "D530":
            if current_d500 is None:
                d["_erro"] = "D530_sem_D500"
                telecom.append({"_erro": "D500_ausente", "d510": [], "d530": [d]})
            else:
                current_d500["d530"].append(d)

        elif reg == "D590":
            telecom_resumo.append(d)

        elif reg == "D695":
            current_d695 = d
            current_d695["d696"] = []
            current_d695["d697"] = []
            energia_comunicacao_resumo.append(current_d695)

        elif reg == "D696":
            if current_d695 is None:
                d["_erro"] = "D696_sem_D695"
                energia_comunicacao_resumo.append({"_erro": "D695_ausente", "d696": [d], "d697": []})
            else:
                current_d695["d696"].append(d)

        elif reg == "D697":
            if current_d695 is None:
                d["_erro"] = "D697_sem_D695"
                energia_comunicacao_resumo.append({"_erro": "D695_ausente", "d696": [], "d697": [d]})
            else:
                current_d695["d697"].append(d)

        elif reg == "D700":
            current_d700 = d
            current_d700["d730"] = []
            current_d700["d731"] = []
            current_d700["d737"] = []
            gas.append(current_d700)

        elif reg == "D730":
            if current_d700 is None:
                d["_erro"] = "D730_sem_D700"
                gas.append({"_erro": "D700_ausente", "d730": [d], "d731": [], "d737": []})
            else:
                current_d700["d730"].append(d)

        elif reg == "D731":
            if current_d700 is None:
                d["_erro"] = "D731_sem_D700"
                gas.append({"_erro": "D700_ausente", "d730": [], "d731": [d], "d737": []})
            else:
                current_d700["d731"].append(d)

        elif reg == "D737":
            if current_d700 is None:
                d["_erro"] = "D737_sem_D700"
                gas.append({"_erro": "D700_ausente", "d730": [], "d731": [], "d737": [d]})
            else:
                current_d700["d737"].append(d)

        elif reg == "D735":
            gas_resumo_clas.append(d)

        elif reg == "D750":
            gas_icms_outra_uf.append(d)

        elif reg == "D760":
            gas_resumo_mensal.append(d)

        elif reg == "D761":
            gas_resumo_st.append(d)

        elif reg == "D990":
            fechamento_bloco_d = d

        elif reg == "E001":
            abertura_bloco_e = d

        elif reg == "E100":
            current_e100 = d
            current_e100["e110"] = None
            e_periodos_icms.append(current_e100)

        elif reg == "E110":
            current_e110 = d
            current_e110["e111"] = []
            current_e110["e112"] = []
            current_e110["e113"] = []
            current_e110["e115"] = []
            current_e110["e116"] = []
            e_apuracoes_icms.append(current_e110)
            if current_e100 is not None:
                current_e100["e110"] = current_e110

        elif reg == "E111":
            if current_e110 is None:
                d["_erro"] = "E111_sem_E110"
            else:
                current_e110["e111"].append(d)
            e_ajustes_icms.append(d)

        elif reg == "E112":
            if current_e110 is None:
                d["_erro"] = "E112_sem_E110"
            else:
                current_e110["e112"].append(d)
            e_obrigacoes_icms.append(d)

        elif reg == "E113":
            if current_e110 is None:
                d["_erro"] = "E113_sem_E110"
            else:
                current_e110["e113"].append(d)
            e_info_doc_icms.append(d)

        elif reg == "E115":
            if current_e110 is None:
                d["_erro"] = "E115_sem_E110"
            else:
                current_e110["e115"].append(d)
            e_info_adic_icms.append(d)

        elif reg == "E116":
            if current_e110 is None:
                d["_erro"] = "E116_sem_E110"
            else:
                current_e110["e116"].append(d)
            e_recolhimentos_icms.append(d)

        elif reg == "E200":
            current_e200 = d
            current_e200["e210"] = []
            e_periodos_st.append(current_e200)

        elif reg == "E210":
            current_e210 = d
            current_e210["e220"] = []
            current_e210["e230"] = []
            current_e210["e250"] = []
            e_apuracoes_st.append(current_e210)
            if current_e200 is not None:
                current_e200["e210"].append(current_e210)

        elif reg == "E220":
            if current_e210 is None:
                d["_erro"] = "E220_sem_E210"
            else:
                current_e210["e220"].append(d)
            e_ajustes_st.append(d)

        elif reg == "E230":
            if current_e210 is None:
                d["_erro"] = "E230_sem_E210"
            else:
                current_e210["e230"].append(d)
            e_info_doc_st.append(d)

        elif reg == "E250":
            if current_e210 is None:
                d["_erro"] = "E250_sem_E210"
            else:
                current_e210["e250"].append(d)
            e_recolhimentos_st.append(d)

        elif reg == "E300":
            current_e300 = d
            current_e300["e310"] = None
            e_periodos_dif.append(current_e300)

        elif reg == "E310":
            current_e310 = d
            current_e310["e311"] = []
            current_e310["e312"] = []
            current_e310["e313"] = []
            current_e310["e316"] = []
            e_apuracoes_dif.append(current_e310)
            if current_e300 is not None:
                current_e300["e310"] = current_e310

        elif reg == "E311":
            if current_e310 is None:
                d["_erro"] = "E311_sem_E310"
            else:
                current_e310["e311"].append(d)
            e_ajustes_dif.append(d)

        elif reg == "E312":
            if current_e310 is None:
                d["_erro"] = "E312_sem_E310"
            else:
                current_e310["e312"].append(d)
            e_obrigacoes_dif.append(d)

        elif reg == "E313":
            if current_e310 is None:
                d["_erro"] = "E313_sem_E310"
            else:
                current_e310["e313"].append(d)
            e_info_doc_dif.append(d)

        elif reg == "E316":
            if current_e310 is None:
                d["_erro"] = "E316_sem_E310"
            else:
                current_e310["e316"].append(d)
            e_recolhimentos_dif.append(d)

        elif reg == "E500":
            current_e500 = d
            current_e500["e510"] = []
            current_e500["e520"] = None
            current_e500["e530"] = []
            current_e500["e531"] = []
            e_ipi.append(current_e500)

        elif reg == "E510":
            if current_e500 is None:
                d["_erro"] = "E510_sem_E500"
                e_ipi_detalhes.append(d)
            else:
                current_e500["e510"].append(d)
                e_ipi_detalhes.append(d)

        elif reg == "E520":
            e_ipi_saldo = d
            if current_e500 is not None:
                current_e500["e520"] = d

        elif reg == "E530":
            if current_e500 is None:
                d["_erro"] = "E530_sem_E500"
            else:
                current_e500["e530"].append(d)
            e_ipi_ajustes.append(d)

        elif reg == "E531":
            if current_e500 is None:
                d["_erro"] = "E531_sem_E500"
            else:
                current_e500["e531"].append(d)
            e_ipi_recolhimentos.append(d)

        elif reg == "E990":
            # mantemos apenas contagem; não guardamos separado
            pass

        elif reg == "G001":
            abertura_bloco_g = d

        elif reg == "G110":
            current_g110 = d
            current_g110["g125"] = []
            g_resumos.append(current_g110)

        elif reg == "G125":
            current_g125 = d
            current_g125["g126"] = []
            current_g125["g130"] = []
            current_g125["g140"] = []
            if current_g110 is None:
                d["_erro"] = "G125_sem_G110"
                g_bens.append({"_erro": "G110_ausente", "g126": [], "g130": [], "g140": []})
            else:
                current_g110["g125"].append(current_g125)
            g_bens.append(current_g125)

        elif reg == "G126":
            if current_g125 is None:
                d["_erro"] = "G126_sem_G125"
                g_saldos.append(d)
            else:
                current_g125["g126"].append(d)
                g_saldos.append(d)

        elif reg == "G130":
            if current_g125 is None:
                d["_erro"] = "G130_sem_G125"
                g_docs.append(d)
            else:
                current_g125["g130"].append(d)
                g_docs.append(d)

        elif reg == "G140":
            if current_g125 is None:
                d["_erro"] = "G140_sem_G125"
                g_icms_util.append(d)
            else:
                current_g125["g140"].append(d)
                g_icms_util.append(d)

        elif reg == "G990":
            # encerra bloco G
            pass

        elif reg == "H001":
            abertura_bloco_h = d

        elif reg == "H005":
            current_h005 = d
            current_h005["h010"] = []
            inventario.append(current_h005)

        elif reg == "H010":
            current_h010 = d
            current_h010["h020"] = []
            current_h010["h030"] = []
            if current_h005 is None:
                d["_erro"] = "H010_sem_H005"
                inventario_itens.append(d)
            else:
                current_h005["h010"].append(current_h010)
                inventario_itens.append(current_h010)

        elif reg == "H020":
            if current_h010 is None:
                d["_erro"] = "H020_sem_H010"
                inventario_impostos.append(d)
            else:
                current_h010["h020"].append(d)
                inventario_impostos.append(d)

        elif reg == "H030":
            if current_h010 is None:
                d["_erro"] = "H030_sem_H010"
                inventario_complemento.append(d)
            else:
                current_h010["h030"].append(d)
                inventario_complemento.append(d)

        elif reg == "H990":
            fechamento_bloco_h = d

        elif reg == "K001":
            abertura_bloco_k = d

        elif reg == "K100":
            k_periodos.append(d)

        elif reg == "K200":
            k_estoques.append(d)

        elif reg == "K210":
            current_k210 = d
            current_k210["k215"] = []
            k_desmontagens.append(current_k210)

        elif reg == "K215":
            if current_k210 is None:
                d["_erro"] = "K215_sem_K210"
                k_desmontagens.append({"_erro": "K210_ausente", "k215": [d]})
            else:
                current_k210["k215"].append(d)

        elif reg == "K220":
            k_movimentacoes.append(d)

        elif reg == "K230":
            current_k230 = d
            current_k230["k235"] = []
            k_producoes.append(current_k230)

        elif reg == "K235":
            if current_k230 is None:
                d["_erro"] = "K235_sem_K230"
                k_insumos.append(d)
            else:
                current_k230["k235"].append(d)
                k_insumos.append(d)

        elif reg == "K250":
            current_k250 = d
            current_k250["k255"] = []
            k_industrializacao_terceiros.append(current_k250)

        elif reg == "K255":
            if current_k250 is None:
                d["_erro"] = "K255_sem_K250"
                k_industrializacao_insumos.append(d)
            else:
                current_k250["k255"].append(d)
                k_industrializacao_insumos.append(d)

        elif reg == "K260":
            current_k260 = d
            current_k260["k265"] = []
            k_reprocesso.append(current_k260)

        elif reg == "K265":
            if current_k260 is None:
                d["_erro"] = "K265_sem_K260"
                k_reprocesso_insumos.append(d)
            else:
                current_k260["k265"].append(d)
                k_reprocesso_insumos.append(d)

        elif reg == "K270":
            k_correcao_ordem.append(d)

        elif reg == "K275":
            k_correcao_insumos.append(d)

        elif reg == "K280":
            k_correcao_estoque.append(d)

        elif reg == "K290":
            k_producao_conjunta.append(d)

        elif reg == "K291":
            k_producao_conjunta_itens.append(d)

        elif reg == "K292":
            k_producao_conjunta_insumos.append(d)

        elif reg == "K300":
            current_k300 = d
            current_k300["k301"] = []
            current_k300["k302"] = []
            k_producao_terceiros.append(current_k300)

        elif reg == "K301":
            if current_k300 is None:
                d["_erro"] = "K301_sem_K300"
                k_producao_terceiros_itens.append(d)
            else:
                current_k300["k301"].append(d)
                k_producao_terceiros_itens.append(d)

        elif reg == "K302":
            if current_k300 is None:
                d["_erro"] = "K302_sem_K300"
                k_producao_terceiros_insumos.append(d)
            else:
                current_k300["k302"].append(d)
                k_producao_terceiros_insumos.append(d)

        elif reg == "K990":
            fechamento_bloco_k = d

        elif reg == "1001":
            abertura_bloco_1 = d

        elif reg == "1010":
            obrigatoriedades_1010.append(d)

        elif reg == "1100":
            exportacoes_1100.append(d)
            current_1100 = d
            current_1100["docs"] = []

        elif reg == "1105":
            if 'current_1100' not in locals() or current_1100 is None:
                d["_erro"] = "1105_sem_1100"
                exportacoes_docs.append(d)
            else:
                current_1100["docs"].append(d)
                exportacoes_docs.append(d)

        elif reg == "1200":
            creditos_icms.append(d)
            current_1200 = d
            current_1200["uso"] = []

        elif reg == "1210":
            if 'current_1200' not in locals() or current_1200 is None:
                d["_erro"] = "1210_sem_1200"
                creditos_icms_utilizacao.append(d)
            else:
                current_1200["uso"].append(d)
                creditos_icms_utilizacao.append(d)

        elif reg == "1250":
            creditos_icms_rest.append(d)
            current_1250 = d
            current_1250["detalhes"] = []

        elif reg == "1255":
            if 'current_1250' not in locals() or current_1250 is None:
                d["_erro"] = "1255_sem_1250"
                creditos_icms_rest_det.append(d)
            else:
                current_1250["detalhes"].append(d)
                creditos_icms_rest_det.append(d)

        elif reg == "1300":
            current_1300 = d
            current_1300["d1301"] = []  # not used; placeholder
            current_1300["d1310"] = []
            current_1300["d1320"] = []
            combustiveis_mov.append(current_1300)

        elif reg == "1310":
            current_1310 = d
            current_1310["d1320"] = []
            if current_1300 is None:
                d["_erro"] = "1310_sem_1300"
                combustiveis_tanques.append(d)
            else:
                current_1300["d1310"].append(current_1310)
                combustiveis_tanques.append(d)

        elif reg == "1320":
            if current_1310 is None:
                d["_erro"] = "1320_sem_1310"
                combustiveis_bicos.append(d)
            else:
                current_1310["d1320"].append(d)
                combustiveis_bicos.append(d)

        elif reg == "1390":
            usina_controle.append(d)
            current_1390 = d
            current_1390["insumos"] = []

        elif reg == "1391":
            if 'current_1390' not in locals() or current_1390 is None:
                d["_erro"] = "1391_sem_1390"
                usina_insumos.append(d)
            else:
                current_1390["insumos"].append(d)
                usina_insumos.append(d)

        elif reg == "1400":
            valor_adicionado.append(d)

        elif reg == "1500":
            current_1500 = d
            current_1500["itens"] = []
            energia_interestadual.append(current_1500)

        elif reg == "1510":
            if current_1500 is None:
                d["_erro"] = "1510_sem_1500"
                energia_itens.append(d)
            else:
                current_1500["itens"].append(d)
                energia_itens.append(d)

        elif reg == "1601":
            pagamentos_eletronicos.append(d)

        elif reg == "1700":
            current_1700 = d
            current_1700["cancelados"] = []
            documentos_utilizados.append(current_1700)

        elif reg == "1710":
            if 'current_1700' not in locals() or current_1700 is None:
                d["_erro"] = "1710_sem_1700"
                documentos_cancelados.append(d)
            else:
                current_1700["cancelados"].append(d)
                documentos_cancelados.append(d)

        elif reg == "1800":
            transporte_aereo.append(d)

        elif reg == "1900":
            current_1900 = d
            current_1900["periodos"] = []
            subapuracoes.append(current_1900)

        elif reg == "1910":
            if current_1900 is None:
                d["_erro"] = "1910_sem_1900"
                subapuracoes_periodos.append(d)
            else:
                current_1900["periodos"].append(d)
                subapuracoes_periodos.append(d)

        elif reg == "1920":
            current_1920 = d
            current_1920["ajustes"] = []
            current_1920["obrigacoes"] = []
            subapuracoes_resumo.append(current_1920)
            if current_1900 is not None:
                current_1900.setdefault("resumos", []).append(current_1920)

        elif reg == "1921":
            if current_1920 is None:
                d["_erro"] = "1921_sem_1920"
                subapuracoes_ajustes.append(d)
            else:
                current_1920["ajustes"].append(d)
                subapuracoes_ajustes.append(d)
            current_1921 = d

        elif reg == "1922":
            if current_1920 is None:
                d["_erro"] = "1922_sem_1920"
                subapuracoes_obrigacoes.append(d)
            else:
                current_1920["obrigacoes"].append(d)
                subapuracoes_obrigacoes.append(d)

        elif reg == "1923":
            if current_1921 is None:
                d["_erro"] = "1923_sem_1921"
                subapuracoes_obrigacoes.append(d)
            else:
                current_1921.setdefault("docs", []).append(d)
                subapuracoes_obrigacoes.append(d)

        elif reg == "1925":
            subapuracoes_resumo.append(d)

        elif reg == "1926":
            subapuracoes_obrigacoes.append(d)

        elif reg == "1960":
            current_1960 = d
            current_1960["importacoes"] = []
            current_1960["devolucoes"] = []
            subapuracoes.append(current_1960)

        elif reg == "1970":
            if current_1960 is None:
                d["_erro"] = "1970_sem_1960"
                subapuracoes.append(d)
            else:
                current_1960["importacoes"].append(d)
            current_1970 = d

        elif reg == "1975":
            if current_1970 is None:
                d["_erro"] = "1975_sem_1970"
                subapuracoes.append(d)
            else:
                current_1970.setdefault("saidas", []).append(d)

        elif reg == "1980":
            if current_1960 is None:
                d["_erro"] = "1980_sem_1960"
                subapuracoes.append(d)
            else:
                current_1960["devolucoes"].append(d)

        elif reg == "1990":
            fechamento_bloco_1 = d

        elif reg == "9001":
            abertura_bloco_9 = d

        elif reg == "9900":
            registros_9900.append(d)

        elif reg == "9990":
            fechamento_bloco_9 = d

        elif reg == "9999":
            fechamento_sped = d

        elif reg == "D200":
            current_d200 = d
            current_d200["pis"] = None
            current_d200["cofins"] = None
            transportes_resumo.append(current_d200)

        elif reg == "D201":
            if current_d200 is None:
                d["_erro"] = "D201_sem_D200"
                transportes_resumo.append({"_erro": "D200_ausente", "pis": d, "cofins": None})
            else:
                current_d200["pis"] = d

        elif reg == "D205":
            if current_d200 is None:
                d["_erro"] = "D205_sem_D200"
                transportes_resumo.append({"_erro": "D200_ausente", "pis": None, "cofins": d})
            else:
                current_d200["cofins"] = d
    return {
        "abertura": abertura,
        "abertura_bloco0": abertura_bloco0,
        "abertura_bloco_e": abertura_bloco_e,
        "classificacoes": classificacoes,
        "dados_complementares": dados_complementares,
        "substitutos_uf": substitutos_uf,
        "contabilistas": contabilistas,
        "participantes": participantes,
        "historico_participantes": historico_participantes,
        "unidades": unidades,
        "conversoes": conversoes,
        "bens": bens,
        "natureza_operacao": natureza_operacao,
        "info_complementar": info_complementar,
        "observacoes_lancamento": observacoes_lancamento,
        "plano_contas": plano_contas,
        "centros_custos": centros_custos,
        "complementos_c176": complementos_c176,
        "complementos_c177": complementos_c177,
        "complementos_c185": complementos_c185,
        "complementos_c186": complementos_c186,
        "analiticos_c190": analiticos_c190,
        "fcp_c191": fcp_c191,
        "observacoes_c195": observacoes_c195,
        "ajustes_c197": ajustes_c197,
        "resumos_c350": resumos_c350,
        "ecf": ecf,
        "documentos_ecf": documentos_ecf,
        "servicos": servicos,
        "consolidacoes": consolidacoes,
        "cfe": cfe,
        "bilhetes": bilhetes,
        "ecf_d350": ecf_d350,
        "bpe": bpe,
        "bpe_simplificado": bpe_simplificado,
        "resumo_transporte": resumo_transporte,
        "telecom": telecom,
        "telecom_resumo": telecom_resumo,
        "energia_comunicacao_resumo": energia_comunicacao_resumo,
        "gas": gas,
        "gas_resumo_clas": gas_resumo_clas,
        "gas_icms_outra_uf": gas_icms_outra_uf,
        "gas_resumo_mensal": gas_resumo_mensal,
        "gas_resumo_st": gas_resumo_st,
        "abertura_bloco_g": abertura_bloco_g,
        "g_resumos": g_resumos,
        "g_bens": g_bens,
        "g_saldos": g_saldos,
        "g_docs": g_docs,
        "g_icms_util": g_icms_util,
        "abertura_bloco_h": abertura_bloco_h,
        "inventario": inventario,
        "inventario_itens": inventario_itens,
        "inventario_impostos": inventario_impostos,
        "inventario_complemento": inventario_complemento,
        "fechamento_bloco_h": fechamento_bloco_h,
        "abertura_bloco_k": abertura_bloco_k,
        "k_periodos": k_periodos,
        "k_estoques": k_estoques,
        "k_desmontagens": k_desmontagens,
        "k_movimentacoes": k_movimentacoes,
        "k_producoes": k_producoes,
        "k_insumos": k_insumos,
        "k_industrializacao_terceiros": k_industrializacao_terceiros,
        "k_industrializacao_insumos": k_industrializacao_insumos,
        "k_reprocesso": k_reprocesso,
        "k_reprocesso_insumos": k_reprocesso_insumos,
        "k_correcao_ordem": k_correcao_ordem,
        "k_correcao_insumos": k_correcao_insumos,
        "k_correcao_estoque": k_correcao_estoque,
        "k_producao_conjunta": k_producao_conjunta,
        "k_producao_conjunta_itens": k_producao_conjunta_itens,
        "k_producao_conjunta_insumos": k_producao_conjunta_insumos,
        "k_producao_terceiros": k_producao_terceiros,
        "k_producao_terceiros_itens": k_producao_terceiros_itens,
        "k_producao_terceiros_insumos": k_producao_terceiros_insumos,
        "fechamento_bloco_k": fechamento_bloco_k,
        "abertura_bloco_1": abertura_bloco_1,
        "obrigatoriedades_1010": obrigatoriedades_1010,
        "exportacoes_1100": exportacoes_1100,
        "exportacoes_docs": exportacoes_docs,
        "creditos_icms": creditos_icms,
        "creditos_icms_utilizacao": creditos_icms_utilizacao,
        "creditos_icms_rest": creditos_icms_rest,
        "creditos_icms_rest_det": creditos_icms_rest_det,
        "combustiveis_mov": combustiveis_mov,
        "combustiveis_tanques": combustiveis_tanques,
        "combustiveis_bicos": combustiveis_bicos,
        "usina_controle": usina_controle,
        "usina_insumos": usina_insumos,
        "valor_adicionado": valor_adicionado,
        "energia_interestadual": energia_interestadual,
        "energia_itens": energia_itens,
        "pagamentos_eletronicos": pagamentos_eletronicos,
        "documentos_utilizados": documentos_utilizados,
        "documentos_cancelados": documentos_cancelados,
        "transporte_aereo": transporte_aereo,
        "subapuracoes": subapuracoes,
        "subapuracoes_periodos": subapuracoes_periodos,
        "subapuracoes_resumo": subapuracoes_resumo,
        "subapuracoes_ajustes": subapuracoes_ajustes,
        "subapuracoes_obrigacoes": subapuracoes_obrigacoes,
        "abertura_bloco_9": abertura_bloco_9,
        "registros_9900": registros_9900,
        "fechamento_bloco_9": fechamento_bloco_9,
        "fechamento_sped": fechamento_sped,
        "complementos_d130": complementos_d130,
        "complementos_d140": complementos_d140,
        "complementos_d150": complementos_d150,
        "complementos_d160": complementos_d160,
        "complementos_d161": complementos_d161,
        "complementos_d162": complementos_d162,
        "complementos_d170": complementos_d170,
        "complementos_d180": complementos_d180,
        "analiticos_d190": analiticos_d190,
        "observacoes_d195": observacoes_d195,
        "ajustes_d197": ajustes_d197,
        "e_periodos_icms": e_periodos_icms,
        "e_apuracoes_icms": e_apuracoes_icms,
        "e_ajustes_icms": e_ajustes_icms,
        "e_obrigacoes_icms": e_obrigacoes_icms,
        "e_info_doc_icms": e_info_doc_icms,
        "e_info_adic_icms": e_info_adic_icms,
        "e_recolhimentos_icms": e_recolhimentos_icms,
        "e_periodos_st": e_periodos_st,
        "e_apuracoes_st": e_apuracoes_st,
        "e_ajustes_st": e_ajustes_st,
        "e_info_doc_st": e_info_doc_st,
        "e_recolhimentos_st": e_recolhimentos_st,
        "e_periodos_dif": e_periodos_dif,
        "e_apuracoes_dif": e_apuracoes_dif,
        "e_ajustes_dif": e_ajustes_dif,
        "e_obrigacoes_dif": e_obrigacoes_dif,
        "e_info_doc_dif": e_info_doc_dif,
        "e_recolhimentos_dif": e_recolhimentos_dif,
        "e_ipi": e_ipi,
        "e_ipi_detalhes": e_ipi_detalhes,
        "e_ipi_saldo": e_ipi_saldo,
        "e_ipi_ajustes": e_ipi_ajustes,
        "e_ipi_recolhimentos": e_ipi_recolhimentos,
        "abertura_bloco_1": abertura_bloco_1,
        "fechamento_bloco_1": fechamento_bloco_1,
        "abertura_bloco_9": abertura_bloco_9,
        "registros_9900": registros_9900,
        "fechamento_bloco_9": fechamento_bloco_9,
        "fechamento_sped": fechamento_sped,
        "fechamento_bloco0": fechamento_bloco0,
        "abertura_bloco_b": abertura_bloco_b,
        "fechamento_bloco_b": fechamento_bloco_b,
        "abertura_bloco_c": abertura_bloco_c,
        "fechamento_bloco_c": fechamento_bloco_c,
        "abertura_bloco_d": abertura_bloco_d,
        "fechamento_bloco_d": fechamento_bloco_d,
        "fechamento_bloco_h": fechamento_bloco_h,
        "itens": itens,
        "notas": notas,
        "transportes": transportes,
        "transportes_resumo": transportes_resumo,
        "contadores": contadores,
    } 