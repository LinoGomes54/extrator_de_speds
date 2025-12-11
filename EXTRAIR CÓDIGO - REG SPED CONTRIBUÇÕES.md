EXTRAIR CÓDIGO - REG SPEDS FISCAL
# Abertura do SPED
# Bloco 0
  ## - 0000 - Informações do contribuinte
   ## 1 - 0001 - abertura do Bloco 0
   ### (Identificação do contribuinte)
	2 - 0000 - Abertura, Identificação e Referências
	2 - 0035 - Identificação de Sociedade em Conta de Participação – SCP
	2 - 0100 - Dados do Contabilista
	2 - 0110 - Regimes de Apuração da Contribuição Social e de Apropriação de Crédito
		3 - 0111 - Tabela de Receita Bruta Mensal Para Fins de Rateio de Créditos Comuns
	2 - 0120 - Identificação de EFD-Contribuições Sem Dados a Escriturar
		3 - 0140 - Tabela de Cadastro de Estabelecimentos
	2 - 0145 - Regime de Apuração da Contribuição Previdenciária Sobre a Receita Bruta
		3 - 0150 - Tabela de Cadastro do Participante
		3 - 0190 - Identificação das Unidades de Medida
		3 - 0200 - Tabela de Identificação do Item (Produtos e Serviços)
			4 - 0205 - Registro 0205 da EFD-Contribuições - Alteração do Item
			4 - 0206 - Código de Produto Conforme Tabela ANP (Combustíveis)
			4 - 0208 - Código de Grupos por Marca Comercial – Refri (bebidas frias)
		3 - 0400 - Tabela de Natureza da Operação/Prestação
		3 - 0450 - Tabela de Informação Complementar do Documento Fiscal
	2 - 0500 - Plano de Contas Contábeis
	2 - 0600 - Centro de Custos
	2 - 0900 - Composição das Receitas do Período – Receita Bruta e Demais Receitas
   ### - 0990 - encerramento do Bloco 0
# Bloco A
## -  A001 - Abertura do bloco A
	2- A010
		3- A100
			4 - A110 - Identificação do Estabelecimento
			4 - A111 - Processo Referenciado
			4 - A120 - Informação Complementar - Operações de Importação
			4 - A170 - Complemento do Documento - Itens do Documento
