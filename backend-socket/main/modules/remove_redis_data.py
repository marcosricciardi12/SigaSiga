from main import redis

def delete_event(event_id):
    pattern = f'{event_id}*'
    keys_to_delete = redis.keys(pattern)
    if keys_to_delete:
        redis.delete(*keys_to_delete)
        print(f"Se han eliminado {len(keys_to_delete)} claves que coinciden con el patrón '{pattern}'.")
    else:
        print(f"No se encontraron claves que coincidan con el patrón '{pattern}'.")