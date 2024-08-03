""" Delivers methods to operate with dates and times objects. """

import calendar
from typing import Literal
import datetime
from dateutil.relativedelta import relativedelta
import requests

class Dates:
    """ Delivers methods to operate with dates and times objects. """
    def __init__(self) -> None:
        self._date: datetime.datetime = datetime.date.today()
        self.week_days: dict[str, int] = { 'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6 }

    def new_date(self, day: int, month: int, year: int, output_format: str = '%d.%m.%Y', format: Literal['str', 'date'] = 'str') -> str | datetime.date:
        """
        Return new date in given format (default: %d.%m.%Y) or date object

        Args:
            day (int): day of month (1 - 31)
            month (int): month of year (1 - 12)
            year (int): year
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        return datetime.date(year, month, day).strftime(output_format) if format == 'str' else datetime.date(year, month, day)
        
    def convert_to_date(self, date_string: str, date_format: str | None = '%d.%m.%Y') -> datetime.date:
        """
        Convert string date to date object using given date format.

        Args:
            date_string (str): date string, ex. 12.12.2022
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            
        Returns:
            datetime.date: date object
        """
        return datetime.datetime.strptime(date_string, date_format).date()

    def change_date_format(
            self, 
            date_string: str | None = None, 
            date_format: str = '%d.%m.%Y', 
            output_format: str = '%d.%m.%Y'
    ) -> str:
        """
        Convert the date from one format to another (default: %d.%m.%Y)

        Args:
            date_string (str): date string, ex. 12.12.2022
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.

        Returns:
            str: date string in given format

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date: datetime.datetime = self.__to_datetime__(date_string, date_format)
        return _date.strftime(output_format)

    def offset(
            self, 
            date: str | datetime.date, 
            date_format:str = '%d.%m.%Y',
            days: int | None = None, 
            months: int | None = None, 
            years: int | None = None, 
            output_format: str = '%d.%m.%Y',
            format: Literal['str', 'date'] = 'str'
    ) -> str | datetime.date:
        """
        Returns new date string or date object calculated by adding or substracting given value (days, months, years) to/from given date

        Args:
            date (str | datetime.date): date string or object.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            days (int | None, optional): positive or negative value of the offset. Defaults to None.
            months (int | None, optional): positive or negative value of the offset. Defaults to None.
            years (int | None, optional): positive or negative value of the offset. Defaults to None.
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or datetime.date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        if days is not None:
            _date += relativedelta(days=days)
        if months is not None:
            _date += relativedelta(months=months)
        if years is not None:
            _date += relativedelta(years=years)

        return _date.strftime(output_format) if format == 'str' else _date.date()

    def today(self, output_format='%d.%m.%Y', format: Literal['str', 'date'] = 'str') -> str | datetime.date:
        """
        Returns today's date in given string format (%d.%m.%Y as default) or date object

        Args:
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        return datetime.datetime.today().strftime(output_format) if format == 'str' else self._date.today().date()

    def yesterday(self, output_format='%d.%m.%Y', format: Literal['str', 'date'] = 'str') -> str | datetime.date:
        """
        Returns yesterday's date in given string format (%d.%m.%Y as default) or date object

        Args:
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object
        """
        _date = datetime.datetime.today() - datetime.timedelta(days=1)
        return _date.strftime(output_format) if format == 'str' else _date.date()

    def tomorrow(self, output_format='%d.%m.%Y', format: Literal['str', 'date'] = 'str') -> str | datetime.date:
        """
        Returns tomorrow's date in given string format (%d.%m.%Y as default) or date object

        Args:
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object
        """
        _date = datetime.datetime.today() + datetime.timedelta(days=1)
        return _date.strftime(output_format) if format == 'str' else _date.date()

    def next_working_day(
            self, 
            date: str | datetime.date | None = None,
            date_format:str = '%d.%m.%Y',
            include_holidays: bool = False, 
            country_code: str | None = None, 
            output_format: str = '%d.%m.%Y',
            format: Literal["str", "date"] = 'str'
    ) -> str | datetime.date:
        """
        Returns date (str or date object) of next working day (ommitting weekends and holidays if included)

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            include_holidays (bool, optional): determines if holidays should be included or not. Defaults to False.
            country_code (str | None, optional): country code ex. 'PL'. Full list available here: https://date.nager.at/Country. Defaults to None.
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        if _date.weekday() == 4: # Friday
            _date += datetime.timedelta(days=3)
        elif _date.weekday() == 5: # Saturday
            _date += datetime.timedelta(days=2)
        else: # Rest of days
            _date += datetime.timedelta(days=1)

        if include_holidays is True and country_code is not None:
            while self.is_public_holiday(country_code, _date.strftime(date_format), date_format) is True or _date.weekday() in [5, 6]:
                _date += datetime.timedelta(days=1)
        elif include_holidays is True and country_code is None:
            raise ValueError('invalid country_code')

        return _date.strftime(output_format) if format == 'str' else _date.date()

    def previous_working_day(
            self, 
            date: str | datetime.date | None = None,
            date_format:str = '%d.%m.%Y',
            include_holidays: bool = False, 
            country_code: str | None = None, 
            output_format: str = '%d.%m.%Y',
            format: Literal["str", "date"] = 'str'
    ) -> str:
        """
        Returns date (str or date object) of previous working day (ommitting weekends and holidays if included)

        Args:
            date_string (str | None, optional): date string. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            date (datetime.date, optional): date object. Defaults to None.
            include_holidays (bool, optional): determines if holidays should be included or not. Defaults to False.
            country_code (str | None, optional): country code ex. 'PL'. Full list available here: https://date.nager.at/Country. Defaults to None.
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        if _date.weekday() == 0: # Monday
            _date = _date - datetime.timedelta(days=3)
        elif _date.weekday() == 6: # Sunday
            _date = _date - datetime.timedelta(days=2)
        else: # Rest of days
            _date = _date - datetime.timedelta(days=1)

        if include_holidays is True and country_code is not None:
            while self.is_public_holiday(country_code, _date.strftime(date_format), date_format) is True or _date.weekday() in [5, 6]:
                _date -= datetime.timedelta(days=1)
        elif include_holidays is True and country_code is None:
            raise ValueError('invalid country_code')

        return _date.strftime(output_format) if format == 'str' else _date.date()

    def first_day_of_month(
            self, 
            date: str | datetime.date | None = None,
            date_format: str = '%d.%m.%Y',
            output_format="%d.%m.%Y",
            format: Literal["str", "date"] = 'str'
    ) -> str | datetime.date:
        """
        Returns the first day of month for given string date in given string format (%d.%m.%Y as default) or date object.

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            output_format (str, optional): pythonic date format. Defaults to "%d.%m.%Y".
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format).replace(day=1)
        return _date.strftime(output_format) if format == 'str' else _date.date()
        
    def last_day_of_month(
            self, 
            date: str | datetime.date | None = None,
            date_format: str = '%d.%m.%Y',
            output_format="%d.%m.%Y",
            format: Literal["str", "date"] = 'str'
    ) -> str | datetime.date:
        """
        Returns the last day of month for given string date in given string format (%d.%m.%Y as default) or date object.

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            output_format (str, optional): pythonic date format. Defaults to "%d.%m.%Y".
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        _date = _date.replace(day=calendar.monthrange(_date.year, _date.month)[1])
        return _date.strftime(output_format) if format == 'str' else _date

    def calculate_date_of_weekday(
            self, 
            date: str | datetime.date | None = None,
            date_format: str = '%d.%m.%Y', 
            week_day: Literal['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'] = 'mon', 
            output_format="%d.%m.%Y",
            format: Literal["str", "date"] = 'str'
    ) -> str | datetime.date:
        """
        Return the date of the week day from the week for given date in given output format (default (%d.%m.%Y)) or date object.

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            date (datetime.date, optional): date object. Defaults to None.
            week_day (Literal['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], optional): weekday. Defaults to 'mon'.
            output_format (str, optional): pythonic date format. Defaults to "%d.%m.%Y".
            format ('str' | 'date', optional): output format. Defaults to 'str'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        monday: datetime.datetime = _date - datetime.timedelta(days=_date.weekday())
        res: datetime.datetime = monday + datetime.timedelta(days=self.week_days[week_day])
        return res.strftime(output_format) if format == 'str' else res.date()

    def day_of_year(self, date: str | datetime.date | None = None, date_format: str = '%d.%m.%Y') -> int:
        """
        Returns the day of year.

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.

        Returns:
            int: number value of the day of year

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        return int(_date.strftime('%j'))

    def week_of_year(self, date: str | datetime.date | None = None, date_format: str = '%d.%m.%Y', iso_format: bool = True) -> int:
        """
        Returns the number of the week in ISO 8601 or non-ISO standard.

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            iso_format (bool, optional): pythonic date format. Defaults to True.

        Returns:
            int: number value of week of the year

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        match iso_format:
            case True:
                return(int(_date.isocalendar().week))
            case False:
                return int((_date - _date.replace(month=1, day=1)).days / 7) + 1

    def difference_between_dates(
            self, 
            first_date: str | datetime.date, 
            second_date: str | datetime.date, 
            date_format: str = '%d.%m.%Y', 
            unit: Literal['seconds', 'minutes', 'hours', 'days'] = 'days'
    ) -> int:
        """
        Return the difference between two dates in given unit

        Args:
            first_date (str | datetime.date): date string or object of the first date 
            second_date (str | datetime.date): date string or object of the second date
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            unit (Literal['seconds', 'minutes', 'hours', 'days'], optional): measure unit. Defaults to 'days'.

        Returns:
            int: number value of the difference in selected unit (ex. days)

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        try:
            _date1: datetime.datetime = self.__to_date__(first_date, date_format)
            _date2: datetime.datetime = self.__to_date__(second_date, date_format)
            diff: datetime.timedelta = _date1 - _date2

            match unit:
                case 'seconds':
                    return abs(diff.seconds)
                case 'minutes':
                    return abs(diff.min)
                case 'hours':
                    return abs(diff.min) / 60
                case 'days':
                    return abs(diff.days)
        except Exception as ex:
            raise Exception from ex

    def get_fiscal_year(self, date: str | datetime.date | None = None, date_format: str = '%d.%m.%Y', start_month_of_fiscal_year: int = 4) -> int:
        """
        Return the fiscal year for given date

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            start_month_of_fiscal_year (int, optional): the number value of the first month of fiscal year. Defaults to 4.

        Returns:
            int: number value of the fiscal year

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        return _date.year if _date.month < start_month_of_fiscal_year else _date.year + 1

    def get_fiscal_month(self, date: str | datetime.date | None = None, date_format: str = '%d.%m.%Y', start_month_of_fiscal_year: int = 4) -> int:
        """
        Return the fiscal month for given date

        Args:
            date (str | date | None, optional): date string or object. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            start_month_of_fiscal_year (int, optional): the number value of the first month of fiscal year. Defaults to 4.

        Returns:
            int: number value of the fiscal month

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        return (_date - relativedelta(months=start_month_of_fiscal_year-1)).month
        
    def get_public_holidays(self, country_code: str, year: int, dates_only: bool = True, date_format: str = '%d.%m.%Y') -> dict | list:
        """
        Return holidays for given year and given country.
        Use https://date.nager.at API
        List of countries: https://date.nager.at/Country

        Args:
            country_code (str): country code, ex. PL
            year (int): number value of the year
            dates_only (bool, optional): determines if results should contains only dates (list). Defaults to True.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.

        Returns:
            dict | list: all holidays for the given country and the year
        """
        url: str = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}'
        response: requests.Response = requests.get(url)
        if response.status_code == 200:
            holidays: dict = {item['date']: item['name'] for item in response.json()}
            return [self.change_date_format(date_string, '%Y-%m-%d', date_format) for date_string in list(holidays.keys())] if dates_only is True else holidays

    def is_public_holiday(self, country_code: str, date: str | datetime.date | None = None, date_format: str = '%d.%m.%Y') -> bool:
        """
        Check if given date is public holiday in given country.\n\r
        Use https://date.nager.at API\n\r
        List of countries: https://date.nager.at/Country\n\r

        Args:
            country_code (str): country code, ex. PL
            date (str | date | None, optional): date string. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.

        Returns:
            bool: True if the date is holiday, False if not

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        
        url: str = f'https://date.nager.at/api/v3/PublicHolidays/{_date.year}/{country_code}'
        response: requests.Response = requests.get(url)
        if response.status_code != 200:
            raise requests.RequestException

        holidays: list = [self.change_date_format(item['date'], '%Y-%m-%d', date_format) for item in response.json()]
        date_string = _date.strftime(date_format) if isinstance(date, datetime.date) else date
        return date_string in holidays

    def nth_working_day_of_month(self,
            date: str | datetime.date | None = None, 
            date_format: str = '%d.%m.%Y', 
            day: int = None, 
            holidays: list[str] | None = None,
            output_format: str = "%d.%m.%Y",
            format: Literal['str', 'date'] = 'str'
        ) -> str | datetime.date:
        """
        Return the nth businees day of month in given string format (ommitting weekends and holidays if included) or datetime.date object.

        Args:
            date (str, date, optional): date string or object. Defaults to None. If none, calculate the nth businees day of current month.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            days (int): positive value of the nth business day. Defaults to None.
            holidays (list, optional): list of date. Default to None. If none, holidays will be excluded. 
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)
        _date = self.last_day_of_month(date=self.offset(date=_date, months=-1), format='date')

        holidays = [self.convert_to_date(holiday_date, date_format) for holiday_date in holidays]

        working_days = 0
        while working_days != day:
            _date +=  datetime.timedelta(days=1)
            if _date.weekday() not in [5,6] and _date not in holidays:
                working_days += 1
        return _date.strftime(output_format) if format == 'str' else _date

    def working_day_offset(self,
        date: str | datetime.date | None = None, 
        date_format: str = '%d.%m.%Y', 
        days_offset: int = None, 
        holidays: list[str] = [],
        output_format: str = "%d.%m.%Y",
        format: Literal['str', 'date'] = 'str'
    ) -> str | datetime.date:
        """
        Return date string or object of the previous/next nth working day from the given date.

        Args:
            date (str, date, optional): date string. Defaults to None.
            date_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            days (int): positive or negative value of the offset. Defaults to None.
            holidays (list, optional): list of date. Default to None. If none, holidays will be excluded. 
            output_format (str, optional): pythonic date format. Defaults to '%d.%m.%Y'.
            format (str, date): output format. Default to 'str'

        Returns:
            str | datetime.date: date string in given format or date object

        More about date formats:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        """
        _date = self.__to_date__(date, date_format)

        holidays = [self.convert_to_date(holiday_date, date_format) for holiday_date in holidays]

        working_days = 0
        while working_days != abs(days_offset):
            if days_offset > 0:
                _date += datetime.timedelta(1)
            elif days_offset < 0:
                _date -= datetime.timedelta(1)

            if _date.weekday() not in [5, 6] and _date not in holidays:
                working_days += 1

        return _date.strftime(output_format) if format == 'str' else _date


    def __to_datetime__(self, date_string: str | None = None, date_format: str = '%d.%m.%Y'):
        if date_string is None:
            return datetime.datetime.today()
        return datetime.datetime.strptime(date_string, date_format)
    
    def __to_date__(self, date: str | datetime.date | None = None, date_format: str | None = '%d.%m.%Y'):
        if isinstance(date, str):
            return self.__to_datetime__(date, date_format).date()
        
        if isinstance(date, datetime.date):
            return date
        
        return datetime.datetime.today()
