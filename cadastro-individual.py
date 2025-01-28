import csv
import os
import chardet

def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        rawdata = f.read()
        resultado = chardet.detect(rawdata)
        return resultado['encoding']

def separar_tabelas(input_csv, output_dir, titulos):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Detectando a codificação do arquivo de entrada
    encoding = detectar_codificacao(input_csv)

    with open(input_csv, 'r', encoding=encoding) as file:
        reader = list(csv.reader(file))
        tabela_atual = []
        titulo_atual = None
        valor_celula_a5 = None

        if len(reader) >= 5:
            # Salva e limpa o valor da célula A5
            valor_celula_a5 = reader[4][0].strip() if reader[4][0] else None

        for i, row in enumerate(reader):
            if not row:
                continue

            if row[0] in titulos:  # Verifica se a linha contém um título válido
                if tabela_atual and titulo_atual:  # Salva a tabela anterior
                    salvar_tabela(titulo_atual, tabela_atual, output_dir, valor_celula_a5)
                titulo_atual = row[0]  # Atualiza o título atual
                tabela_atual = []  # Reinicia a tabela
            elif row:  # Adiciona linha à tabela atual
                tabela_atual.append(row)

        # Salva a última tabela, se existir
        if tabela_atual and titulo_atual:
            salvar_tabela(titulo_atual, tabela_atual, output_dir, valor_celula_a5)

def salvar_tabela(titulo, tabela, output_dir, valor_celula_a5):
    nome_arquivo = titulo.replace(" / ", "_").replace(" ", "_").replace("-", "_").replace("__", "_").strip("_") + '.csv'
    caminho_completo = os.path.join(output_dir, nome_arquivo)

    with open(caminho_completo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in tabela:
            # Adiciona `valor_celula_a5` apenas se não for None
            writer.writerow([valor_celula_a5 or ""] + row)

    print(f"Tabela '{titulo}' salva em '{caminho_completo}'.")

def atualizar_tabelas_com_a5(output_dir, valor_a5):
    """
    Abre cada tabela no diretório de saída e adiciona o valor de A5 na próxima coluna disponível.
    """
    for arquivo in os.listdir(output_dir):
        caminho_arquivo = os.path.join(output_dir, arquivo)

        if not arquivo.endswith('.csv'):
            continue

        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            reader = list(csv.reader(file))
        
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in reader:
                row.append(valor_a5)
                writer.writerow(row)

        print(f"Valor de A5 adicionado em '{arquivo}'.")

# Configurações do script
input_csv = 'Relatório de cadastro individual-20250127223114.csv'
output_dir = 'tabelas_separadas'

# Títulos das tabelas
titulos = [
    "Identificação do usuário / cidadão - Faixa etária",
    "Identificação do usuário / cidadão",
    "Identificação do usuário / cidadão - Sexo",
    "Identificação do usuário / cidadão - Raça / Cor",
    "Identificação do usuário / cidadão - Etnia",
    "Identificação do usuário / cidadão - Nacionalidade",
    "Informações sociodemográficas - Relação de parentesco com o responsável familiar",
    "Informações sociodemográficas - Ocupação",
    "Informações sociodemográficas - Qual é o curso mais elevado que frequenta ou frequentou",
    "Informações sociodemográficas - Situação no mercado de trabalho",
    "Informações sociodemográficas - Crianças de 0 a 9 anos, com quem fica",
    "Informações sociodemográficas - Orientação sexual",
    "Informações sociodemográficas - Identidade de gênero",
    "Informações sociodemográficas - Deficiência",
    "Informações sociodemográficas - Povos e comunidades",
    "Outras informações sociodemográficas",
    "Condições / Situações de saúde gerais",
    "Condições / Situações de saúde gerais - Sobre seu peso, você se considera",
    "Condições / Situações de saúde gerais - Doença respiratória",
    "Condições / Situações de saúde gerais - Doença cardíaca",
    "Condições / Situações de saúde gerais - Problemas nos rins",
    "Cidadão em situação de rua",
    "Cidadão em situação de rua - Tempo em situação de rua",
    "Cidadão em situação de rua - Quantas vezes se alimenta ao dia",
    "Cidadão em situação de rua - Qual a origem da alimentação",
    "Cidadão em situação de rua - Tem acesso à higiene pessoal",
    "TRIA - Nos últimos três meses, os alimentos acabaram antes que a pessoa tivesse dinheiro para comprar mais comida?",
    "TRIA - Nos últimos três meses, a pessoa comeu apenas alguns alimentos que ainda tinha, porque o dinheiro acabou?"
]


# Passo 1: Separar as tabelas
separar_tabelas(input_csv, output_dir, titulos)

# Passo 2: Obter o valor da célula A5
encoding = detectar_codificacao(input_csv)
with open(input_csv, 'r', encoding=encoding) as file:
    reader = list(csv.reader(file))
    valor_a5 = reader[4][0] if len(reader) >= 5 else "N/A"

# Passo 3: Atualizar tabelas com o valor de A5
atualizar_tabelas_com_a5(output_dir, valor_a5)
