EXTRAIR CÓDIGO - REG SPEDS
# Abertura do SPED
# Bloco 0
  ## - 0000 - Informações do contribuinte
   ## 1 - 0001 - abertura do Bloco 0
   ### (Identificação do contribuinte)
	2 - 0002 - Classificação do estabelecimento industrial
	2 - 0005 - Dados complementares da entidade
	2 - 0015 - Dados do contribuinte substituto ou responsável pelo ICMS destino
	2 - 0100 - Dados do contabilista
	2 - 0150 - Tabela de cadastro do participante
		3 - 0175 - Alteração da Tabela de Cadastro de Participante
	2 - 0190 - Identificação das Unidades de Medida
	2 - 0200 - Tabela de identificação do item (produto e serviços)
		3 - 0205 - Alteração do item
		3 - 0206 - Código de produto conforme Tabela publicada pela ANP 
		3 - 0220 - Fatores de conversão de unidades
		3 - 0221 - Correlação entre códigos de itens comercializados
	2 - 0400 - Tabela de Natureza da Operação/Prestação
	2 - 0450 - Tabela de Informação Complementar do Documento Fiscal
	2 - 0460 - Tabela de Observações do Lançamento Fiscal
	2 - 0300 - Cadastro de bens ou componentes do Ativo Imobilizado
		3 - 0305 - Informação sobre a utilização do bem
	2 - 0500 - Plano de Contas Contábeis
	2 - 0600 - Centro de Custos
   ### - 0990 - encerramento do Bloco 0

# Bloco B
## - B001 - Abertura Bloco B - Somente vigente no DF para apuração de ISS
 ### (Apuração do ISS no DF)
    2 - B020 - Nota Fiscal (código 01), Nota Fiscal de Serviços (código 03), Nota Fiscal de Serviços Avulsa (código 3B), Nota Fiscal de Produtor (código 04), Conhecimento de Transporte Rodoviário de Cargas (código 08), NF-e (código 55) e NFC-e (código 65)
        3 - B025 - Detalhamento por combinação de alíquota e item da lista de serviços da Lei Complementar nº 116/2003
    2 - B030 - Nota fiscal de Serviços Simplificada (código 3A)
    2 - B035 - Detalhamento por combinação de alíquota e item da lista de serviços da Lei Complementar nº 116/2003
    2 - B350 - Serviços prestados por insituições financeiras
    2 - B420 - Totalização dos valores de serviços prestados por combinação de alíquota e item da lista de serviços da Lei Complementar nº 116/2003
    2 - B440 - Totalização dos valores retidos
    2 - B460 - Deduções do ISS
    2 - B470 - Deduções do ISS
    2 - B500 - Apuração do ISS sociedade uniprofissional
        3 - B510 - Uniprofissional – empregados e sócios
## - B990 - Fechamento Bloco B - Somente vigente no DF para apuração de ISS

