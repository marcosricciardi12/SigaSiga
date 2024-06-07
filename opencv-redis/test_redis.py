import redis

def obtener_elementos_por_patron(host, port, pattern):
    # Conectar a Redis
    cliente = redis.Redis(host=host, port=port, decode_responses=True)
    
    # Obtener todas las claves que coincidan con el patrón
    claves = cliente.keys(pattern)
    
    # Obtener los valores correspondientes a las claves
    elementos = {clave: cliente.get(clave) for clave in claves}
    
    return elementos

# Configuración de conexión (ajusta según tus necesidades)
host = 'localhost'  # Dirección del servidor Redis
port = 6379         # Puerto del servidor Redis

# Patrón de búsqueda
pattern = '45nHoUgC9ZyAS3TWmGiGyh-participant-*'  # Sustituye 'tu_patron*' por el patrón deseado

# Obtener y mostrar los elementos
participantes = obtener_elementos_por_patron(host, port, pattern)
for clave, valor in participantes.items():
    print(f'Clave: {clave}, Valor: {valor}')
    pattern = f"user-{valor}*"
    participante = obtener_elementos_por_patron(host, port, pattern)
    for clave, valor in participante.items():
        print(f'\tClave: {clave}, Valor: {valor}')
    