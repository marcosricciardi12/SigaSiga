import time
import os
from pyfiglet import Figlet
from colorama import Fore, Style

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_large_text(text, font='standard'):
    f = Figlet(font=font)
    clear_screen()
    print(f.renderText(text))

def animate_text(text, font='standard', speed=0.1):
    f = Figlet(font=font)
    clear_screen()
    for i in range(len(text)+1):
        print(f.renderText(text[:i]))
        time.sleep(speed)
        clear_screen()

def main():
    text = input("Ingrese el texto a mostrar: ")
    print_large_text(text)
    time.sleep(2)
    animate_text(text)

if __name__ == "__main__":
    main()
