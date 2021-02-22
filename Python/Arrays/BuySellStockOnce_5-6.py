import numpy as np
# Brute force approach
# Loop through the array and calculate the max profit for each element in the array (towards the future values)
# return the max


def maximum_profit_brute_force(daily_stock: list) -> int:
    # O(n^2) time complexity  [(n-1) * n] / 2
    # O(n) space complexity
    max_profit = 0
    for m in range(0, len(daily_stock) - 1):
        for following_day in range(m+1, len(daily_stock)):
            if daily_stock[following_day] - daily_stock[m] > max_profit:
                max_profit = daily_stock[following_day] - daily_stock[m]

    return max_profit


# Second approach: create two matrices of N x N, substract them, find max
def maximum_profit(daily_stock: list) -> list:
    # O(n/2) time complexity
    # O(2n) space complexity
    columns = np.tile(np.array(daily_stock)[:, np.newaxis], (1, len(daily_stock)))
    rows = np.tile(np.array(daily_stock), (len(daily_stock), 1))
    price_diff = rows - columns
    r, c = np.triu_indices(len(daily_stock))
    # idx = daily_stock[r, c].argpartition(-1)[-1:]
    # print(columns[r], rows[c])
    return np.max(price_diff[r, c])


def maximum_profit_divide_and_conquer(daily_stock: list) -> int:

    return 0


def maximum_profit_one_pass(stock: list) -> int:

    # Sets a minimum price
    # sets a minimum price for the day
    # compares with the maximum profit, if larger, updates the maximum profit

    min_price = float('inf')
    max_profit = 0
    for price in stock:
        max_profit_today = price - min_price
        max_profit = max(max_profit, max_profit_today)
        min_price = min(price, min_price)
    return max_profit


stock = [310, 315, 275, 295, 260, 270, 290, 230, 255, 250]  # max profit = 30 (260 - 290)

max_prof = maximum_profit(stock)
print('Maximum Profit: {}'.format(max_prof))

max_prof = maximum_profit_brute_force(stock)
print('Maximum Profit Brute Force: {}'.format(max_prof))

max_prof = maximum_profit_one_pass(stock)
print('Maximum Profit One Pass: {}'.format(max_prof))
