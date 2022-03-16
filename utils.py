from datetime import datetime, timedelta
from rates_constants import morning_shift, midday_shift, evening_shift, weekends, hourstep
import re

#Regex for days
days_re = '(MO|TU|WE|TH|FR|SA|SU)'

#Convert hours to date
morningstart=datetime.strptime(morning_shift['start'],'%H:%M')
morningsend=datetime.strptime(morning_shift['end'],'%H:%M')
middaystart=datetime.strptime(midday_shift['start'],'%H:%M')
middayend=datetime.strptime(midday_shift['end'],'%H:%M')
eveningstart=datetime.strptime(evening_shift['start'],'%H:%M')
eveningend=datetime.strptime(evening_shift['end'],'%H:%M')

def deserialize_schedules(finput):
    resultarr = []

    
    #Iterate lines
    for line in finput.splitlines():
        pay = 0
        resultobj = {}
        eqsplit = line.split('=')
        resultobj['name'] = eqsplit[0]
        shifts = []
        
        #Iterate shifts
        for hourpair in eqsplit[1].split(','):
            shiftobj = {}
            hour_split = hourpair.split('-')
            shiftobj['day'] = re.match(days_re, hour_split[0])[0]
            shiftobj['start'] = datetime.strptime(hour_split[0].replace(shiftobj['day'], ''),'%H:%M')
            shiftobj['end'] = datetime.strptime(hour_split[1],'%H:%M')
            
            #Checked and calculated here to avoid using another for loop
            check_shift(shiftobj,resultobj['name'])
            pay += calculate_pay(shiftobj)
            shifts.append(shiftobj)
            
        resultobj['shifts'] = shifts
        resultobj['pay'] = pay
        resultarr.append(resultobj)
        
    
    return resultarr

#Can add as many as we need, the ones that wouldn't naturally raise an error
def check_shift(shift,name):
    
    #Check if the start hour is after the end hour
    if shift['start'] > shift['end']:
        raise ValueError('Start time is after end time in {}\'s shift \n{}: {} > {}'.format(name,shift['day'],datetime.strftime(shift['start'], '%H:%M'), datetime.strftime(shift['end'], '%H:%M')))
    if name.isalpha() == False:
        raise ValueError('Name should contain only letters')

def calculate_pay(shift):
    total = 0
    rate = 0
    worked = (shift['end'] - shift['start']).total_seconds() / 3600
    adder = hourstep
    
    #Check if they worked on the weekend
    if shift['day'] in weekends:
        ratetype='rateweekend'
    else:
        ratetype='rate'
        
    #Check rate every step
    while(adder <= worked):
        analyze = shift['start'] + timedelta(hours=adder)
        if morningstart <= analyze <= morningsend:
            rate = morning_shift[ratetype] * hourstep
        elif middaystart <= analyze <= middayend:
            rate = midday_shift[ratetype] * hourstep
        elif eveningstart <= analyze <= eveningend:
            rate = evening_shift[ratetype] * hourstep
        adder += hourstep
        total += rate
        
    return total
