#import edu 導入package 呼叫函式要寫edu.tools.caculate_bmi

#from edu.tools import caculate_bmi,get_state 從某一個module裡面匯入自定義函式，呼叫函式要寫caculate_bmi

from edu.tools import caculate_bmi as a1 #從某一個module裡面匯入自定義函式，並命名為a1。呼叫函式直接寫a1。
from edu.tools import get_state as a2 #從某一個module裡面匯入自定義函式，並命名為a2。呼叫函式直接寫a1。

#上面三種呼叫函式的方式都可以使用，需要搭配不同的程式碼，以成功呼叫所需要的函式。

def main():
    height:int = int(input("請輸入身高(cm):"))
    weight:int = int(input("請輸入體重(kg):"))

    bmi = a1(height, weight)

    print(bmi)
    print(a2(bmi))


if __name__ == '__main__':
    main()