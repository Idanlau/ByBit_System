from sympy import symbols, solve
import datetime
import gspread


usd_amt = float(input("How much usdt/usdc did you put in? "))
apy = float(input("APY? "))*0.01 #Convert percentage to decimal
crypto_returns = float(input("Crypto return + original proceeds shown on the order? "))
days = int(input("Staking period in days? "))

print("If the cyrpto price is above benchmarkprice: ")
print("You recieve " + str(usd_amt*(1+(apy*(days/365)))) + "USDT/USDC.")

print("If cyrpto price is below benchmark: ")
x = symbols('x')
expr = (crypto_returns*x*0.999 > usd_amt)
sol = solve(expr)
print("Selling price needs to be at least " + str(sol) + " to make profit")

y = symbols('y')
expr = (crypto_returns*y*0.999 > (usd_amt*(1+(apy*(days/365)))))
sol2 = solve(expr)
print("Optimal prices of the crypto " + str(sol2) +
      " to make profit, you would make more than if crypto price was above benchmark price.")


if input("Would you like to log onto google sheets y/n? ") == "y":

    #SpreadSheet input
    sa = gspread.service_account(filename = "/Users/idanlau/Downloads/bybit-344307-351f58a1c2d6.json")
    sh = sa.open("ByBit Dual Asset Minning")
    wks = sh.worksheet("Crypto Trade")
    val = int(input("What line? "))
    pair = input("What Crypto Pair? ")
    BenchMarkPrice = float(input("BenchMark Price? "))
    wks.update(f'A{val}:H{val}',[[str(datetime.datetime.utcnow()),str(pair),str(apy),str(BenchMarkPrice),str(crypto_returns),
                                  str(sol),str(sol2),str(usd_amt)]])


