estado_map = {
    "SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais",
    "BA": "Bahia", "RS": "Rio Grande do Sul", "PR": "Paraná",
    "SC": "Santa Catarina", "PE": "Pernambuco", "CE": "Ceará",
}

def cidade_para_estado(cidade):
    return ESTADOS.get(cidade, "SEM_INFO")