import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Conectado al servidor')

@sio.event
def message_from_server(data):
    print('Mensaje del servidor:', data['time'])

sio.connect('http://localhost:5000')

while True:
    message = input('Ingrese un mensaje para enviar al servidor: ')
    sio.emit('message_from_client', message)
