import warnings

import pandas as pd
import sqlalchemy

# Retirada de avisos desnecessários
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

print("⌛\tIniciando inserção de dados...")

# Importação dos arquivos csv
cadastro = pd.read_csv('./public/202307_Cadastro.csv', encoding='iso-8859-1', sep=';')
remuneracao = pd.read_csv('./public/202307_Remuneracao.csv', encoding='iso-8859-1', sep=';')

print("🕒\tImportações concluídas.")

# Filtragem para que se tenha apenas os servidores do RJ
filtered_cadastro = cadastro[cadastro['UF_EXERCICIO'].isin(['RJ', '-1'])]

# Filtro para ter apenas servidores com cargos semelhantes a professores
filtered_cadastro = filtered_cadastro[filtered_cadastro['DESCRICAO_CARGO'].isin(['PROFESSOR 3 GRAU - SUBSTITUTO', 'PROFESSOR 3 GRAU - VISITANTE', 'PROFESSOR DO MAGISTERIO SUPERIOR', 'PROFESSOR ENS BASICO TECN TECNOLOGICO', 'PROFESSOR MAGISTERIO SUPERIOR -VISITANTE', 'PROFESSOR MAGISTERIO SUPERIOR-SUBSTITUTO', 'PROFESSOR MAGISTERIO SUPERIOR-TEMPORARIO', 'PROFESSOR TITULAR-LIVRE MAG SUPERIOR'])]

# Filtragem para remoção dos servidores que exercem cargos em outras instituições fora as 3 universidades listadas
filtered_cadastro = filtered_cadastro[filtered_cadastro['ORG_EXERCICIO'].isin(['Universidade Federal do Rio de Janeiro', 'Universidade Federal Rural do Rio de Janeiro', 'Universidade Federal Fluminense - RJ'])]

filtered_cadastro = filtered_cadastro[filtered_cadastro['ORG_LOTACAO'].isin(['Universidade Federal do Rio de Janeiro', 'Universidade Federal Rural do Rio de Janeiro', 'Universidade Federal Fluminense - RJ'])]

# Remoção de colunas que não serão utilizadas
filtered_cadastro.drop(columns=['DIPLOMA_INGRESSO_CARGOFUNCAO', 'DIPLOMA_INGRESSO_ORGAO', 'DIPLOMA_INGRESSO_SERVICOPUBLICO', 'CLASSE_CARGO', 'REFERENCIA_CARGO', 'PADRAO_CARGO', 'NIVEL_CARGO', 'SIGLA_FUNCAO', 'NIVEL_FUNCAO', 'FUNCAO', 'CODIGO_ATIVIDADE', 'CLASSE_CARGO', 'ATIVIDADE', 'OPCAO_PARCIAL', 'COD_ORGSUP_LOTACAO', 'ORGSUP_LOTACAO', 'COD_ORGSUP_EXERCICIO', 'ORGSUP_EXERCICIO', 'COD_TIPO_VINCULO', 'TIPO_VINCULO', 'DATA_INICIO_AFASTAMENTO', 'DATA_TERMINO_AFASTAMENTO', 'DATA_NOMEACAO_CARGOFUNCAO', 'DATA_DIPLOMA_INGRESSO_SERVICOPUBLICO', 'DOCUMENTO_INGRESSO_SERVICOPUBLICO','REGIME_JURIDICO', 'SITUACAO_VINCULO', 'DATA_INGRESSO_CARGOFUNCAO', 'UF_EXERCICIO', 'COD_ORG_EXERCICIO', 'COD_UORG_EXERCICIO',	'UORG_EXERCICIO', 'MATRICULA', 'JORNADA_DE_TRABALHO', 'ORG_EXERCICIO'], inplace=True)

# Renomeação de colunas
filtered_cadastro.rename(columns={'Id_SERVIDOR_PORTAL': 'id_servidor', 'NOME': 'nome', 'CPF': 'cpf', 'DESCRICAO_CARGO': 'cargo', 'COD_UORG_LOTACAO': 'id_instituto','UORG_LOTACAO': 'nome_instituto', 'COD_ORG_LOTACAO': 'id_uni', 'ORG_LOTACAO': 'nome_uni', 'DATA_INGRESSO_ORGAO': 'data_ingresso' }, inplace=True)

