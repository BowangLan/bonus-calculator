# Bonus Calculator

This is a program for calculating the bonus given some order and some incomes.

## Some Definitions

Total income: the sum of all order's amount.

Actual income: the sum of all income's amount.

Order: an order adds a certain amount to the total income.

- If the order's money is paid, then that money is added to the actual income. This money is called income of the order.
- If the order's money is unpaid, this means that there's no corresponding income to this order.

Income: an income represent the incoming money that come from a certain order.

Bonus:

## How

See this flowchard for how the bonus is calculated: https://whimsical.com/bonus-calculator-EY9iipKuBuxqHWrUMSpzqT

The main calculation is done in the `BonusCalculator` class. When creating an instance, this class takes in an instance of `DataLoaderBase` , which will be used to load the data inside `BonusCalculator` class.