# Bloco C
## - C001 - Abertura do Bloco C
 ### (Doumentos de Entrada/Saida)
	2 - C100 - Documento - Nota Fiscal (código 01), Nota Fiscal Avulsa (código 1B), Nota Fiscal de Produtor (código 04), Nota Fiscal Eletrônica (código 55) e Nota Fiscal Eletrônica para Consumidor Final (código 65)
	    3 - C101 - Informação complementar dos documentos fiscais quando das operações interestaduais destinadas a consumidor final não contribuinte EC 87/15 (Código 55)
	    3 - C105 - Operações com ICMS ST recolhido para UF diversa do destinatário do documento fiscal (Código 55)
	    3 - C110 - Complemento de Documento - Informação Complementar da Nota Fiscal (código 01, 1B, 55)
		    4 - C111 - Complemento de Documento - Processo referenciado
		    4 - C112 - Complemento de Documento - Documento de Arrecadação Referenciado
		    4 - C113 - Complemento de Documento - Documento Fiscal Referenciado
		    4 - C114 - Complemento de Documento - Cupom Fiscal Referenciado
            4 - C115 - Local de coleta e/ou entrega (CÓDIGOS 01, 1B e 04)
		    4 - C116 - Cupom Fiscal Eletrônico - CF-e referenciado
	    3 - C120 - Complemento de Documento - Operações de Importação (código 01 e 55)
        3 - C130 - Complemento de Documento - ISSQN, IRRF e Previdência Social
        3 - C140 - Complemento de Documento - Fatura (código 01)
            4 - C141 -  Complemento de Documento - Vencimento da Fatura (código 01)
        3 - C160 - Complemento de Documento - Volumes Transportados (código 01 e 04) Exceto Combustíveis
            4 - C165 -  Complemento de Documento - Operações com combustíveis (código 01)
	    3 - C170 - Complemento de Documento - Itens do Documento (código 01, 1B, 04 55)
		    4 - C171 - Complemento de Item - Armazenamento de Combustíveis (código 01,55)
		    4 - C172 - Complemento de Item - Operações com ISSQN (código 01)
            4 - C173 - Complemento de Item - Operações com Medicamentos (código 01,55)
            4 - C174 - Complemento de Item - Operações com Armas de Fogo (código 01)
		    4 - C175 - Complemento de Item - Operações com Veículos Novos (código 01,55)
		    4 - C176 - Complemento de Item - Ressarcimento de ICMS em operações com Substituição Tributária (código 01,55)
		    4 - C177 - Complemento de Item - Operações com Produtos Sujeitos a Selo de Controle IPI (código 01)
            4 - C178 - Complemento de Item - Operações com Produtos Sujeitos a Tributação de IPI por Unidade ou Quantidade de produto
            4 - C179 - Complemento de Item - Informações Complementares ST (código 01)
		    4 - C180 - Informações complementares das operações de entrada de mercadorias sujeitas à substituição tributária (Código 01, 1B, 04 e 55)	
		    4 - C181 - Informações complementares das operações de devolução de saídas de mercadorias sujeitas à substituição tributária (Código 01, 1B, 04 e 55)
	    3 - C185 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (Código 01, 1B, 04, 55 e 65)
	    3 - C186 - Informações complementares das operações de devolução de entradas de mercadorias sujeitas à substituição tributária (Código 01, 1B, 04 e 55)
	    3 - C190 - Registro Analítico do Documento (código 01, 1B, 04, 55 e 65)
		    4 - C191 - Informações do Fundo de Combate à Pobreza - FCP - na NF-e (código 55) e na NFC-e (código 65)
	    3 - C195 - Complemento do Registro Analítico - Observações do Lançamento Fiscal (código 01, 1B, 04 e 55)
		    4 - C197 - Outras Obrigações Tributárias, Ajustes e Informações provenientes de Documento Fiscal
 ### (Resumo Diário das NF de Venda a Consumidor)
	2 - C300 - Documento - Resumo Diário das Notas Fiscais de Venda a Consumidor (código 02)
	2 - C310 - Documentos Cancelados de Nota Fiscal de Venda a Consumidor (código 02)
	2 - C320 - Registro Analítico das Notas Fiscais de Venda a Consumidor (código 02)
		3 -C321 - Itens dos Resumos Diários dos Documentos (código 02)
		    4 -C330 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (Código 02)
 ### (NF de venda a Consumidor)
 	2 - C350 - Nota Fiscal de venda a consumidor (código 02)
		3 - C370 - Itens do documento (código 02)
			4 - C380 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (Código 02)
		3 - C390 - Registro Analítico das Notas Fiscais de Venda a Consumidor (código 02)
 ### (Equipamento ECF - NF de venda a Consumidor)
	2 - C400 - Equipamento ECF (código 02, 2D e 60)
		3 - C405 - Redução Z (código 02, 2D e 60)
			4 - C410 - PIS e COFINS Totalizados no Dia (código 02 e 2D)
			4 - C420 - Registro dos Totalizadores Parciais da Redução Z (código 02, 2D e 60)
                5 - C425 - Resumo de itens do movimento diário (código 02 e 2D)
                    6 - C430 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (Código 02, 2D e 60)
			4 - C460 - Documento Fiscal Emitido por ECF (código 02, 2D e 60)
                5 - C465 - Complemento do Cupom Fiscal Eletrônico Emitido por ECF - CF-e-ECF (código 60)
			    5 - C470 - Itens do Documento Fiscal Emitido por ECF (código 02 e 2D)
			        6 - C480 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (Código 02, 2D e 60)
			4 - C490 - Registro Analítico do movimento diário (código 02, 2D e 60)
    2 - C495 - Resumo Mensal de Itens do ECF por Estabelecimento (código 02 e 2D e 2E)
 ### (NF/Conta Energia Elétrica, Gás e Água)
	2 - C500 - Nota Fiscal/Conta de Energia Elétrica (código 06), Nota Fiscal/Conta de fornecimento dágua canalizada (código 29) e Nota Fiscal/Consumo Fornecimento de Gás (Código 28)
        3 - C510 - Itens do Documento - Nota Fiscal/Conta de Energia Elétrica (código 06), Nota Fiscal/Conta de fornecimento dágua canalizada (código 29) e Nota Fiscal/Conta Fornecimento de Gás (Código 28)
		3 - C590 - Registro Analítico do Documento - Nota Fiscal/Conta de Energia Elétrica (código 06), Nota Fiscal/Conta de fornecimento dágua canalizada (código 29) e Nota Fiscal/Conta Fornecimento de Gás (Código 28)
			4 - C591 - Informações do Fundo de Combate à Pobreza – FCP na NF3e (Código 66)
		3 - C595 - Observações do lançamento fiscal (Códigos 06, 28, 29 e 66)
			4 - C597 - Outras obrigações tributárias, ajustes e informações de valores provenientes de documento fiscal
 ### (Energia Elétrica/Água/Gás - NF consolidadas)
	2 - C600 - Consolidação Diária de Notas Fiscais/Contas de Energia Elétrica (Código 06), Nota Fiscal/Conta de Fornecimento d´água (código 29) e Nota Fiscal/Conta de Fornecimento de Gás (Código 28) - (Empresas não obrigadas ao Convênio ICMS 115/03)
		3 - C601 - Documentos cancelados - Consolidação diária de notas fiscais/conta de energia elétrica (Código 06), nota fiscal/conta de fornecimento de água (código 29) e nota fiscal/conta de fornecimento de gás (código 28)
		3 - C610 - Itens do Documento Consolidado - Notas Fiscais/Contas de Energia Elétrica (Código 06), Nota Fiscal/Conta de Fornecimento d´água (código 29) e Nota Fiscal/Conta de Fornecimento de Gás (Código 28) - (Empresas não obrigadas ao Convênio ICMS 115/03)
		3 - C690 - Registro Analítico dos Documentos - Notas Fiscais/Contas de Energia Elétrica (Código 06), Nota Fiscal/Conta de Fornecimento d´água (código 29) e Nota Fiscal/Conta de Fornecimento de Gás (Código 28)
 ### (Energia Elétrica/Gás - NF em Via Uníca (Convênio ICMS 115/03))
	2 - C700 - Consolidação dos Documentos Nota Fiscal/Conta Energia Elétrica (código 06) emitidas em via única - (Empresas obrigadas à entrega do arquivo previsto no Convênio ICMS 115/03) e Nota Fiscal/Conta de Fornecimento de Gás Canalizado (Código 28)
		3 - C790 - Registro Analítico dos Documentos - Nota Fiscal/Conta Energia Elétrica (código 06) emitidas em via única
			4 - C791 - Registro de Informações de ICMS ST por UF
 ### (Cupom Fiscal Eletrônico - SAT)
	2 - C800 - Registro Cupom Fiscal Eletrônico - CF-e (Código 59)
		3 - C810 - Itens do documento do Cupom Fiscal Eletrônico – SAT (CFE-SAT) (Código 59)
			4 - C815 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (CF-E-SAT) (Código 59)
		3 - C850 - Registro analítico do CF-e-SAT (Código 59)
		3 - C855 - Observações do lançamento fiscal (Código 59)
			4 - C857 - Outras obrigações tributárias, ajustes e informações de valores provenientes de documento fiscal
 ### (Equipamento SAT-CF-e)
	2 - C860 - Identificação do Equipamento SAT-CF-e
		3 - C870 - Itens do resumo diário dos documentos (CF-E-SAT) (Código 59)
			4 - C880 - Informações complementares das operações de saída de mercadorias sujeitas à substituição tributária (CF-E-SAT) (Código 59)
		3 - C890 - Resumo Diário do CF-e-SAT (Código 59) por Equipamento SAT-CF-e
        3 - C895 - Registro C895 da EFD-ICMS/IPI - Observações do lançamento fiscal(Código 59) 
			4 - C897 - Outras obrigações tributárias, ajustes e informações de valores provenientes de documento fiscal
