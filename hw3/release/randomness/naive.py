#!/usr/bin/python3

from binascii import hexlify, unhexlify
import random
#import secret
import os

def buyflag():
#   print(f"This is your flag: {secret.flag}")
    print(f"test")

def generate_randomness(contributions):
    randomness = 0
    for contribution in contributions:
        randomness ^= int.from_bytes(contribution, 'big')
    random.seed(randomness)
    return random.random()

def play():
    contributions = [os.urandom(256) for _ in range(10)]
    for contribution in contributions:
        print(f"Contribution: {hexlify(contribution).decode()}")
    while True:
        new_contribution = input("Give me your contribution (at most 256 bytes) in hexadecimal: ")
        try:
            new_contribution = unhexlify(new_contribution)
            if len(new_contribution) > 256:
                print("Too long")
            else:
                break
        except:
            print("Invalid Value")
    contributions.append(new_contribution)
    result = generate_randomness(contributions)
    if result > 0.5:
        return True
    else:
        return False

def menu(current):
    print('===================')
    print(' 1. play (1G)      ')
    print(' 2. buy flag (200G)')
    print(' 3. exit           ')
    print('===================')
    print(f"Current money: {current}G")

def not_enough():
    print("You don't have enough money.")

if __name__ == "__main__":
    current = 100
    goal = 200
    chance = 200
    print(f"Welcome to my casino. Now you have {current}G.")
    print(f"You need {goal}G to buy the flag.")
    print(f"You have {chance} chances to pay 1G and play. If you win, I will give you 2G!")
    print("Good luck!")
    while True:
        menu(current)
        choice = input('Your choice: ').strip()
        try:
            choice = int(choice)
        except:
            print('Invalid Choice')
            continue
        if choice == 1:
            if chance <= 0:
                print("You don't have any chances!")
                continue
            if current >= 1:
                chance -= 1
                current -= 1
                win = play()
                if win:
                    current += 2
                    print(f"Congratulations! You win in this turn, and now you have {current}G.")
                else:
                    print(f"Oops! You lose in this turn, and now you have {current}G.")
            else:
                not_enough()
            
        elif choice == 2:
            if current >= goal:
                current -= goal
                buyflag()
            else:
                not_enough()
        elif choice == 3:
            exit()
        else:
            print('Invalid Choice')
