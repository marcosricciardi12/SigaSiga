from main import create_app

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(host = "0.0.0.0", debug=True, app = app)