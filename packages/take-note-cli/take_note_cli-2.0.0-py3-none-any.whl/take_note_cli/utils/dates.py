from datetime import date, timedelta

WEEK = 7


def get_monday(the_date: date):
    return the_date - timedelta(days=(the_date.isoweekday() - 1))


def format_header_date(the_date: date):
    return the_date.strftime("%A %d %B %Y")


def format_file_date(the_date: date):
    return the_date.strftime("%Y-%m-%d")


def get_time_delta_from_options(options):
    delta = timedelta(0)
    if options.lastWeek:
        delta = timedelta(-WEEK)
    elif options.nextWeek:
        delta = timedelta(WEEK)

    return delta


def get_weeks_delta(weeks: int):
    if weeks >= 0:
        return timedelta(WEEK * weeks)
    else:
        raise ValueError("Batch size must be 0 or greater.")
