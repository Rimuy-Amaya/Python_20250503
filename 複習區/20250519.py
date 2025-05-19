#複習python

#%%
a = int ( input ("請輸入被除數(整數):" ) )
b = int ( input ("請輸入除數(整數，且不為0):" ) )
if b == 0 :
    print("除數不可為0，計算結束。")
else:
    print("商數:",str(a // b),"餘數:",str( a % b ))

# 計算使用者輸入的2個任意數，程式會顯示2數相加的總和
a = float ( input ("請輸入第一個數值:"))
b = float ( input ("請輸入第二個數值:"))
print(f"兩個數的和是{ a + b }")

#%%
#money.py
money = 50000 
cell = int(input("請輸入手機金額:"))
money -= cell
print("剩餘款為:" + str(money)) 

#%%
a = float ( input ("請輸入任意數:"))
print (f"此數的平方是:{a**2}")
print (f"此數的立方是:{a**3}")

a = float ( input ("請輸入任意數:"))
print (f"此數的平方是:{a**2}") 
print (f"此數的立方是:{a**3}") 

#%%
a = float ( input("請輸入第一個數字:"))
b = float ( input("請輸入第二個數字:"))
C = float ( input("請輸入第三個數字:"))
print (f"三個數的總和為:{a+b+c}")

sum = 0
a = float ( input("請輸入第一個數字:"))
sum += a
a = float ( input("請輸入第二個數字:"))
sum += a
a = float ( input("請輸入第三個數字:"))
sum += a
print("三個數的總和為:",sum)

#%%
price = int (input("輸入顧客購買金額:"))
if price >= 100000:
    price = price * 0.8
elif price >= 50000:
    price = price * 0.85
elif price >= 30000:
    price = price * 0.9
elif price >= 10000:
    price = price * 0.95
print("實付金額是:",price)

price = int(input("輸入顧客購買金額:"))

if price >= 100000:
    price = price * 0.8
elif price >= 50000:
    price = price * 0.85
elif price >= 30000:
    price = price * 0.9
elif price >= 10000:
    price = price * 0.95

print("實付金額是:", price)
