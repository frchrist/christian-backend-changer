from perfectmoney import PerfectMoney as pm

#remember to put it env
p = pm(a, b)
balance = p.balance()


if not balance:
    print(p.error)
else:
    print(balance)


res = p.spend("U29763801", "U27906293", 0.01)
print(res)

