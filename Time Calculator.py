from datetime import datetime

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

def seconder(day, month, year, hour, minute, second):
    monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    leap_years = (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    days = (year - 1) * 365 + leap_years

    for i in range(month - 1):
        days += monthdays[i]

    if month > 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
        days += 1

    days += day - 1

    total_seconds = days * 86400 + hour * 3600 + minute * 60 + second
    return total_seconds

def calendar_difference(d1, m1, y1, h1, min1, s1, d2, m2, y2, h2, min2, s2):
    if (y2, m2, d2, h2, min2, s2) < (y1, m1, d1, h1, min1, s1):
        d1, m1, y1, h1, min1, s1, d2, m2, y2, h2, min2, s2 = d2, m2, y2, h2, min2, s2, d1, m1, y1, h1, min1, s1

    def get_monthdays(month, year):
        if month == 2:
            return 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
        return [31,28,31,30,31,30,31,31,30,31,30,31][month - 1]

    sec = s2 - s1
    if sec < 0:
        sec += 60
        min2 -= 1

    minute = min2 - min1
    if minute < 0:
        minute += 60
        h2 -= 1

    hour = h2 - h1
    if hour < 0:
        hour += 24
        d2 -= 1

    day = d2 - d1
    if day < 0:
        m2 -= 1
        if m2 == 0:
            m2 = 12
            y2 -= 1
        day += get_monthdays(m2, y2)

    month = m2 - m1
    if month < 0:
        month += 12
        y2 -= 1

    year = y2 - y1

    return year, month, day, hour, minute, sec

def inputchecker(prompt):
    while True:
        try:
            userinput = input(prompt).strip()

            if userinput.lower() == "now":
                now = datetime.now()
                return now.day, now.month, now.year, now.hour, now.minute, now.second

            parts = userinput.split()
            if len(parts) not in [6, 7]:
                raise ValueError("You must provide 6 values (or 7 with AM/PM), or 'now'.")

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
            print("Invalid input. Please enter day, month, year, hour, minute, second, and optional AM/PM, or type 'now'.")

day1, month1, year1, hour1, minute1, second1 = inputchecker("Enter the first time (day month year hour minute second): ")
day2, month2, year2, hour2, minute2, second2 = inputchecker("Enter the second time (day month year hour minute second): ")

seconds = abs(seconder(day2, month2, year2, hour2, minute2, second2) -
              seconder(day1, month1, year1, hour1, minute1, second1))

print(f"\nTotal Seconds: {integ(seconds)}")
print(f"Total Minutes: {integ(seconds / 60)}")
print(f"Total Hours: {integ(seconds / 3600)}")
print(f"Total Days: {integ(seconds // 86400)}")
print(f"Total Months: {round((seconds // 86400) / 30.436875, 2)}")
print(f"Total Years: {round((seconds // 86400) / 365.2425, 2)}")

y, mo, d, h, mi, s = calendar_difference(day1, month1, year1, hour1, minute1, second1,
                                        day2, month2, year2, hour2, minute2, second2)

print("\n" + ", ".join(
    f"{v} {label}{'s' if v != 1 else ''}"
    for v, label in zip([y, mo, d, h, mi, s], ["Year", "Month", "Day", "Hour", "Minute", "Second"])
    if v
))
