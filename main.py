import mysql.connector
from tabulate import tabulate

#Configuração do banco de dados
try:
    conexao_bd = mysql.connector.connect(
        host="172.16.12.14", #IP servidor da PUC
        user="BD080324137",
        password="Orinf7",
        database="BD080324137"
    )
    print('CONECTADO COM SUCESSO!')
except Exception:
    print(Exception)

def inserir_dados(produtos_insert, dados):
    executor_sql = conexao_bd.cursor()
    try:
        executor_sql.execute(produtos_insert,dados)
        conexao_bd.commit()
        print("DADOS DO PRODUTO INSERIDOS COM SUCESSO!")
    except Exception:
        print(Exception)

def executar_query(query):
    executor_sql = conexao_bd.cursor()
    try:
        executor_sql.execute(query)
        conexao_bd.commit()
        print("'",query,"'", "- REALIZADO COM SUCESSO")
    except Exception:
        print(Exception)

#Função para obter o valor de um input
def obter_input(mensagem):
    valor = input(mensagem)
    while not valor.strip():
        print('\nINSIRA UM VALOR VÁLIDO!')
        valor = input(mensagem)
    return valor

#Função para obter um valor do tipo float em um input  
def obter_num_float(mensagem):
    valor = float(input(mensagem))
    while valor <= 0:
        print('\nINSIRA UM VALOR NUMÉRICO POSITIVO E ACIMA DE 0!')
        valor = float(input(mensagem))
    return valor

def arredondar_decimal(num):
    return round(num, 2)
    
print('SEJA BEM-VINDO AO INSTOCK!')
print('PARA INICIARMOS FORNEÇA AS INFORMAÇÕES ABAIXO POR FAVOR\n')

cod_produto = obter_input("Digite o código do produto: ") #chave primária
nome_produto = obter_input("Digite o nome do produto: ")
descricao_produto = obter_input("Digite a descrição do produto: ")

while True:
        try:
            #custo do produto
            CP = obter_num_float("Digite o custo do produto (R$): ")
               
            #custo fixo/administrativo
            CF = obter_num_float("Digite o custo do fixo (%): ")
                
            #comissão de vendas
            CV = obter_num_float("Digite a comissão sobre a venda (%): ")
                
            #impostos 
            IV = obter_num_float("Digite o valor dos impostos (%): ")
                
            #rentabilidade
            ML = obter_num_float("Digite a rentabilidade desejada (%): ")
            
            #Fórmula Preço de Venda
            PV = CP / (1 - ((CF + CV + IV + ML) / 100))
            
            print()
            tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
            tabela_resultados = [
                ["A. Preço de Venda", arredondar_decimal(PV), "100"],
                ["B. Custo de Aquisição (Fornecedor)", arredondar_decimal(CP), arredondar_decimal((CP / PV) * 100)],
                ["C. Receita Bruta (A-B)", arredondar_decimal((PV - CP)), arredondar_decimal(((PV - CP) / PV) * 100)],
                ["D. Custo Fixo/Administrativo", arredondar_decimal((PV * CF) / 100), arredondar_decimal(CF)],
                ["E. Comissão de Vendas", arredondar_decimal((CV * PV) / 100), arredondar_decimal(CV)],
                ["F. Impostos", arredondar_decimal((IV * PV) / 100), arredondar_decimal(IV)],
                ["G. Outros custos (D+E+F)", arredondar_decimal(((PV * CF) / 100)+((CV * PV) / 100)+((IV * PV) / 100)), arredondar_decimal((CF + CV + IV))],
                ["H. Rentabilidade (C-G)", arredondar_decimal(((PV - CP) - (((PV * CF) / 100) + ((CV * PV) / 100) + ((IV * PV) / 100)))), arredondar_decimal(ML)]
            ]  
            print(tabulate(tabela_resultados, headers = tabela_cabecalho))
            
            
            #Faixa de lucro do produto
            if ML >= 20:
                print('\nSua classificação de rentabilidade é de nivel alto')
                  
            elif ML >= 10 and ML < 20:
                print('\nSua classificação de rentabilidade é de nivel médio')
                  
            elif ML > 0 and ML < 10:
                print('\nSua classificação de rentabilidade é de nivel baixo')
                  
            elif ML == 0:
                print('\nSua classificação de rentabilidade é de nivel equilibrado')
                  
            else:
                print('\nSua classificação de rentabilidade é de prejuizo')

            #Inserindo os dados dos produtos da tabela
            produtos_insert = "insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV , ML) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            dados = (cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML)
            inserir = inserir_dados(produtos_insert, dados)
                   
            #Opção de continuar
            continuar = input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            while continuar != 'S' and continuar != 'N':
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                continuar = input('\nDESEJA CONTINUAR UTILIZANDO O PROGRAMA? [S/N]: ').upper()
            if continuar == 'N':
                print('\nOBRIGADO POR USAR ESTE PROGRAMA!')
                break
                
            print('\nINSIRA AS INFORMAÇÕES DO PRÓXIMO PRODUTO')
            cod_produto = obter_input("Digite o código do produto: ") #chave primária
            nome_produto = obter_input("Digite o nome do produto: ")
            descricao_produto = obter_input("Digite a descrição do produto: ")
                
        except ValueError:
            print('\nINSIRA UM VALOR NUMÉRICO!')