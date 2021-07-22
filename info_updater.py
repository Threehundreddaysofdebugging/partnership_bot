import schedule

from misc import update_advertisers_cost


schedule.every().day.at('4:30').do(update_advertisers_cost)
