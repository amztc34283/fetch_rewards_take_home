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
rule2_pattern = r'^\d+\.00$'

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

"""
Calculate the points awarded for a given receipt using a set of rules.

Args:
    receipt (dict): A dictionary representing a receipt with the following keys:
        - 'retailer' (str): The name of the retailer.
        - 'total' (str): The total amount of the receipt.
        - 'items' (list): A list of dictionaries representing the items on the receipt, each with the following keys:
            - 'price' (str): The price of the item.
            - 'shortDescription' (str): A short description of the item.
        - 'purchaseDate' (str): The date of the purchase in the format 'YYYY-MM-DD'.
        - 'purchaseTime' (str): The time of the purchase in the format 'HH:MM:SS'.

Returns:
    int: The total number of points awarded for the receipt.
"""
async def calculate_points(receipt):
    points = 0
    for rule in rules:
        points += rule(receipt)
    return points