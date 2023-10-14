from dataclasses import dataclass


@dataclass 
class Date:
    month: int
    week: int
    day: int
    
    
def from_num(x: int) -> Date:
    if x < 111 or x > 999:
        raise RuntimeError('Date is invalid')
    d = Date()
    d.day = x % 10
    x = x // 10
    d.week = x % 10
    x = x // 10
    d.month = x % 10
    return d

def days_passed(d : Date) -> int:
    return (d.day - 1) + (d.week - 1) * 7 + (d.month - 1) * 28 

def weeks_passed(d: Date) -> int:
    return (d.month-1)* 4 + (d.week - 1)
