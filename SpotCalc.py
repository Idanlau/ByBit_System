from sympy import symbols, solve
import datetime
import gspread


amt = float(input("How much crypto did you intend to buy? "))

paid = float(input("USDT/USDC paid?"))


real_amt = amt*0.999

print("You actually own " + str(real_amt) + "of the purchased crypto due to trading fees.")

x = symbols('x')

expr = (real_amt*x*0.999 > paid)

sol = solve(expr)

print("Selling price needs to be at least " + str(sol) + " to make profit")

#Wrtie profit calculator
#Write the least amt of coins to sell



if input("Would you like to log onto google sheets y/n? ") == "y":
    sa = gspread.service_account(filename = "/Users/idanlau/Downloads/bybit-344307-351f58a1c2d6.json")
    sh = sa.open("Crypto Trade")

    val = sh.values_get(range='Spot Trades!A:A')
    val = len(val['values']) + 1

    wks = sh.worksheet("Spot Trades")
    pair = input("What Crypto Pair? ")
    BuyPrice = float(input("Price Per Crypto "))
    wks.update(f'A{val}:G{val}',[[str(datetime.datetime.utcnow()),str(pair),str(BuyPrice),str(real_amt),str(paid),str(sol),None]])


if input("Would you calculate profit? y/n") == "y":
    selling_price = float(input("What selling price? "))
    print(f"Profit is {(real_amt*selling_price)-paid}")