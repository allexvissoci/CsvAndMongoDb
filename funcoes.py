import csv
from itertools import combinations


def lerVendas():

    vendas_lista = []
    with open('csv/vendas.csv') as f:

        vendas = csv.reader(f)
        for venda in vendas:
            split_venda = venda[0].split(';')
            venda_dict = {
                            'id_loja': int(split_venda[0]),
                            'id_venda': int(split_venda[1]),
                            'numero_caixa': int(split_venda[2]),
                            'data_venda': split_venda[3],
                            'hora_venda': split_venda[4],
                            'valor_total_sem_desc': float(split_venda[5]),
                            'valor_desconto': float(split_venda[6]),
                            'valor_total_com_desc': float(split_venda[7]),
                            'id_cliente_1': int(split_venda[8]),
                            'id_cliente_2': int(split_venda[9])
                        }
            vendas_lista.append(venda_dict)
        return vendas_lista


def lerVendasItens():

    vendas_itens_lista = []
    with open('csv/vendas_itens.csv') as f:

        vendas_itens = csv.reader(f)
        for venda_item in vendas_itens:

            if(len(venda_item) == 2):
                venda_item = venda_item[0] + ";" + venda_item[1]
            else:
                venda_item = venda_item[0]

            split_venda_item = venda_item.split(';')
            venda_item_dict = {
                'id_loja': int(split_venda_item[0]),
                'id_venda': int(split_venda_item[1]),
                'numero_caixa': int(split_venda_item[2]),
                'id_produto': int(split_venda_item[3]),
                'quantidade': float(split_venda_item[4]),
                'valor_unitario': float(split_venda_item[5]),
                'valor_total_sem_desc': float(split_venda_item[6]),
                'valor_desconto': float(split_venda_item[7]),
                'valor_total_com_desc': float(split_venda_item[8]),
                'id_profissional_1': int(split_venda_item[9].replace('.', '')),
                'id_profissional_2': int(split_venda_item[10].replace('.', ''))
            }
            vendas_itens_lista.append(venda_item_dict)
        return vendas_itens_lista


def calculaTotalVendasProduto(db, vendas_itens):
    pipeline = [
                    {
                        "$group":
                        {
                            "_id": "$id_produto",
                            "numero_produtos": {"$sum": 1},
                            "id_produto": {"$first": "$id_produto"},
                            "totalValorUnitario": {
                                "$sum": {
                                    "$multiply": [
                                      "$valor_unitario",
                                      "$quantidade"
                                    ]
                                }
                            },
                            "valor_total_sem_desc": {
                                "$sum": {
                                    "$multiply": [
                                        "$valor_total_sem_desc",
                                        "$quantidade"
                                        ]
                                    }
                                },
                            "valor_desconto": {
                                "$sum": {
                                    "$multiply": [
                                        "$valor_desconto",
                                        "$quantidade"
                                    ]
                                }
                            },
                            "valor_total_com_desc": {
                                "$sum": {
                                    "$multiply": [
                                        "$valor_total_com_desc",
                                        "$quantidade"
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "$project": {
                           "_id": 0, "numero_produtos": 1, "id_produto": 1,
                           "totalValorUnitario": 1, "valor_total_sem_desc": 1,
                           "valor_desconto": 1, "valor_total_com_desc": 1}
                    }
                ]
    return (list(db.vendas_itens.aggregate(pipeline)))


def calculaTotalVendasCliente(db, vendas):
    pipeline = [
                    {
                        "$group":
                        {
                            "_id": "$id_cliente_1",
                            "numero_clientes": {"$sum": 1},
                            "id_cliente": {"$first": "$id_cliente_1"},
                            "valor_total_sem_desc": {
                                "$sum": "$valor_total_sem_desc"
                            },
                            "valor_desconto": {
                                "$sum": "$valor_desconto"
                            },
                            "valor_total_com_desc": {
                                "$sum": "$valor_total_com_desc"
                            }
                        }
                    },
                    {
                        "$project": {
                           "_id": 0, "numero_clientes": 1, "id_cliente": 1,
                           "valor_total_sem_desc": 1, "valor_desconto": 1,
                           "valor_total_com_desc": 1}
                    }
                ]
    return list(db.vendas.aggregate(pipeline))


def calculaTotalVendasDia(db, vendas):
    pipeline = [
                    {
                        "$group":
                        {
                            "_id": "$data_venda",
                            "numero_datas": {"$sum": 1},
                            "data_venda": {"$first": "$data_venda"},
                            "valor_total_sem_desc": {
                                "$sum": "$valor_total_sem_desc"
                            },
                            "valor_desconto": {
                                "$sum": "$valor_desconto"
                            },
                            "valor_total_com_desc": {
                                "$sum": "$valor_total_com_desc"
                            }
                        }
                    },
                    {
                        "$project": {
                           "_id": 0, "numero_datas": 1, "data_venda": 1,
                           "valor_total_sem_desc": 1, "valor_desconto": 1,
                           "valor_total_com_desc": 1}
                    }
                ]
    return list(db.vendas.aggregate(pipeline))


def calculaTicketMedioClienteDia(db, vendas):
    pipeline = [
                    {
                        "$group":
                        {
                            "_id": {
                                'cliente': "$id_cliente_1",
                                'data_venda': "$data_venda"
                            },
                            "id_cliente": {"$first": "$id_cliente_1"},
                            "count": {"$sum": 1},
                            "valor_total_com_desc": {
                                "$sum": "$valor_total_com_desc"
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "id_cliente": 1,
                            "ticket_medio": {
                                "$divide": [
                                    "$valor_total_com_desc",
                                    "$count"
                                    ]
                            }
                        }
                    }
                ]
    return list(db.vendas.aggregate(pipeline))


def calculaCombinacoes(db, vendas_itens):
    pipeline = [
                    {
                        "$group":
                        {
                            "_id": "$id_venda",
                            "id_venda": {"$first": "$id_venda"},
                            "numero_vendas": {"$sum": 1},
                            "produtos": {"$addToSet": "$id_produto"}
                        }
                    },
                    {
                        "$project": {
                           "_id": 0, "id_venda": 1, "numero_vendas": 1,
                           "produtos": 1}
                    }
                ]

    combinacoesList = []
    for venda in list(db.vendas_itens.aggregate(pipeline)):
        if(len(venda['produtos']) > 1):
            for combinacao in combinations(venda['produtos'], 2):
                d = {
                    "produto1": combinacao[0],
                    "produto2": combinacao[1]}
                combinacoesList.append(d)

    return combinacoesList


def getCombinacoesAgrupadas(db):

    pipeline = [
        {
            "$group":
            {
                "_id": {"produto1": "$produto1", "produto2": "$produto2"},
                "produto1": {"$first": "$produto1"},
                "produto2": {"$first": "$produto2"},
                "count": {"$sum": 1}
            }
        },
        {"$match": {"count": {"$gt": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 50},
        {
            "$project": {
               "_id": 0, "count": 1, "produto1": 1, "produto2": 1}
        }
    ]
    return list(db['combinacoes'].aggregate(pipeline))
