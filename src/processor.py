import re
import math
import datetime
import time

'''
    These rules collectively define how many points should be awarded to a receipt.

    One point for every alphanumeric character in the retailer name.
    50 points if the total is a round dollar amount with no cents.
    25 points if the total is a multiple of 0.25.
    5 points for every two items on the receipt.
    If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    6 points if the day in the purchase date is odd.
    10 points if the time of purchase is after 2:00pm and before 4:00pm.
'''
rule2_pattern = r'^\\d+\\.00$'

rules = [
            lambda x: sum([1 if c.isalnum() else 0 for c in x['retailer']]), # One point for every alphanumeric character in the retailer name.
            lambda x: 50 if re.match(rule2_pattern, x['total']) else 0, # 50 points if the total is a round dollar amount with no cents.
            lambda x: 25 if float(x['total'])%0.25==0 else 0, # 25 points if the total is a multiple of 0.25.
            lambda x: len(x['items'])//2 * 5, # 5 points for every two items on the receipt.
            # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
            lambda x: sum([math.ceil(float(item['price'])*0.2) if len(item['shortDescription'].strip())%3==0 else 0 for item in x['items']]),
            lambda x: 6 if datetime.datetime.strptime(x['purchaseDate'], "%Y-%m-%d").date().day % 2 == 1 else 0, # 6 points if the day in the purchase date is odd.
            lambda x: 10 if time.strptime('16:00', "%H:%M") > time.strptime(x['purchaseTime'], "%H:%M:%S") > time.strptime('14:00', "%H:%M") else 0 # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        ]

async def calculate_points(receipt):
    points = 0
    for rule in rules:
        points += rule(receipt)
    return points