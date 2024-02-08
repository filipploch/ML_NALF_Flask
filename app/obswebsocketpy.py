from obswebsocket import obsws, requests


class OBSWebsocket:
    def __init__(self, app=None, host=None, port=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, host="127.0.0.1", port=4445):
        with app.app_context():
            try:
                # Próba połączenia z adresem 127.20.10.3
                self.ws = obsws(host, port)
            except Exception as e:
                print(f"Nie udało się połączyć z adresem {host}. Błąd: {e}")
                # Jeśli nie udało się połączyć, spróbuj z localhost
                localhost = "localhost"
                try:
                    # Próba połączenia z adresem localhost
                    self.ws = obsws(localhost, port)
                except Exception as e:
                    print(f"Nie udało się połączyć z adresem {localhost}. Błąd: {e}")
                    print("Żadne z dostępnych adresów IP nie jest dostępne.")

    def connect_websocket(self, app):
        with app.app_context():
            self.ws.connect()

    def get_audio_source_state(self, source_name):
        request = self.ws.call(requests.GetInputMute(**{'inputName': source_name})).datain
        response = request.get('inputMuted')
        return response