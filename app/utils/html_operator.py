class HtmlOperator:

    @staticmethod
    def save_scene(scene_name, content):
        txt_file_path = f'app/scenes/{scene_name}.html'
        with open(txt_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(str(content))