## -  A990 - Encerramento do bloco A
# Bloco C
## - C001 - Abertura do Bloco C
 ### (NF, NF Avulsa, NF de Produção)
	2 - C010 - Identificação do Estabelecimento
		3 - C100 - Documento - Nota Fiscal (Código 01), Nota Fiscal Avulsa (Código 1B), Nota Fiscal de Produtor (Código 04), NF-e (Código 55) e NFC-e (Código 65)
			4 - C110 - Complemento do Documento - Informação Complementar da Nota Fiscal (Códigos 01, 1B, 04 e 55) da EFD-Contribuições
			4 - C111 - Processo Referenciado
			4 - C120 - Complemento do Documento - Operações de Importação (Código 01)
			4 - C170 - Complemento do Documento - Itens do Documento (Códigos 01, 1B, 04 e 55)
			4 - C175 - Registro Analítico do Documento (Código 65)
 ### (Consolidação de NF-e Emitidas - Operações de Venda)
		3 - C180 - Consolidação de Notas Fiscais Eletrônicas Emitidas Pela Pessoa Jurídica (Códigos 55 e 65) – Operações de Vendas
			4 - C181 - Detalhamento da Consolidação - Operações de Vendas - PIS/Pasep
			4 - C185 - Detalhamento da Consolidação – Operações de Vendas – Cofins
			4 - C188 - Processo Referenciado
		3 - C190 - Consolidação de Notas Fiscais Eletrônicas (Código 55) – Operações de Aquisição com Direito a Crédito, e Operações de Devolução de Compras e Vendas
			4 - C191 - Detalhamento da Consolidação – Operações de Aquisição Com Direito a Crédito, e Operações de Devolução de Compras e Vendas – PIS/Pasep
			4 - C195 - Detalhamento da Consolidação - Operações de Aquisição Com Direito a Crédito, e Operações de Devolução de Compras e Vendas – Cofins
			4 - C198 - Processo Referenciado
			4 - C199 - Complemento do Documento - Operações de Importação (Código 55)
 ### (Consolição de NF de Venda a Consumidor)
		3 - C380 - Nota Fiscal de Venda a Consumidor (Código 02) - Consolidação de Documentos Emitidos
			4 - C381 - Detalhamento da Consolidação – PIS/Pasep
			4 - C385 - Detalhamento da Consolidação – Cofins
		3 - C395 - Detalhamento da Consolidação – Cofins
			4 - C396 - Itens do Documento (Códigos 02, 2D, 2E, 59, 60 e 65) – Aquisições/Entradas com Crédito
 ### (Equipamento ECF - Saida de Mercadoria)
		3 - C400 - Equipamento ECF (Códigos 02 e 2D)
			4 - C405 - Redução Z (Códigos 02 e 2D)
				5 - C481 - Resumo Diário de Documentos Emitidos por ECF–PIS/Pasep (Código 02 e 2D)
				5 - C485 - Resumo Diário de Documentos Emitidos por ECF – Cofins (Códigos 02 e 2D)
			4 - C489 - Processo Referenciado
 ### (Consolidação de Documentos Emitidos por ECF - Saida de Mercadoria)
		3 - C490 - Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60)
			4 - C491 - Detalhamento da Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60) – PIS/Pasep
			4 - C495 - Detalhamento da Consolidação de Documentos Emitidos por ECF (Códigos 02, 2D, 59 e 60) – Cofins
			4 - C499 - Processo Referenciado
		3 - C500 - Nota Fiscal/Conta de Energia Elétrica (Código 06), Nota Fiscal/Conta de Fornecimento Dágua Canalizada (Código 29) e Nota Fiscal Consumo Fornecimento de Gás (Código 28) e NF-e (Código 55) – Documentos de Entrada/Aquisição com Crédito
			4 - C501 - Complemento da Operação (Códigos 06, 28 e 29) – PIS/Pasep
			4 - C505 - Complemento da Operação (Códigos 06, 28 e 29) – Cofins
			4 - C509 - Processo Referenciado
 ### (Consolidação de Documentos Emitidos por ECF - Saida de Mercadoria)
		3 - C600 - Consolidação Diária de Notas Fiscais/Contas Emitidas de Energia Elétrica (Código 06), Nota Fiscal de Energia Elétrica Eletrônica – NF3e (Código 66), Nota Fiscal/Conta de Fornecimento Dágua Canalizada (Código 29) e Nota Fiscal/Conta de Fornecimento de Gás (Código 28) (Empresas Obrigadas ou não Obrigadas ao Convenio ICMS 115/03) – Documentos de Saída
			4 - C601 - Complemento da Consolidação Diária (Códigos 06, 28 e 29) – Documentos de Saídas - PIS/Pasep
		3 - C605 - Complemento da Consolidação Diária (Códigos 06, 28 e 29) – Documentos de Saídas - PIS/Pasep
			4 - C609 - Processo Referenciado
 ### (Identificação do Equipamento SAT - CF-e)
		3 - C800 - Cupom Fiscal Eletrônico (Código 59)
			4 - C810 - Detalhamento do Cupom Fiscal Eletrônico (Código 59) – PIS/Pasep e Cofins
			4 - C820 - Detalhamento do Cupom Fiscal Eletrônico (Código 59) – PIS/Pasep e Cofins Apurado por Unidade de Medida de Produto
			4 - C830 - Processo Referenciado
			4 - C850
		3 - C860 - Identificação do Equipamento SAT-CF-e
			4 - C870 - Resumo Diário de Documentos Emitidos por Equipamento SAT-Cf-e (Código 59) – PIS/Pasep e Cofins
			4 - C880 - Resumo Diário de Documentos Emitidos por Equipamento SAT-Cf-e (Código 59) – PIS/Pasep e Cofins Apurado por Unidade de Medida de Produto
			4 - C890 - Processo Referenciado
