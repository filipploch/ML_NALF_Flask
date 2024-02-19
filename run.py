from app.main import create_app
app = create_app()
socketio = app.config['SOCKETIO']

if __name__ == "__main__":
    port = 5000
    socketio.run(app, host="0.0.0.0", port=port, debug=True, use_reloader=False)
    # app.run(host="0.0.0.0", port=port, debug=True)