## - C990 - Encerramento do Bloco C
# Bloco D
 ## - D001 - Abertura do Bloco D
 ### (Documentos Fiscais de Transportes)
	2 - D100 - Nota Fiscal de Serviço de Transporte (código 07) e Conhecimentos de Transporte Rodoviário de Cargas (código 08), Conhecimento de Transporte de Cargas Avulso (Código 8B), Aquaviário de Cargas (código 09), Aéreo (código 10), Ferroviário de Cargas (código 11) e Multimodal de Cargas (código 26) e Nota Fiscal de Transporte Ferroviário de Cargas (código 27) e Conhecimento de Transporte Eletrônico - CT-e (código 57)
		3 - D101 - Informação complementar dos documentos fiscais quando das prestações interestaduais destinadas a consumidor final não contribuinte EC 87/15 (código 57)
		3 - D105 - 
        3 - D110 - Itens do documento - Nota Fiscal de Serviços de Transporte (código 07)
            4 - D120 - Complemento da Nota Fiscal de Serviços de Transporte (código 07)
		3 - D130 - Complemento do Conhecimento Rodoviário de Cargas (código 08) e Conhecimento de Transporte de Cargas Avulso (Código 8B)
		3 - D140 - Complemento do Conhecimento Aquaviário de Cargas (código 09)
        3 - D150 - Complemento do Conhecimento Aéreo de Cargas (código 10)
        3 - D160 - Carga Transportada (Código 08, 8B, 09, 10, 11, 26 E 27)
            4 - D161 - Local de Coleta e Entrega (códigos 08, 8B, 09, 10, 11 e 26)
            4 - D162 - Identificação dos documentos fiscais (código 08, 8B, 09, 10, 11, 26 e 27)
        3 - D170 - Complemento do Conhecimento Multimodal de Cargas (código 26)
        3 - D180 - Modais (código 26)
        3 - D190 - Registro Analítico dos Documentos (Código 07, 08, 8B, 09, 10, 11, 26, 27 e 57)
		3 - D195 - Observações do lançamento (Código 07, 08, 8B, 09, 10, 11, 26, 27 e 57)
			4 - D197 - Outras obrigações tributárias, ajustes e informações de valores provenientes do documento fiscal
 ### (Analítico de Bilhetes de Passageiros)
	2 - D300 - Registro Analítico dos bilhetes consolidados de Passagem Rodoviário (código 13), de Passagem Aquaviário (código 14), de Passagem e Nota de Bagagem (código 15) e de Passagem Ferroviário (código 16)
		3 - D301 - Documentos cancelados dos Bilhetes de Passagem Rodoviário (código 13), de Passagem Aquaviário (código 14), de Passagem e Nota de Bagagem (código 15) e de Passagem Ferroviário (código 16)
		3 - D310 - Complemento dos Bilhetes (código 13, código 14, código 15 e código 16)

 ### (Equipamento ECF - Prestação de Serviços)
	2 - D350 - Equipamento ECF (Códigos 2E, 13, 14, 15 e 16)
		3 - D355 - Redução Z (Códigos 2E, 13, 14, 15 e 16)
			4 - D360 - PIS E COFINS totalizados no dia (Códigos 2E, 13, 14, 15 e 16)
			4 - D365 - Registro dos Totalizadores Parciais da Redução Z (Códigos 2E, 13, 14, 15 e 16)
				5 - D370 - Complemento dos documentos informados (Códigos 13, 14, 15, 16 E 2E)
			4 - D390 - Registro analítico do movimento diário (Códigos 13, 14, 15, 16 E 2E)
 ### (Resumo de Movimento Diário)
	2 - D400 - Resumo do Movimento Diário (código 18)
		3 - D410 - Documentos Informados (Códigos 13, 14, 15 e 16)
			4 - D411 - Documentos Cancelados dos Documentos Informados (Códigos 13, 14, 15 e 16)
		3 - D420 - 	Complemento dos Documentos Informados (Códigos 13, 14, 15 e 16)
 ### (NF de Comunicação e de Telecomunicação)
	2 - D500 - Nota Fiscal de Serviço de Comunicação (código 21) e Serviço de Telecomunicação (código 22)
		3 - D510 - Itens do Documento - Nota Fiscal de Serviço de Comunicação (código 21) e Serviço de Telecomunicação (código 22)
		3 - D530 - Terminal Faturado
		3 - D590 - Registro Analítico do Documento (códigos 21 e 22)
 ### (NF de Comunicação e de Telecomunicação Consolidada)
	2 - D600 - Consolidação da Prestação de Serviços - Notas de Serviço de Comunicação (código 21) e de Serviço de Telecomunicação (código 22)
		3 - D610 - Itens do Documento Consolidado (códigos 21 e 22)
		3 - D690 - Registro Analítico dos Documentos (códigos 21 e 22)
 ### (NF de Comunicação e de Telecomunicação Consolidada - Convênio 115)
	2 - D695 - Consolidação da Prestação de Serviços - Notas de Serviço de Comunicação (código 21) e de Serviço de Telecomunicação (código 22)
		3 - D696 - Registro Analítico dos Documentos (códigos 21 e 22)
			4 - D697 - Registro de informações de outras UFs, relativamente aos serviços “não-medidos” de televisão por assinatura via satélite
 ### (NF Fatura Eletrônica de Serviços de Comunicação - NFCom (CÓDIGO 62))
	2 - D700 - Nota Fiscal Fatura Eletrônica de serviços de comunicação - NFCom (Código 62)
		3 - D730 - Registro analítico Nota Fiscal Fatura Eletrônica de serviços de comunicação – NFCom (Código 62)
			4 - D731 - Informações do Fundo de Combate à Pobreza - FCP - (Código 62)
		3 - D735 - 	Observações do lançamento fiscal (Código 62)
			4 - D737 - Outras obrigações tributárias, ajustes e informações de valores provenientes de documento fiscal
 ### (Escrituração Consolidada da NF Fatura Eletrônica de Serviços de Comunicação - NFCom)
	2 - D750 - Escrituração consolidada da Nota Fiscal Fatura Eletrônica de serviços de comunicação - NFCom (Código 62)
		3 - D760 - Registro analítico da escrituração consolidada da Nota Fiscal Fatura Eletrônica de serviços de comunicação - NFCom (Código 62)
			4 - D761 - Informações do Fundo de Combate à Pobreza – FCP – (Código 62)