filtered_cadastro.loc[filtered_cadastro['nome_uni'] == 'Universidade Federal Fluminense - RJ', 'nome_uni'] = 'Universidade Federal Fluminense'

print("🕕\tFiltragem de cadastro finalizada.")

# Junção das colunas de mês e ano para que se tenha apenas uma coluna de data
filtered_remuneracao = remuneracao[remuneracao['MES'].isin([7.0])]
filtered_remuneracao['MES'] = filtered_remuneracao['MES'].astype(int)
filtered_remuneracao['MES/ANO'] = filtered_remuneracao['MES'].astype(str) + '/' + filtered_remuneracao['ANO'].astype(str)
filtered_remuneracao['MES/ANO'] = pd.to_datetime(filtered_remuneracao['MES/ANO'], format='%m/%Y')

# Remoção de colunas que não serão utilizadas
filtered_remuneracao.drop(columns=['ANO', 'MES','CPF', 'NOME', 'REMUNERAÇÃO BÁSICA BRUTA (U$)', 'ABATE-TETO (R$)', 'ABATE-TETO (U$)', 'GRATIFICAÇÃO NATALINA (U$)', 'ABATE-TETO DA GRATIFICAÇÃO NATALINA (R$)', 'ABATE-TETO DA GRATIFICAÇÃO NATALINA (U$)', 'FÉRIAS (U$)', 'OUTRAS REMUNERAÇÕES EVENTUAIS (R$)', 'OUTRAS REMUNERAÇÕES EVENTUAIS (U$)', 'IRRF (U$)', 'PSS/RPGS (U$)', 'DEMAIS DEDUÇÕES (U$)', 'PENSÃO MILITAR (R$)', 'PENSÃO MILITAR (U$)', 'FUNDO DE SAÚDE (R$)', 'FUNDO DE SAÚDE (U$)', 'TAXA DE OCUPAÇÃO IMÓVEL FUNCIONAL (R$)', 'TAXA DE OCUPAÇÃO IMÓVEL FUNCIONAL (U$)', 'REMUNERAÇÃO APÓS DEDUÇÕES OBRIGATÓRIAS (U$)', 'VERBAS INDENIZATÓRIAS REGISTRADAS EM SISTEMAS DE PESSOAL - CIVIL (R$)(*)', 'VERBAS INDENIZATÓRIAS REGISTRADAS EM SISTEMAS DE PESSOAL - CIVIL (U$)(*)', 'VERBAS INDENIZATÓRIAS REGISTRADAS EM SISTEMAS DE PESSOAL - MILITAR (R$)(*)', 'VERBAS INDENIZATÓRIAS REGISTRADAS EM SISTEMAS DE PESSOAL - MILITAR (U$)(*)', 'VERBAS INDENIZATÓRIAS PROGRAMA DESLIGAMENTO VOLUNTÁRIO  MP 792/2017 (R$)', 'VERBAS INDENIZATÓRIAS PROGRAMA DESLIGAMENTO VOLUNTÁRIO  MP 792/2017 (U$)', 'TOTAL DE VERBAS INDENIZATÓRIAS (R$)(*)', 'TOTAL DE VERBAS INDENIZATÓRIAS (U$)(*)'], inplace=True)

# Renomeação de colunas
filtered_remuneracao.rename(columns={'Id_SERVIDOR_PORTAL': 'id_servidor', 'REMUNERAÇÃO BÁSICA BRUTA (R$)': 'val_bruto', 'GRATIFICAÇÃO NATALINA (R$)': 'val_natal', 'FÉRIAS (R$)': 'val_ferias', 'IRRF (R$)': 'irrf', 'PSS/RPGS (R$)': 'pss/rpgs', 'DEMAIS DEDUÇÕES (R$)': 'outras_deducoes', 'REMUNERAÇÃO APÓS DEDUÇÕES OBRIGATÓRIAS (R$)': 'val_liquido', 'MES/ANO': 'data'}, inplace=True)

