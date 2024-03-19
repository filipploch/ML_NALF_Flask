from obswebsocket import obsws, requests, events
from time import sleep
from flask import json


class OBSWebsocket(obsws):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ws = None
        self.socketio = None
        self.config = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, host="192.168.0.157", port=4445):
        with app.app_context():
            try:
                # Próba połączenia z adresem 127.20.10.3
                self.ws = obsws(host, port)
                self.config = app.config
                self.socketio = app.config['SOCKETIO']
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
            self.ws.register(self.on_audio_input_state_change, events.InputMuteStateChanged)
            self.ws.register(self.on_record_state_change, events.RecordStateChanged)

    def connect_websocket(self, app):
        with app.app_context():
            self.ws.connect()

    def take_screenshot(self):
        self.ws.call(requests.TriggerHotkeyByName(**{'hotkeyName': 'OBSBasic.Screenshot'}))

    def start_recording(self):
        self.ws.call(requests.StartRecord())

    def stop_recording(self):
        self.ws.call(requests.StopRecord())

    def show_scene(self, scene_name):
        self.ws.call(requests.SetCurrentProgramScene(**{'sceneName': scene_name}))

    def get_source_id(self, scene_name, source_name):
        scene_item_id = self.ws.call(requests.GetSceneItemId(**{'sceneName': scene_name, 'sourceName': source_name}))
        response_data = scene_item_id.datain
        return response_data['sceneItemId']

    def show_source(self, scene_name, source_name, visible=True):
        source_id = self.get_source_id(scene_name, source_name)
        self.ws.call(requests.SetSceneItemEnabled(**{'sceneName': scene_name, "sceneItemId": source_id, "sceneItemEnabled": visible}))

    def mute_input(self, source_name, is_muted=True):
        self.ws.call(requests.SetInputMute(**{'inputName': source_name, 'inputMuted': is_muted}))

    def get_audio_source_state(self, source_name):
        request = self.ws.call(requests.GetInputMute(**{'inputName': source_name})).datain
        response = request.get('inputMuted')
        return response

    def on_audio_input_state_change(self, message):
        if message.datain['inputName'] in self.config['AUDIO_ICONS']:
            _data = message.datain
            _div_id = _data['inputName']
            _suffix = ''
            if _data['inputMuted']:
                _suffix = '_MUTED'
            else:
                _suffix = '_UNMUTED'
            _img_file = _data['inputName'].upper().replace('-', '_')
            _img_file += _suffix
            _img_tag = f"/static/controller/images/{self.config[_img_file]}"
            data = {'divId': _div_id, 'imgTag': _img_tag}
            self.socketio.emit('changeAudioIcon',  data, namespace='/')

    def get_record_status(self):
        request = self.ws.call(requests.GetRecordStatus()).datain
        return request

    def start_record_cascade(self):
        self.mute_input('Mikrofon')
        self.mute_input('tytul-muzyka')
        self.mute_input('podklad-muzyka')
        self.show_source('TYTUŁ', 'MUZYKA-TYTUŁ', visible=False)
        self.show_scene('PUSTA')
        sleep(0.5)
        self.start_recording()
        sleep(0.5)
        self.show_scene('TYTUŁ')
        sleep(8)
        self.show_source('TYTUŁ', 'MUZYKA-TYTUŁ')
        self.mute_input('tytul-muzyka', is_muted=False)
        sleep(8)
        self.take_screenshot()
        sleep(4)
        self.show_scene('STUDIO-START')
        self.mute_input('Mikrofon', is_muted=False)
        sleep(1)
        self.show_source('TYTUŁ', 'MUZYKA-TYTUŁ', visible=False)
        self.mute_input('tytul-muzyka')
        self.mute_input('podklad-muzyka', is_muted=False)

    def end_record_cascade(self):
        self.mute_input('Mikrofon')
        self.mute_input('podklad-muzyka')
        self.show_scene('Napisy-koncowe')
        sleep(10)
        self.stop_recording()

    def higlight_cascade(self):
        self.mute_input('podklad-muzyka', is_muted=False)
        self.mute_input('Mikrofon', is_muted=False)
        self.mute_input('Skrot_YT')
        self.show_scene('Skrót-Start')
        sleep(1.5)
        self.show_scene('SKRÓT YT')

    def flash_highlight_cascade(self):
        self.show_scene('Skrót-Start')
        sleep(1.5)
        self.mute_input('podklad-muzyka')
        self.mute_input('Mikrofon')
        self.mute_input('Skrot_YT', is_muted=False)
        self.show_scene('SKRÓT YT')

    def end_highlight_cascade(self):
        self.show_scene('Sktót-koniec')
        self.mute_input('podklad-muzyka', is_muted=False)
        self.mute_input('Mikrofon', is_muted=False)
        self.mute_input('Skrot_YT')
        sleep(4)
        self.show_scene('STUDIO-BLANK')

    def show_studio(self):
        self.mute_input('podklad-muzyka', is_muted=False)
        self.mute_input('Mikrofon', is_muted=False)
        self.mute_input('Skrot_YT')
        self.show_scene('STUDIO')

    def show_results(self):
        self.show_scene('WYNIKI')

    def show_table(self):
        self.show_scene('TABELA')

    def show_schedule(self):
        self.show_scene('TERMINARZ')

    def show_strikers(self):
        self.show_scene('STRZELCY')

    def show_assistants(self):
        self.show_scene('ASYSTENCI')

    def show_canadians(self):
        self.show_scene('KANADYJSKA')

    def show_best_five(self):
        self.show_scene('PIĄTKA KOLEJKI')

    def on_record_state_change(self, message):
        _data = message.datain
        if _data['outputActive']:
            className = 'button-active'
        else:
            className = 'button-inactive'
        self.socketio.emit('changeRecordIcon', className, namespace='/')





