import mysql.connector
import pywhatkit
import random
from datetime import datetime
import pyqrcode
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vivek@1999",
    database="atm_bank"
)
cur = conn.cursor()
cur.execute("select username from login_user")
active = cur.fetchone()[0]
ty = str(datetime.now())[10:13]
ty1 = str(datetime.now())[14:16]
time_now = str(datetime.now())[:-7]


def tabel():
    cur.execute("""create table profiles (id int auto_increment primary key, name varchar(50) not null ,
    password varchar(50), balance int (0))""")
    conn.commit()


def sing_up():
    username = input("Enter Your Name: ")
    password = input("Enter Password: ")
    conf_password = input("Enter Conform Password: ")
    balance = input("Enter Amount: ")
    mobile_number = input("Enter Mobile Number: ")
    if password == conf_password:
        cur.execute(f"create table {username} (id int auto_increment primary key, deposit varchar(50),"
                    f"withdraw varchar(50), balance varchar(50),transfer varchar(50), receive varchar(50),"
                    f"date_time varchar(50) not null) ")
        cur.execute(f"insert into profiles (name, password, balance,card_number, cvv_number,mobile_number) values ('{username}', "
                    f"{password}, {balance},0,0,{mobile_number})")
        conn.commit()
        cur.execute(f"insert into {username} (deposit, withdraw, balance,transfer, receive,date_time) values (0, 0, {balance},"
                    f"0, 0,'{time_now}')")
        conn.commit()
        cur.execute(f"update login_user set username = '{username}' ")
        conn.commit()
    else:
        print("Password Does Not Match")


def login():
    username = input("Enter Your Name: ")
    password = input("Enter Password: ")
    cur.execute(f"select * from profiles where name = '{username}'")
    users = cur.fetchone()
    if users and users[2] == password:
        print("Login Successful")
        cur.execute(f"update login_user set username = '{username}'")
        conn.commit()
    else:
        print("User Doesn't Found")


def deposit():
    balance = input("Enter Amount: ")
    cur.execute(f"update profiles set balance = balance + {balance} where name = '{active}'")
    conn.commit()
    cur.execute(f"select balance from profiles where name = '{active}'")
    balance1 = cur.fetchone()[0]
    cur.execute(f"""insert into {active} (deposit, balance,transfer, receive,date_time) values ({balance}, {balance1}, 
                0, 0,'{time_now}')""")
    conn.commit()
    print(f"{balance}rs Deposited Successfully")


def withdraw():
    balance = input("Enter Amount: ")
    cur.execute(f"update profiles set balance = balance - {balance} where name = '{active}'")
    conn.commit()
    cur.execute(f"select balance from profiles where name ='{active}'")
    balance1 = cur.fetchone()[0]
    cur.execute(f"insert into {active} (withdraw, balance, transfer, receive,date_time) values ({balance}, {balance1}, "
                f"0, 0,'{time_now}')")
    conn.commit()
    print(f"{balance}rs Withdraw Successfully")


def check_balance():
    cur.execute(f"select balance from profiles where name = '{active}' ")
    balance = cur.fetchone()[0]
    print(balance)


def update_card():
    card_number = input("Enter 6 digit Card Numbers: ")
    cvv_number = input("Enter 3 Digit CVV Numbers: ")
    if len(card_number) == 6 and len(cvv_number) == 3:
        cur.execute(
            f"update profiles set card_number ={card_number}, cvv_number = {cvv_number} where name = '{active}' ")
        conn.commit()
    else:
        print("Enter 6 and 3 digit Numbers")


def transfer_money():
    account_Holder = input("Enter Name to Transfer Money: ")
    amount = input("Enter Transfer Money: ")
    cur.execute(f"select mobile_number from profiles where name = '{account_Holder}'")
    mobile = cur.fetchone()
    OTP1 = random.randint(1000, 9999)
    msg = f"{active} sending to you {amount}.Your otp is {OTP1} "
    pywhatkit.sendwhatmsg(f"+{mobile}", msg, int(ty), int(ty1) + 1)
    OTP = int(input("Enter OTP to send Money: "))
    if OTP == OTP1:
        cur.execute(f"update profiles set balance = balance - {amount} where name = '{active}' ")
        conn.commit()
        cur.execute(f"update profiles set balance = balance + {amount} where name = '{account_Holder}' ")
        conn.commit()
        cur.execute(f"select balance from profiles where name = '{active}'")
        balance1 = cur.fetchone()[0]
        cur.execute(f"insert into {active} (transfer, receive,balance,date_time) values ({amount}, 0, {balance1},"
                    f"'{time_now}') ")
        conn.commit()
        cur.execute(f"select balance from profiles where name = '{account_Holder}'")
        balance2 = cur.fetchone()[0]
        cur.execute(f"insert into {account_Holder} (receive, transfer, balance,date_time) values ({amount},0,{balance2}"
                    f",'{time_now}') ")
        conn.commit()
    else:
        print("You Entered Wrong OTP")


"""def mobile_number():
    mobile_number = input("Enter Mobile Number: ")
    cur.execute(f"update profiles set  mobile_number = +91{mobile_number}  where name = '{active}' ")
    conn.commit()
"""


def Ministatement():
    cur.execute(f"Select * from {active}")
    ministatement = cur.fetchall()
    for i in ministatement:
        print(i)


def main():
    cur.execute("select username from login_user")
    active = cur.fetchone()[0]
    if active != "None":
        print("Welcome", active)
    else:
        print("PLZ Login")
    print("""Select Option
    1.sing_Up
    2.Login
    3.Deposit
    4.Withdraw
    5.Check_Balance
    6.Update Card
    7.Transfer Money
    8.MiniStatement""")
    ch = int(input("Enter Choice: "))
    if ch == 1:
        sing_up()
    elif ch == 2:
        login()
    elif ch == 3:
        if active == 'None':
            print("PLease Login")
        else:
            deposit()
    elif ch == 4:
        if active == 'None':
            print("PLease Login")
        else:
            withdraw()
    elif ch == 5:
        if active == 'None':
            print("PLease Login")
        else:
            check_balance()
    elif ch == 6:
        if active == 'None':
            print("PLease Login")
        else:
            update_card()
    elif ch == 7:
        if active == 'None':
            print("PLease Login")
        else:
            transfer_money()
    elif ch == 8:
        if active == 'None':
            print("PLease Login")
        else:
            Ministatement()
    else:

        cur.execute("update login_user set username = 'None'")
        conn.commit()
        exit()


if __name__ == "__main__":
    main()