# Conversão de valores para float
filtered_remuneracao['val_bruto'] = filtered_remuneracao['val_bruto'].str.replace(',', '.').astype(float)
filtered_remuneracao['val_natal'] = filtered_remuneracao['val_natal'].str.replace(',', '.').astype(float)
filtered_remuneracao['val_ferias'] = filtered_remuneracao['val_ferias'].str.replace(',', '.').astype(float)
filtered_remuneracao['irrf'] = filtered_remuneracao['irrf'].str.replace(',', '.').astype(float)
filtered_remuneracao['pss/rpgs'] = filtered_remuneracao['pss/rpgs'].str.replace(',', '.').astype(float)
filtered_remuneracao['outras_deducoes'] = filtered_remuneracao['outras_deducoes'].str.replace(',', '.').astype(float)
filtered_remuneracao['val_liquido'] = filtered_remuneracao['val_liquido'].str.replace(',', '.').astype(float)

# Preenchimento de valores nulos
filtered_remuneracao['val_bruto'] = filtered_remuneracao['val_bruto'].fillna(0)
filtered_remuneracao['val_natal'] = filtered_remuneracao['val_natal'].fillna(0)
filtered_remuneracao['val_ferias'] = filtered_remuneracao['val_ferias'].fillna(0)
filtered_remuneracao['irrf'] = filtered_remuneracao['irrf'].fillna(0)
filtered_remuneracao['pss/rpgs'] = filtered_remuneracao['pss/rpgs'].fillna(0)
filtered_remuneracao['outras_deducoes'] = filtered_remuneracao['outras_deducoes'].fillna(0)
filtered_remuneracao['val_liquido'] = filtered_remuneracao['val_liquido'].fillna(0)

print("🕘\tFiltragem de remuneração finalizada. ")

# Conexão com o banco de dados
conexao = sqlalchemy.create_engine('mysql+mysqlconnector://root:root@localhost:33061/servidores', echo=False)

# Inserção dos dados na tabela Universidade
universidade_data = filtered_cadastro[['id_uni', 'nome_uni']].drop_duplicates()
universidade_data.to_sql('Universidade', con=conexao, if_exists='append', index=False, method='multi', chunksize=10000) 

# Inserção dos dados na tabela Instituto
instituto_data = filtered_cadastro[~filtered_cadastro['id_instituto'].duplicated()]
instituto_data.rename(columns={'id_uni': 'fk_instituto_universidade'}, inplace=True)
instituto_data[['id_instituto', 'nome_instituto', 'fk_instituto_universidade']].to_sql('Instituto', con=conexao, if_exists='append', index=False, method='multi', chunksize=10000) 

# Inserção dos dados na tabela Servidor
servidor_data = filtered_cadastro.rename(columns={'id_uni': 'fk_servidor_universidade', 'id_instituto': 'fk_servidor_instituto'})
servidor_data['data_ingresso'] = pd.to_datetime(servidor_data['data_ingresso'], format='%d/%m/%Y')
servidor_data = servidor_data[~servidor_data['id_servidor'].duplicated()]
servidor_data[['id_servidor', 'nome', 'cpf', 'cargo', 'data_ingresso', 'fk_servidor_instituto', 'fk_servidor_universidade']].to_sql('Servidor', con=conexao, if_exists='append', index=False, method='multi', chunksize=10000)

print("🕛\tMetade das inserções concluídas.")

# Inserção dos dados na tabela Remuneracao
remuneracao_data = filtered_remuneracao[filtered_remuneracao['id_servidor'].isin(filtered_cadastro['id_servidor'])]
remuneracao_data.rename(columns={'id_servidor': 'fk_remuneracao_servidor'}, inplace=True)
remuneracao_data[['fk_remuneracao_servidor', 'val_bruto', 'val_natal', 'val_ferias', 'outras_deducoes', 'val_liquido', 'data']].to_sql('Remuneracao', con=conexao, if_exists='append', index=False, method='multi', chunksize=10000)

# Inserção dos dados na tabela Imposto
column_titles = ['irrf', 'pss/rpgs']
imposto_data = pd.DataFrame({'nome_imposto': [title.upper() for title in column_titles]})
imposto_data.to_sql('Imposto', con=conexao, if_exists='append', index=False, method='multi', chunksize=10000)

print("✅\tDados inseridos com sucesso!")