{X} - D200 - NÃO EXISTE NO SPED FISCAL
{X} - D201 - NÃO EXISTE NO SPED FISCAL
{X} - D205 - NÃO EXISTE NO SPED FISCAL
 ## - D990 - Fechamento do Bloco D
# Bloco E
 ## - E001 - Abertura do Bloco E
 ### (ICMS Próprio)
	2 - E100 - Período de Apuração do ICMS
		3 - E110 - Apuração do ICMS - Operações Próprias
			4 - E111 - 	Ajuste/Benefício/Incentivo da Apuração do ICMS
				5 - E112 - 	Informações Adicionais dos Ajustes da Apuração do ICMS
				5 - E113 - 	Informações Adicionais dos Ajustes da Apuração do ICMS - Identificação dos documentos fiscais
			4 - E115 - 	Informações Adicionais da Apuração do ICMS - Valores Declaratórios
			4 - E116 - Obrigações do ICMS Recolhido ou a Recolher - Obrigações Próprias
 ### (ICMS por Substituição Tributária)
	2 - E200 - 	Período de Apuração do ICMS - Substituição Tributária
		3 - E210 - 	Apuração do ICMS - Substituição Tributária
			4 - E220 - Ajuste/Benefício/Incentivo da Apuração do ICMS - Substituição Tributária
				5 - E230 - Informações Adicionais dos Ajustes da Apuração do ICMS Substituição Tributária
				5 - E240 - Informações Adicionais dos Ajustes da Apuração do ICMS Substituição Tributária - Identificação dos documentos fiscais
			4 - E250 - 	Obrigações do ICMS Recolhido ou a Recolher - Substituição Tributária
 ### (ICMS diferencial alíquota origem/destino EC 87/15)
	2 - E300 - Período de Apuração do ICMS Diferencial de Alíquota - UF Origem/Destino EC 87/15
		3 - E310 - 	Apuração do ICMS Diferencial de Alíquota - UF Origem/Destino EC 87/15
			4 - E311 - 	Ajuste/Benefício/Incentivo da Apuração do ICMS Diferencial de Alíquota - UF Origem/Destino EC 87/15
				5 - E312 - 	Informações Adicionais dos Ajustes da Apuração do ICMS Diferencial de Alíquota - UF Origem/Destino EC 87/15
				5 - E313 - Informações Adicionais da Apuração do ICMS Diferencial de Alíquota - UF Origem/Destino EC 87/15 Identificação dos Documentos Fiscais
			4 - E316 - Obrigações do ICMS recolhido ou a recolher - Diferencial de Alíquota - UF Origem/Destino EC 87/15
 ### (IPI)
	2 - E500 - 	Período de Apuração do IPI
		3 - E510 - Consolidação dos Valores de IPI
		3 - E520 - Apuração do IPI
			4 - E530 - Ajustes da Apuração do IPI
				5 - E531 - Informações adicionais dos ajustes da apuração do IPI - Identificação dos documentos fiscais (01 e 55)
 ## - E990 - Fechamento do Bloco E
