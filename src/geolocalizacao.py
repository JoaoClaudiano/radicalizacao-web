# Função para normalizar nomes de estados

estado_map = {
    "SP": "São Paulo", "RJ": "Rio de Janeiro", "MG": "Minas Gerais",
    "BA": "Bahia", "RS": "Rio Grande do Sul", "PR": "Paraná",
    "SC": "Santa Catarina", "PE": "Pernambuco", "CE": "Ceará",
    "RN": "Rio Grande do Norte",
    # Adicione outros estados aqui...
}

def normalizar_estado(nome):
    """Converte abreviação ou cidade para nome de estado (simulado)"""
    if nome in estado_map.values():
        return nome
    for sigla, estado in estado_map.items():
        if sigla.lower() == nome.lower():
            return estado
    # fallback
    return None
