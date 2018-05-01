from pymongo import MongoClient
from funcoes import lerVendas, lerVendasItens
from funcoes import calculaTotalVendasProduto, calculaTotalVendasCliente
from funcoes import calculaTotalVendasDia, calculaTicketMedioClienteDia
from funcoes import calculaCombinacoes, getCombinacoesAgrupadas


print("Lendo Arquivos")
vendas_lista = lerVendas()
vendas_itens_lista = lerVendasItens()

cliente = MongoClient('localhost', 27017)
db = cliente['testeMercafacil']

vendas = db['vendas']
vendas.insert_many(vendas_lista)

vendas_itens = db['vendas_itens']
vendas_itens.insert_many(vendas_itens_lista)

print("Calculando Sumários")
######################################################
# TOTAL DE VENDAS POR PRODUTO#########################
######################################################
totalVendasProduto = calculaTotalVendasProduto(db, vendas_itens)
totalVendasProdutoCollection = db['total_vendas_produto']
db.drop_collection('total_vendas_produto')
totalVendasProdutoCollection.insert_many(totalVendasProduto)

######################################################
# TOTAL DE VENDAS POR CLIENTE#########################
######################################################
totalVendasCliente = calculaTotalVendasCliente(db, vendas)
totalVendasClienteCollection = db['total_vendas_cliente']
db.drop_collection('total_vendas_cliente')
totalVendasClienteCollection.insert_many(totalVendasCliente)

######################################################
# TOTAL DE VENDAS POR DIA#############################
######################################################
totalVendasDia = calculaTotalVendasDia(db, vendas)
totalVendasDiaCollection = db['total_vendas_dia']
db.drop_collection('total_vendas_dia')
totalVendasDiaCollection.insert_many(totalVendasDia)

######################################################
# Ticket Médio Cliente por Dia########################
######################################################
ticketMedioCliente = calculaTicketMedioClienteDia(db, vendas)
ticketMedioCollection = db['ticket_medio_cliente_dia']
db.drop_collection('ticket_medio_cliente_dia')
ticketMedioCollection.insert_many(ticketMedioCliente)


######################################################
# Produtos comprados em conjunto######################
######################################################
print("Calculando produtos com maior chance de serem vendidos/comprados em conjunto")
combinacoesList = calculaCombinacoes(db, vendas_itens)
db.drop_collection('combinacoes')
db['combinacoes'].insert_many(combinacoesList)


combinacoesAgrupadas = getCombinacoesAgrupadas(db)
totalVendas = len(list(db.vendas_itens.aggregate([
    {"$group": {"_id": "$id_venda"}}
])))

print("Dado uma amostra de %s produtos vendidos:" % (totalVendas))
print("Tem-se uma lista das 50 combinaçoes de produtos que possuem maior chance de serem comprados em conjunto:")
c = 1
for x in combinacoesAgrupadas:
    print("{0}: Produtos: {1}, {2} - Vendidos {3} vezes em {4} Vendas".format(c, x["produto1"], x["produto2"], x["count"], totalVendas))
    c += 1
