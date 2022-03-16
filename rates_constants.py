# Monday - Friday
# 00:01 - 09:00 25 USD
# 09:01 - 18:00 15 USD
# 18:01 - 00:00 20 USD
# Saturday and Sunday
# 00:01 - 09:00 30 USD
# 09:01 - 18:00 20 USD
# 18:01 - 00:00 25 USD

# Date conversion in utils to avoid importing datetime here and keeping the parameters simple

morning_shift = {
    'start': '00:01',
    'end': '09:00',
    'rate': 25,
    'rateweekend': 30
}

midday_shift = {
    'start': '09:01',
    'end': '18:00',
    'rate': 15,
    'rateweekend': 20
}

evening_shift = {
    'start': '18:01',
    'end': '23:59',
    'rate': 20,
    'rateweekend': 25
}

weekends = ['SA','SU']

#Defines how often we need to check for the rate
#hourtep = 1 #Every hour
#hourtep = 0.25 #Every 15 minutes
hourstep = 0.5