

class TxtOperator:
    @staticmethod
    def write_text(text):
        txt_file_path = 'app/data/txt/logs.txt'
        with open(txt_file_path, 'a') as text_file:
            text_file.writelines(str(text) + '\n')

