import random
import sqlite3

conn = sqlite3.connect('card.s3db')

database = conn.cursor()
database.execute('CREATE TABLE IF NOT EXISTS card ( \
                    id INTEGER, \
                    number TEXT, \
                    pin TEXT, \
                    balance INTEGER DEFAULT 0)')

def menu():
    while True:
        print('1. Create an account\n2. Log into account\n0. Exit')
        option = int(input())
        if option == 0:
            print('\nBye!')
            conn.close()
            break
        if option == 1:
            create_account()
        elif option == 2:
            cn = input('\nEnter your card number:\n')
            pn = input('Enter your pin:\n')
            database.execute(f'SELECT number, pin FROM card WHERE number = {cn} AND pin = {pn}')
            conn.commit()
            if database.fetchone() is None:
                print('\nWrong card number or PIN!\n')
            else:
                print('\nYou have successfully logged in!\n')
                login(cn, pn)


def create_account():
    card_number = '400000'
    pin = ''
    for _ in range(9):
        card_number += str(random.randint(0, 9))
    cs = checksum(card_number)
    card_number += cs #str(random.randint(1, 9))
    #print(cs)
    for _ in range(4):
        pin += str(random.randint(0,9))
    #database[card_number] = pin  #FIX
    database.execute('INSERT INTO card VALUES (?, ?, ?, ?)', (1, card_number, pin, 0))
    print(f'\nYour card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}')
    conn.commit()

def checksum(card_number):
    multiply_by_2 = ''
    subtract9 = ''
    sum = 0
    checksum = 0
    odd = 1
    for i in list(card_number):
        if odd % 2 == 1:
            multiply_by_2 += str(int(i) * 2)
            odd += 1
        else:
            multiply_by_2 += i
            odd += 1
    for i in list(multiply_by_2):
        if int(i) > 9:
            subtract9 += str(int(i) - 9)
        else:
            subtract9 += i
    for i in list(subtract9):
        sum += int(i)
    
    if sum % 10 == 0:
        return str(checksum)
    else:
        checksum = 10 - (sum % 10)
        return str(checksum)

def checkluhn(num):
    multiply_by_2 = ''
    subtract9 = ''
    sum = 0
    odd = 1
    for i in list(num):
        if odd % 2 == 1:
            multiply_by_2 += str(int(i) * 2)
            odd += 1
        else:
            multiply_by_2 += i
            odd += 1
    for i in list(multiply_by_2):
        if int(i) > 9:
            subtract9 += str(int(i) - 9)
        else:
            subtract9 += i
    for i in list(subtract9):
        sum += int(i)
    
    if sum % 10 != 0:
        return False
    else:
        return True

    
def login(card_number, pin):
    while True:
        print('''1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit''')
        option = int(input())
        if not option:
            print('\nBye!')
            conn.close()
            exit()
        if option == 1:
            database.execute(f'SELECT balance FROM card WHERE number = {card_number} AND pin = {pin}')
            balance = (database.fetchone())[0]
            print(f'\nBalance: {balance}\n')
            conn.commit()
        elif option == 2:
            income = input('\nEnter income:\n')
            database.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {card_number} AND pin = {pin}')
            print('Income was added!\n')
            conn.commit()
        elif option == 3:
            print('\nTranfer\n')
            num = input('Enter card number:\n')
            if checkluhn(num):
                database.execute(f'SELECT number FROM card WHERE number = {num}')
                if database.fetchone() is None:
                    print('Such a card does not exist.\n')
                else:
                    money = int(input('Enter how much money you want to transfer:\n'))
                    database.execute(f'SELECT balance FROM card WHERE number = {card_number}')
                    balance = (database.fetchone())[0]
                    if balance < money:
                        print('Not enough money!\n')
                    else:
                        database.execute(f'UPDATE card SET balance = balance - {money} WHERE number = {card_number}')
                        database.execute(f'UPDATE card SET balance = balance + {money} WHERE number = {num}')
                        print('Success!\n')
                    conn.commit()
            else:
                print('Probably you made mistake in the card number. Please try again!\n')  
            conn.commit()
        elif option == 4:
            database.execute(f'DELETE FROM card WHERE number = {card_number} AND pin = {pin}')
            conn.commit()
            print('\nThe account has been closed!\n')
        elif option == 5:
            print('\nYou have successfully logged out!\n')
            break
    conn.commit()
            
menu()      