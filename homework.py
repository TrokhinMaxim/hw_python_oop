import datetime as dt


date_format = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        '''Сохраняем новую запись о расходах.'''
        self.records.append(record)

    def get_today_stats(self):
        '''Получаем данные за сегодня'''
        today = dt.date.today()
        total = 0
        for record in self.records:
            if today == record.date:
                total += record.amount
        return total

    def get_currency(self):
        my_total = self.get_today_stats()
        differency = self.limit - my_total
        return differency

    def get_week_stats(self):
        '''Получаем данные за неделю.'''
        total = 0
        today = dt.date.today()
        week = today - dt.timedelta(days=7)
        for days in self.records:
            if week <= days.date <= today:
                total += days.amount
        return total


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        '''Определяем, сколько ещё калорий можно/нужно получить сегодня.'''
        answer = self.get_currency()
        if answer > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {answer} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.2
    EURO_RATE = 86.3
    RUB = 1.0

    def get_today_cash_remained(self, currency):

        difference = self.get_currency()
        currency_dict = {'usd': ('USD', self.USD_RATE),
                         'eur': ('Euro', self.EURO_RATE),
                         'rub': ('руб', self.RUB)
                         }
        flag, rate = currency_dict[currency]
        result = abs(round(difference / rate, 2))
        if difference == 0:
            return 'Денег нет, держись'
        if difference > 0:
            return f'На сегодня осталось {result} {flag}'
        return f'Денег нет, держись: твой долг - {result} {flag}'
