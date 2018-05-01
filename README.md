# CsvAndMongoDb

Descrição:
  Programa em Python que acessa documentos CSV "vendas.csv" e "vendas_itens.csv", e calcule os seguintes sumários e os insira no MongoDB:

  - Total de vendas por produto
  - Total de vendas cliente
  - Total de vendas por dia
  - Ticket médio por cliente por dia (Ticket Médio = Faturamento / numero de cupons de vendas)
  
  O programa também deve calcular uma correlação entre produtos indicando quais produtos em conjunto tem maiores chances de       serem comprados ou vendidos em conjunto.
  
Layout vendas.csv:

  Campo	                      Descrição	                Tipo	      tamanho	    Formato	          Valor Padrão
id_loja	              identificação da loja	          inteiro	        20		                  ref. arquivo “lojas.txt”
id_venda	            identificação da venda	        inteiro	        20		
numero_caixa	        identificação do caixa	        inteiro	        20		                            0
data_venda	          data da venda	                    data	        10	    dd/mm/aaaa	
hora_venda	          hora da venda	                    hora	         5	         hh:mm	
valor_total_sem_desc	valor da venda sem desconto	    decimal	        9,2	          9.99	
valor_desconto	      valor do desconto concedido	    decimal	        9,2	          9.99                 0.00
valor_total_com_desc	valor da venda com desconto	    decimal	        9,2	          9.99	    valor_total_sem_desc
id_cliente_1	        identificação cliente venda	    inteiro	        20		                  ref. arquivo “clientes.txt”
id_cliente_2	        identificação do cliente / 	    inteiro	        20		                  ref. arquivo “clientes.txt”
                      profissional desta venda
                      (ex. arquiteto, mestre 
                      de obras etc)


Layout vendas_itens.csv:

  Campo	                     Descrição	                  Tipo	  Tamanho	    Formato	      Valor Padrão
id_loja	              identificação da loja	            inteiro	    20		                ref. arquivo “lojas.txt”
id_venda	            identificação da venda	          inteiro	    20		                ref. arquivo “vendas.txt”
numero_caixa	        identificação do caixa	          inteiro	    20		                ref. arquivo “vendas.txt”
id_produto	          identificação do produto	        inteiro	    20		                ref. arquivo “produtos.txt”
quantidade	          quantidade comprada do produto	  decimal	    6,4	    01/09/99	
valor_unitario	      valor unitário do produto	        decimal	    9,3	      9999	
valor_total_sem_desc	valor da venda sem desconto	      decimal	    9,3	      9999	
valor_desconto	      valor do desconto concedido	      decimal	    9,3	      9999	      0.0
valor_total_com_desc	valor da venda com desconto	      decimal	    9,3	      9999	      valor_total_sem_desc
id_profissional_1	    identificação do profissional     inteiro	    20		                ref. arquivo “profissionais.txt”
                      deste item.	
id_profissional_2     identificação do profissional     inteiro	    20		                ref. arquivo “profissionais.txt”
                      auxiliar deste item.	


Como executar:
1º Clone o repositório.
2º Abra o terminal.
3º Acesse o repositório.
4º rode o comando "python3 lercsv.py"


O script criará um database chamado "vendasCsv" no MongoDB.
Os dados do csv "vendas.csv" serão armazenados na collection "vendas"
Os dados do csv "vendas_itens.csv" serão armazenados na collection "vendas_itens"
Os sumários serão inseridos respectivamente nas collections:

  - Total de vendas por produto = "total_vendas_produto"
  - Total de vendas cliente = "total_vendas_cliente"
  - Total de vendas por dia = "total_vendas_dia"
  - Ticket médio por cliente por dia (Ticket Médio = Faturamento / numero de cupons de vendas) = "ticket_medio_cliente_dia"

O calculo de produtos com maior chance de serem vendidos/comprados em conjunto, foi elaborado agrupando todos as vendas da collection "vendas_itens", e armazenando em um array todos os produtos das vendas agrupadas.
Depois foi calculado todas as combinações de 2 produtos vendidos em uma venda possível as inserindo na collection "combinacoes"
A partir desta collection foi possível calcular quantas vezes determinadas combinações se repetiram. Sendo as com maior número de repetições consideradas as combinações com maiores chances de se repetirem.

