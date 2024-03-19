class EpisodeDataParser:

    @staticmethod
    def parse_best_five_form_data(request_form):
        best_five = []

        # Grupowanie elementów formularza
        grouped_data = {}
        for key, value in request_form.items():
            if key == "episodeId" or key == "mvp-radio" or key == 'competitionId':
                continue
            parts = key.split('-')
            group_name = parts[0]
            index = int(parts[-1])

            if index not in grouped_data:
                grouped_data[index] = {}

            grouped_data[index][group_name] = value

        # Przekształcanie do oczekiwanej konstrukcji
        for index, data in grouped_data.items():
            best_five.append({
                "name": data.get("name", ""),
                "team": data.get("team", ""),
                "mvp": data.get("mvp", ""),
            })

        return best_five

    @staticmethod
    def parse_highlights_form_data(request_form):
        highlights = []

        # Grupowanie elementów formularza
        grouped_data = {}
        for key, value in request_form.items():
            if key == "episodeId":
                continue
            parts = key.split('-')
            group_name = parts[0]
            index = int(parts[-1])

            if index not in grouped_data:
                grouped_data[index] = {}

            grouped_data[index][group_name] = value

        # Przekształcanie do oczekiwanej konstrukcji
        for index, data in grouped_data.items():
            highlights.append({
                "url": data.get("url", ""),
                "teams": data.get("teams", ""),
                "video_id": EpisodeDataParser.get_youtube_video_id(data["url"]),
                "is_active": False,
            })

        return highlights

    @staticmethod
    def get_youtube_video_id(url):
        if "youtube.com" in url:
            video_id_start = url.find("v=") + 2
            video_id_end = url.find("&", video_id_start)
            if video_id_end == -1:
                return url[video_id_start:]
            else:
                return url[video_id_start:video_id_end]