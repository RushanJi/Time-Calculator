def integ(value):
    value = float(value)
    if value.is_integer():
        return int(value) 
    else:
        return round(value, 2) 

def valid(day, month, year, hour, minute, second):
    if month < 1 or month > 12:
        return False

    monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  
        monthdays[1] = 29  
            
    if not (1 <= day <= monthdays[month - 1]):
        return False

    if not (0 <= hour < 24):
        return False
    if not (0 <= minute < 60):
        return False
    if not (0 <= second < 60):
        return False

    return True

def masher(n, m):
    y, mo, d, h, mi, s = 0, 0, 0, 0, 0, 0
    year = 1
    month = 1
    day = 1

    while True:
        days_in_year = 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365
        if n >= days_in_year * 86400:
            y += 1
            n -= days_in_year * 86400
            year += 1
        else:
            break

    monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        monthdays[1] = 29

    month = 1
    while month <= 12:
        seconds_in_month = monthdays[month - 1] * 86400
        if n >= seconds_in_month:
            mo += 1
            n -= seconds_in_month
            month += 1
        else:
            break

    d = n // 86400
    n %= 86400

    h = n // 3600
    n %= 3600

    mi = n // 60
    s = n % 60

    if m == "Years":
        if y != 0:
            return f"{integ(y)} Year{'s' if y != 1 else ''}, "
        else:
            return ""
    elif m == "Months":
        if mo != 0:
            return f"{integ(mo)} Month{'s' if mo != 1 else ''}, "
        else:
            return ""
    elif m == "Days":
        if d != 0:
            return f"{integ(d)} Day{'s' if d != 1 else ''}, "
        else:
            return ""
    elif m == "Hours":
        if h != 0:
            return f"{integ(h)} Hour{'s' if h != 1 else ''}, "
        else:
            return ""
    elif m == "Minutes":
        if mi != 0:
            return f"{integ(mi)} Minute{'s' if mi != 1 else ''}, "
        else:
            return ""
    elif m == "Seconds":
        if s != 0:
            return f"{integ(s)} Second{'s' if s != 1 else ''} "
        else:
            return ""

def seconder(day, month, year, hour, minute, second):
    monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0): 
        monthdays[1] = 29 

    total_days = (year - 1) * 365 + (year - 1) // 4  
    for i in range(month - 1):
        total_days += monthdays[i]

    total_days += day - 1

    total_seconds = total_days * 86400 + hour * 3600 + minute * 60 + second
    return total_seconds

def difference(day1, month1, year1, hour1, minute1, second1, day2, month2, year2, hour2, minute2, second2):
    time1_seconds = seconder(day1, month1, year1, hour1, minute1, second1)
    time2_seconds = seconder(day2, month2, year2, hour2, minute2, second2)

    diff_seconds = abs(time2_seconds - time1_seconds)

    diff_minutes = diff_seconds / 60
    diff_hours = diff_seconds / 3600
    diff_days = diff_seconds // 86400
    diff_months = diff_days / 30.436875
    diff_years = diff_days / 365.2425 

    return diff_seconds, diff_minutes, diff_hours, diff_days, diff_months, diff_years

def inputchecker(prompt):
    while True:
        try:
            userinput = input(prompt)
            parts = userinput.strip().split()

            if len(parts) not in [6, 7]:
                raise ValueError("You must provide 6 values (or 7 with AM/PM).")

            values = list(map(integ, parts[:6]))
            day, month, year, hour, minute, second = values

            if len(parts) == 7:
                am_pm = parts[6].upper()
                if am_pm == "PM" and 1 <= hour < 12:
                    hour += 12
                elif am_pm == "AM" and hour == 12:
                    hour = 0

            if valid(day, month, year, hour, minute, second):
                return day, month, year, hour, minute, second
            else:
                print("Invalid date or time values. Please check and try again.")
        except ValueError:
            print("Invalid input. Please enter day, month, year, hour, minute, second, and optional AM/PM.")

day1, month1, year1, hour1, minute1, second1 = inputchecker("Enter the first time (day month year hour minute second): ")

day2, month2, year2, hour2, minute2, second2 = inputchecker("Enter the second time (day month year hour minute second): ")

seconds, minutes, hours, days, months, years = difference(day1, month1, year1, hour1, minute1, second1, day2, month2, year2, hour2, minute2, second2)

print(f"Total Seconds: {integ(seconds)}")
print(f"Total Minutes: {integ(minutes)}")
print(f"Total Hours: {integ(hours)}")
print(f"Total Days: {integ(days)}")
print(f"Total Months: {integ(months)}")
print(f"Total Years: {integ(years)}")
print(f"\n{masher(seconds, 'Years')}{masher(seconds, 'Months')}{masher(seconds, 'Days')}{masher(seconds, 'Hours')}{masher(seconds, 'Minutes')}{masher(seconds, 'Seconds')}")
