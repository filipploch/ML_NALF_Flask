from datetime import datetime, timedelta


class DateOperator:
    @staticmethod
    def get_last_day_date(day_name):
        day_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                       'sunday': 6}
        _day = day_of_week[day_name]
        _today_date = datetime.now()
        _today_day_nr = _today_date.weekday()
        _days_difference = (_today_day_nr - _day) % 7
        _last_day_date = _today_date - timedelta(days=_days_difference)
        return _last_day_date.strftime("%Y-%m-%d")

    @staticmethod
    def get_next_day_date(day_name):
        day_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                       'sunday': 6}
        _day = day_of_week[day_name]
        _today_date = datetime.now()
        _today_day_nr = _today_date.weekday()
        _days_difference = (day_of_week[day_name] - _today_day_nr + 7) % 7
        _next_day_date = _today_date + timedelta(days=_days_difference)
        return _next_day_date.strftime("%Y-%m-%d")

