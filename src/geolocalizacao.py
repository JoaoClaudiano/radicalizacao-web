estado_map = {
    "SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais",
    "BA": "Bahia", "RS": "Rio Grande do Sul", "PR": "Paraná",
    "SC": "Santa Catarina", "PE": "Pernambuco", "CE": "Ceará",
}

def normalizar_estado(nome):
    if nome in estado_map.values():
        return nome
    for sigla, estado in estado_map.items():
        if sigla.lower() == nome.lower():
            return estado
    return None