# Bloco G
 ## - G001 - Abertura do Bloco G
 ### (ICMS - Ativo Permanente - CIAP)
	- G110
		- G125
			- G126
			- G130
				- G140
 ## - G990 - Fechamento do Bloco G
# Bloco H
 ## - H001 - Abertura do Bloco H
 ### (Inventário Fisico)
	2 - H005 - Totais do Inventário
		3 - H010 - Inventário
			4 - H020 - Informação complementar do Inventário
			4 - H030 - Informações complementares do inventário das mercadorias sujeitas ao regime de substituição tributária
 ## - H990 - Fechamento do Bloco H
# Bloco K
 ## - K001 - Abertura do Bloco K
 ### (Produção e Estoque - RCPE)
	2 - K010 - Informação sobre o tipo de leiaute (simplificado / completo)
	2 - K100 - 	Período de Apuração do ICMS/IPI
		3 - K200 - Estoque Escriturado
		3 - K210 - Desmontagem de mercadorias - Item de origem
			4 - K215 - Desmontagem de mercadorias - Item de destino
		3 - K220 - Outras Movimentações Internas entre Mercadorias
		3 - K230 - Itens Produzidos 
			4 - K235 - Insumos Consumidos
		3 - K250 - 	Industrialização Efetuada por Terceiros - Itens Produzidos
			4 - K255 - Industrialização em Terceiros - Insumos Consumidos
		3 - K260 - Reprocessamento/reparo de produto/insumo
			4 - K265 - Reprocessamento/reparo - Mercadorias consumidas e/ou retornadas
		3 - K270 - Correção de apontamento dos Registros K210, K220, K230, K250, K260, K291, K292, K301 e K302
			4 - K275 - Correção de apontamento e retorno de insumos dos Registros K215, K220, K235, K255 e K265
		3 - K280 - Correção de apontamento - Estoque escriturado
		3 - K290 - Produção conjunta - Ordem de Produção
			4 - K291 - Produção conjunta - Itens produzidos
			4 - K292 - Produção conjunta - Insumos consumidos
		3 - K300 - Produção conjunta - Industrialização efetuada por terceiros
			4 - K301 - Produção conjunta - Industrialização efetuada por terceiros - Itens produzidos
			4 - K302 - Produção conjunta - Industrialização efetuada por terceiros - Insumos consumidos
 ## - K990 - Fechamento do Bloco K
