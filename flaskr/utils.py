def get_seconds(time: str) -> int:
    """ Get seconds from a time string. """
    hours, minutes = time.split(':')
    return int(hours)*3600 + int(minutes)*60

def convert_time_to_iso(time_str):
    return timedelta(get_seconds(time_str))

def convert_date_to_iso(date_str):
    year, month, day = date_str.split("-")
    return date(int(year), int(month), int(day))