## - C990 - Fechamento do Bloco C
# Bloco D
 ## - D001 - Abertura do Bloco D
 ### (Documentos Fiscais de Transportes)
	2 - D010 - Identificação do Estabelecimento
		3 - D100 - Aquisição de Serviços de Transporte - Nota Fiscal de Serviço de Transporte (Código 07), Conhecimento de Transporte Rodoviário de Cargas (Código 08), Conhecimento de Transporte de Cargas Avulso (Código 8B), Conhecimento de Transporte Aquaviário de Cargas (Código 09), Conhecimento de Transporte Aéreo (Código 10), Conhecimento de Transporte Ferroviário de Cargas (Código 11), Conhecimento de Transporte Multimodal de Cargas (Código 26), Nota Fiscal de Transporte Ferroviário de Carga (Código 27), Conhecimento de Transporte Eletrônico – CT-E (Código 57), Bilhete de Passagem Eletrônico - BP-e (Código 63) e Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS, modelo 67
			4 - D101 - Complemento do Documento de Transporte (Códigos 07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67) – PIS/Pasep
			4 - D105 - Complemento do Documento de Transporte (Códigos 07, 08, 8B, 09, 10, 11, 26, 27, 57, 63 e 67) – Cofins
			4 - D111 - Processo Referenciado
		3 - D200 - Resumo da Escrituração Diária – Prestação de Serviços de Transporte: Nota Fiscal de Serviço de Transporte (Código 07), Conhecimento de Transporte Rodoviário de Cargas (Código 08), Conhecimento de Transporte de Cargas Avulso (Código 8B), Conhecimento de Transporte Aquaviário de Cargas (Código 09), Conhecimento de Transporte Aéreo (Código 10), Conhecimento de Transporte Ferroviário de Cargas (Código 11), Conhecimento de Transporte Multimodal de Cargas (Código 26), Nota Fiscal de Transporte Ferroviário de Carga (Código 27), Conhecimento de Transporte Eletrônico – CT-E (Código 57), Bilhete de Passagem Eletrônico - BP-e (Código 63) e Conhecimento de Transporte Eletrônico para Outros Serviços – CT-e OS, modelo 67
			4 - D201 - Totalização do Resumo Diário – PIS/Pasep
			4 - D205 - Totalização do Resumo Diário – Cofins
			4 - D209 - Processo Referenciado
		3 - D300 - Resumo da Escrituração Diária - Bilhetes Consolidados de Passagem Rodoviário (Código 13), de Passagem Aquaviário (Código 14), de Passagem e Nota de Bagagem (Código 15), de Passagem Ferroviário (Código 16) e Resumo de Movimento Diário (Código 18)
		3 - D350 - Resumo Diário de Cupom Fiscal Emitido Por ECF - (Código: 2E, 13, 14, 15 e 16)
		3 - D359 - Processo Referenciado
		3 - D500 - Nota Fiscal de Serviço de Comunicação (Código 21) e Nota Fiscal de Serviço de Telecomunicação (Código 22) – Documentos de Aquisição com Direito a Crédito
			4 - D501 - Complemento da Operação (Códigos 21 e 22) – PIS/Pasep
			4 - D505 - Complemento da Operação (Códigos 21 e 22) – Cofins
			4 - D509 - Processo Referenciado
		3 - D600 - Consolidação da Prestação de Serviços - Notas de Serviço de Comunicação (Código 21) e de Serviço de Telecomunicação (Código 22)
			4 - D601 - Complemento da Consolidação da Prestação de Serviços (Códigos 21 e 22) - PIS/Pasep
			4 - D605 - Complemento da Consolidação da Prestação de Serviços (Códigos 21 e 22) – Cofins
			4 - D609 - Processo Referenciado
 ## - D990 - Fechamento do Bloco C
 # Bloco F
  ## - F001 - Abertura do Bloco D
	2 - F010 - Identificação do Estabelecimento
		3 - F100 - Demais Documentos e Operações Geradoras de Contribuição e Créditos
			4 - F111 - Processo Referenciado
		3 - F120 - Bens Incorporados ao Ativo Imobilizado – Operações Geradoras de Créditos com Base nos Encargos de Depreciação e Amortização
			4 - F129 - Processo Referenciado
		3 - F130 - Bens Incorporados ao Ativo Imobilizado – Operações Geradoras de Créditos com Base no Valor de Aquisição/Contribuição
			4 - F139 - Processo Referenciado
		3 - F150 - Crédito Presumido sobre Estoque de Abertura
		3 - F200 - Operações da Atividade Imobiliária - Unidade Imobiliária Vendida
			4 - F205 - Operações da Atividade Imobiliária – Custo Incorrido da Unidade Imobiliária
			4 - F210 - Operações da Atividade Imobiliária - Custo Orçado da Unidade Imobiliária Vendida
			4 - F211 - Processo Referenciado
		3 - F500 - Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Caixa
			4 - F509 - Processo Referenciado
		3 - F510 - Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação Com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Caixa (Apuração da Contribuição por Unidade de Medida de Produto – Alíquota em Reais)
			4 - F519 - Processo Referenciado
		3 - F525 - Composição da Receita Escriturada no Período – Detalhamento da Receita Recebida pelo Regime de Caixa
		3 - F550 - Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Competência
			4 - F559 - Processo Referenciado
		3 - F560 - Consolidação das Operações da Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido – Incidência do PIS/Pasep e da Cofins pelo Regime de Competência (Apuração da Contribuição por Unidade de Medida de Produto – Alíquota em Reais)
			4 - F569 - Processo Referenciado
		3 - F600 - Contribuição Retida na Fonte
	2 - F700 - Deduções Diversas
 1 - F800 - Créditos Decorrentes de Eventos de Incorporação, Fusão e Cisão
 ## - F990 - Fechamento do Bloco F
 # Bloco I
   ## - I001 - Abertura do Bloco I
		3 - I010 - Identificação da Pessoa Jurídica/Estabelecimento
			4 - I100 - Consolidação das Operações do Período
			4 - I199 - Processo Referenciado
				5 - 1200 - Composição das Receitas, Deduções e/ou Exclusões do Período
				5 - I299 - Processo Referenciado
					6 - I300 - Complemento das Operações – Detalhamento das Receitas, Deduções e/ou Exclusões Do Período
					6 - I399 - Processo Referenciado
 ## - I990 - Fechamento do Bloco I

 # Bloco M
   ## - M001 - Abertura do Bloco M
	1 - M100 - Crédito de PIS/Pasep Relativo ao Período
		2 - M105 - Detalhamento da Base de Calculo do Crédito Apurado no Período – PIS/Pasep
			3 - M110 - Ajustes do Crédito de PIS/Pasep Apurado
			3 - M115 - Detalhamento dos Ajustes do Crédito de PIS/Pasep Apurado
		2 - M200 - Consolidação da Contribuição para o PIS/Pasep do Período
			3 - M205 - Contribuição para o PIS/Pasep a Recolher–Detalhamento por Código de Receita
			3 - M210 - Detalhamento da Contribuição para o PIS/Pasep do Período
			3 - M211 - Sociedades Cooperativas – Composição da Base de Calculo – PIS/Pasep
				4 - M215 - Ajustes da Base de Cálculo da Contribuição para o PIS/Pasep Apurada
				4 - M220 - Ajustes da Contribuição para o PIS/Pasep Apurada
					5 - M225 - Detalhamento dos Ajustes da Contribuição Para o Pis/Pasep Apurada
			3 - M230 - Informações Adicionais de Diferimento
		2 - M300 - Contribuição de PIS/Pasep Diferida em Períodos Anteriores – Valores a Pagar no Período
		2 - M350 - Folha de Salários
		2 - M400 - Receitas Isentas, não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – PIS/Pasep
			3 - M410 - Detalhamento das Receitas Isentas, não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – Cofins
			3 - M500 - Crédito de Cofins Relativo Ao Período
			3 - M505 - Detalhamento da Base de Calculo do Crédito Apurado no Período – Cofins
			3 - M510 - Ajustes do Crédito de Cofins Apurado
				4 - M515 - Detalhamento dos Ajustes do Crédito de Cofins Apurado
			3 - M600 - Consolidação da Contribuição para a Seguridade Social - Cofins do Período
			3 - M605 - Cofins a Recolher – Detalhamento por Código de Receita
		2 - M610 - Ajustes do Crédito de Cofins Apurado
				4 - M611 - Sociedades Cooperativas – Composição da Base de Calculo – Cofins
				4 - M615 - Ajustes da Base de Cálculo da COFINS Apurada
				4 - M620 - Ajustes da Cofins Apurada
				4 - M630 - Informações Adicionais de Diferimento
		2 - M700 - Cofins Diferida em Períodos Anteriores – Valores a Pagar no Período
		2 - M800 - Receitas Isentas, Não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas Com Suspensão – Cofins
			3 - M810 - Detalhamento das Receitas Isentas, Não Alcançadas pela Incidência da Contribuição, Sujeitas a Alíquota Zero ou de Vendas com Suspensão – Cofins
  ## - M990 - Fechamento do Bloco M

 # Bloco P
 ## - P001 - Abertura do Bloco P
	2 - P010 - Identificação do Estabelecimento
		3 - P100 - Contribuição Previdenciária sobre a Receita Bruta
			4 - P110 - Complemento da Escrituração – Detalhamento da Apuração da Contribuição
			4 - P199 - Processo Referenciado
	2 - P200 - Consolidação da Contribuição Previdenciária Sobre a Receita Bruta
		3 - P210 - Ajuste da Contribuição Previdenciária Apurada Sobre a Receita Bruta
  ## - P990 - Fechamento do Bloco P
 # Bloco 1
 ## - 1001 - Abertura do Bloco 1
	2 - 1010 - Processo Referenciado – Ação Judicial
		3 - 1011 - Detalhamento das Contribuições com Exigibilidade Suspensa
	2 - 1020 - Processo Referenciado – Processo Administrativo
	2 - 1050 - Detalhamento de Ajustes de Base de Cálculo – Valores Extra Apuração
		3 - 1100 - Controle de Créditos Fiscais – PIS/Pasep
	2 - 1101 - Apuração de Crédito Extemporâneo - Documentos e Operações de Períodos Anteriores – PIS/Pasep
		3 - 1102 - Detalhamento do Crédito Extemporâneo Vinculado a Mais de Um Tipo de Receita – PIS/Pasep
	2 - 1200 - Contribuição Social Extemporânea – PIS/Pasep
		3 - 1210 - Detalhamento da Contribuição Social Extemporânea – PIS/Pasep
		3 - 1220 - Demonstração do Crédito a Descontar a Contribuição Extemporânea – PIS/Pasep
	2 - 1300 - Controle dos Valores Retidos na Fonte – PIS/Pasep
	2 - 1500 - Controle de Créditos Fiscais – Cofins
		3 - 1501 - Apuração de Crédito Extemporâneo - Documentos e Operações de Períodos Anteriores – Cofins
			4 - 1502 - Detalhamento do Crédito Extemporâneo Vinculado a Mais de Um Tipo de Receita – Cofins
	2 - 1600 - Contribuição Social Extemporânea – Cofins
		3 - 1610 - Detalhamento da Contribuição Social Extemporânea – Cofins
		3 - 1620 - Demonstração do Crédito a Descontar da Contribuição Extemporânea – Cofins
	2 - 1700 - Controle dos Valores Retidos na Fonte – Cofins
	2 - 1800 - Incorporação Imobiliária – RET
		3 - 1809 - Processo Referenciado
	2 - 1900 - Consolidação dos Documentos Emitidos no Período por Pessoa Jurídica Submetida ao Regime de Tributação com Base no Lucro Presumido–Regime de Caixa ou de Competência
  ## - 1990 - Fechamento do Bloco 1

  # Bloco 9
 ## - 9001 - Abertura do Bloco 9
	2 - 9900 - Registros do Arquivo
 ## - 9990 - Fechamento do Bloco 9

 # - 9999 - Total