# Bloco 1
 ## - 1001 - Abertura do Bloco 1
 ### (Obrigatoriedade de Registros do Bloco 1)
	2 - 1010 - Obrigatoriedade de registros do Bloco 1
 ### (Exportação)
	2 - 1100 - Registro de Informações sobre Exportação
		3 - 1105 - Documentos Fiscais de Exportação
		3 - 1110 - Operações de Exportação Indireta - Mercadorias de terceiros
 ### (Créditos Fiscais)
	2 - 1200 - Controle de Créditos Fiscais - ICMS
		3 - 1210 - Utilização de Créditos Fiscais - ICMS
 ### (Restituição, Ressarcimento e Complementação do ICMS Registro)
	2 - 1250 - Informações consolidadas de saldos de restituição, ressarcimento e complementação do ICMS
		3 - 1255 - Informações consolidadas de saldos de restituição, ressarcimento e complementação do ICMS por motivo
 ### (Combustiveis)
	2 - 1300 - Movimentação diária de combustíveis
		3 - 1310 - Movimentação diária de combustíveis por tanque
			4 - 1320 - 	Volume de vendas
	2 - 1350 - Bombas
		3 - 1360 - Lacres das bombas
		3 - 1370 - Bicos da bomba
 ### (Controle de Produção de Usina)
	2 - 1390 - Controle de produção de Usina
		3 - 1391 - Produção diária da usina
 ### (Valores Agregados)
	2 - 1400 - 	Informação sobre Valor Agregado
 ### (Saidas Interestaduais - Energia Elétrica)
	2 - 1500 - Nota Fiscal/Conta de energia elétrica (código 06) - Operações Interestaduais
		3 - 1510 - Itens do documento Nota Fiscal/Conta de energia elétrica (código 06)
 ### (Operações com Instrumentos de Pagamentos Eletrônicos)
    2 - 1600 - Total das operações com cartão de crédito e/ou débito
	2 - 1601 - Operações com instrumentos de pagamentos eletrônicos
 ### (Doc. Fiscais Utilizados)
	2 - 1700 - Documentos fiscais utilizados
		3 - 1710 - Documentos fiscais cancelados/inutilizados
 ### (Demonstrativos de Crédito ICMS)
	2 - 1800 - DCTA - Demonstrativo de crédito do ICMS sobre transporte aéreo
 ### (Outras Apurações)
	2 - 1900 - Indicador de sub-apuração do ICMS
		3 - 1910 - Período da sub-apuração do ICMS
			4 - 1920 - Sub-apuração do ICMS
				5 - 1921 - Ajuste/benefício/incentivo da sub-apuração do ICMS
					6 - 1922 - 	Informações adicionais dos ajustes da sub-apuração do ICMS
					6 - 1923 - Informações adicionais dos ajustes da sub-apuração do ICMS - Identificação dos documentos fiscais
				5 - 1925 - Informações adicionais da sub-apuração do ICMS - Valores declaratórios
				5 - 1926 - Obrigações do ICMS a recolher - Operações referentes à sub-apuração do ICMS
 ### (Indústria (Crédito Presumido))
	2 - 1960 - 	Guia de Informação e Apuração de incentivos Fiscais e Financeiros: Indústria (Crédito presumido)
 ### (Importação(Diferimento na Entrada e Crédito Presumido na Saida Subsequente))
	2 - 1970 - GIAF 3 - Guia de Informação e Apuração de incentivos Fiscais e Financeiros: Importação (Diferimento na entrada e crédito presumido na saída subsequente)
		3 - 1975 - 	Guia de Informação e Apuração de Incentivos Fiscais e Financeiros: Importação (Saídas intermas por faixa de alíquota)
 ### (Central de Distribuição (Entradas/Saidas))
	2 - 1980 - GIAF 4 - Guia de Informação e Apuração de Incentivos Fiscais e Financeiros: Central de distribuição (entradas/saídas)
## - 1990 - Fechamento do Bloco 1
# Bloco 9 
## - 9001 - Abertura do Bloco 9
	2 - 9900
	(       Ele é um bloco totalizador por bloco ou seja
	  |9900|Bloco tal|Quantidade de Registros do bloco tal|    )

	2 - 9990 
	(Ele é um bloco que soma todos os 9900 e encerra o bloco 9)
## - 9990 - Fechamento do Bloco 9

# - 9999 - Fechamento do SPED e total de Linhas no arquivo