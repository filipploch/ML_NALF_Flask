from flask import jsonify
import json


class JsonOperator:
    @staticmethod
    def get_json_data(json_file):
        # with app.app_context():
        json_file_path = f'app/data/json/{json_file}.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)

    @staticmethod
    def get_current_edition_episodes(app, number_of_episodes=None):
        with app.app_context():
            json_file_path = app.config['MAGAZINES_JSON_FILE']
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            episodes = sorted([edition['episodes'] for edition in data['editions'] if edition['is_active']],
                              key=lambda episode: episode.id)
            if number_of_episodes is not None:
                episodes = episodes[:number_of_episodes]
            return jsonify(episodes)

    @staticmethod
    def add_episode(app, new_episode):
        with app.app_context():
            json_file_path = app.config['MAGAZINES_JSON_FILE']
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            _actual_edition = [edition for edition in data['editions'] if edition['is_active']][0]
            _actual_edition_index = data['editions'].index(_actual_edition)
            _actual_edition_episodes = sorted(
                [edition['episodes'] for edition in data['editions'] if edition['is_active']],
                key=lambda episode: episode.id)
            _actual_edition_episodes.append(new_episode)
            data['editions'][_actual_edition_index]['episodes'] = _actual_edition_episodes
            with open(json_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)

    @staticmethod
    def buffer_new_episodes(new_episodes_list):
        json_file_path = f'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(new_episodes_list, file, indent=2)

    @staticmethod
    def update_episode_buffer(data):
        json_file_path = f'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_actual_edition_episodes(episodes):
        json_file_path = f'app/data/json/magazines.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        for edition in data['editions']:
            if edition['is_active']:
                edition['episodes'] = episodes
                break
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_title_buffer(_title, _episode_id):
        json_file_path = f'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        for episode in data:
            if episode['id'] is int(_episode_id):
                episode['title'][0] = _title[0]
                episode['title'][1] = _title[1]
                break
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_title(_title, _episode_id):
        json_file_path = f'app/data/json/magazines.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        _edition = [edition for edition in data['editions'] if edition['is_active']][0]
        _edition_idx = next((idx for idx, edition in enumerate(data['editions'])
                             if edition['is_active']), None)
        _episode = [episode for episode in _edition['episodes'] if episode['id'] is int(_episode_id)][0]
        _episode_idx = next((idx for idx, episode in enumerate(_edition['episodes'])
                             if episode['id'] is int(_episode_id)), None)
        data['editions'][_edition_idx]['episodes'][_episode_idx]['title'] = _title
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_best_five_buffer(_best_five, _episode_id):
        json_file_path = f'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        for episode in data:
            if episode['id'] is int(_episode_id):
                episode['best_five'] = _best_five
                break
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_best_five(_best_five, _episode_id, _competition_id):
        json_file_path = f'app/data/json/magazines.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        _edition = [edition for edition in data['editions'] if edition['is_active']][0]
        _edition_idx = next((idx for idx, edition in enumerate(data['editions'])
                             if edition['is_active']), None)
        _episode = [episode for episode in _edition['episodes'] if episode['id'] is int(_episode_id)][0]
        _episode_idx = next((idx for idx, episode in enumerate(_edition['episodes'])
                             if episode['id'] is int(_episode_id)), None)
        competition_idx = int
        for idx, competition in enumerate(_episode['competitions']):
            if competition['id'] == int(_competition_id):
                competition_idx = idx
                break
        data['editions'][_edition_idx]['episodes'][_episode_idx]['competitions'][competition_idx]['best_five'] \
            = _best_five

        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_highlights_buffer(_highlights, _episode_id):
        json_file_path = 'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        for episode in data:
            if episode['id'] is int(_episode_id):
                episode['highlights'] = _highlights
                break
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def update_episode_highlights(_highlights, _episode_id):
        json_file_path = f'app/data/json/magazines.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        _edition = [edition for edition in data['editions'] if edition['is_active']][0]
        _edition_idx = next((idx for idx, edition in enumerate(data['editions'])
                             if edition['is_active']), None)
        _episode = [episode for episode in _edition['episodes'] if episode['id'] is int(_episode_id)][0]
        _episode_idx = next((idx for idx, episode in enumerate(_edition['episodes'])
                             if episode['id'] is int(_episode_id)), None)
        data['editions'][_edition_idx]['episodes'][_episode_idx]['highlights'] = _highlights
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

    @staticmethod
    def get_current_buffer_episode_id():
        json_file_path = f'app/data/json/buffer-episodes.json'
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        for episode in data:
            if episode['is_active']:
                return episode['id']
