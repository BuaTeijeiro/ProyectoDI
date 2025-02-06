
import locale
import calendar

import eventos

locale.setlocale(locale.LC_TIME, "es_ES")


class Month:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def __str__(self):
        return calendar.month_name[self.month] + " " + str(self.year)

    @staticmethod
    def ofDateTime(self, date):
        return Month(date.year, date.month)

    @staticmethod
    def ofDateString(self, date):
        date = eventos.Eventos.convertStringToDate(date)
        return Month(date.year, date.month)


    def addmonth(self):
        self.month = self.month + 1
        if self.month > 12:
            self.month = 1
            self.year = self.year + 1

    def __le__(self, other):
        return self.year < other.year or (self.year == other.year and self.month <= other.month)
    def __lt__(self, other):
        return self.year < other.year or (self.year == other.year and self.month < other.month)

    def get_nombre(self):
        return calendar.month_name[self.month] +  " " + str(self.year)

if __name__ == "__main__":
    mes = Month(2020, 1)
    print(mes.get_nombre())