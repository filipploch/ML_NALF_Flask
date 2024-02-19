


@socketio.on('message_from_obs')
def handle_some_event(data):
    print('Received data:', data)