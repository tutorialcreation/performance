from dateutil.relativedelta import relativedelta


def convert_to_seconds(date_data):
        years=int(date_data.years)* 365*24*60*60
        days=int(date_data.days)*24*60*60
        hours=int(date_data.hours)*60*60
        minutes=int(date_data.minutes)*60
        seconds=int(date_data.seconds)
        date_in_seconds=years+days+hours+minutes+seconds
        return date_in_seconds