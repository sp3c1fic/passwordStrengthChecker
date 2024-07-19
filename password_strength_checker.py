import re
import sys
import time
import math
from colorama import init, Fore, Style

init(autoreset=True)

MIN_PASS_LENGTH = 8

class PasswordStrengthChecker:
    def __init__(self):
        self.password = ""
    
    def _get_password_from_user(self): 
        self.password = input(Fore.CYAN + "Enter password that you would like to test: ")
     
    def _not_common(self):
        try:
            with open("top-100.txt.txt", 'r') as file:
                lines = file.readlines()
                stripped_lines = [line.strip() for line in lines]
                
                return self.password not in stripped_lines
        except FileNotFoundError as e:
            print(e)
            sys.exit(0)
    
    def estimate_cracking_time(self):
        # Define the character set size
        charset_size = 0
        if re.search(r'[a-z]', self.password):
            charset_size += 26
        if re.search(r'[A-Z]', self.password):
            charset_size += 26
        if re.search(r'\d', self.password):
            charset_size += 10
        if re.search(r'[^a-zA-Z\d\s]', self.password):
            charset_size += 32  # Assume 32 special characters
    
        # Calculate the entropy of the password
        entropy = len(self.password) * math.log2(charset_size)
    
        # Estimate the number of guesses needed
        num_guesses = 2 ** entropy
    
        # Define the attack rates
        offline_fast_rate = 10**10  # 10 billion guesses per second
        offline_slow_rate = 10**6   # 1 million guesses per second
        online_rate = 10**3         # 1 thousand guesses per second
    
        # Calculate the time to crack in seconds
        offline_fast_time = num_guesses / offline_fast_rate
        offline_slow_time = num_guesses / offline_slow_rate
        online_time = num_guesses / online_rate
    
        # Convert time to more readable format (years, days, hours, minutes, seconds)
        def convert_seconds(seconds):
            years = seconds // (365*24*3600)
            seconds %= (365*24*3600)
            days = seconds // (24*3600)
            seconds %= (24*3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            return years, days, hours, minutes, seconds
    
        offline_fast_time_converted = convert_seconds(offline_fast_time)
        offline_slow_time_converted = convert_seconds(offline_slow_time)
        online_time_converted = convert_seconds(online_time)
    
        def format_time(time_tuple):
            years, days, hours, minutes, seconds = time_tuple
            return (f" {years} years, {days} days, {hours} hours, "
                        f"{minutes} minutes, {seconds} seconds")
    
        print(Fore.YELLOW + f"Estimated cracking time (offline fast attack): {format_time(offline_fast_time_converted)}")
        print(Fore.YELLOW + f"Estimated cracking time (offline slow attack): {format_time(offline_slow_time_converted)}")
        print(Fore.YELLOW + f"Estimated cracking time (online attack): {format_time(online_time_converted)}")
        
    def check_password_strength(self):
        while True:
            self._get_password_from_user()

            if self.password.strip() == "":
                print(Fore.RED + 'Password cannot be empty or just spaces: Re-enter again')
                continue
                        
            has_numbers = bool(re.search(r'[\\d]', self.password))
            has_lowercase = bool(re.search(r'[a-z]', self.password))
            has_uppercase = bool(re.search('[A-Z]', self.password))
            has_special_chars = bool(re.search(r'[^a-zA-Z\\d\\s]', self.password))            
            strength = "Weak"
           
            if len(self.password) >= MIN_PASS_LENGTH:               
                if has_lowercase and has_uppercase and has_numbers and has_special_chars and self._not_common():
                    strength = 'Strong'
                elif (has_lowercase or has_uppercase) and has_numbers:
                    strength = 'Moderate'
                else:
                    strength = "Weak"
            else:
                strength = 'Weak'
            print(Fore.GREEN + f"Password strength: {strength}")

def print_welcome_message():
    welcome_text = Fore.BLUE + Style.BRIGHT + """
        ___________________________________________________
        |                                                 |
        |          Welcome to the Password Checker        |
        |_________________________________________________|
        """
    ascii_art = Fore.MAGENTA + Style.BRIGHT + """
          _____                                _               
         |  __ \                              | |              
         | |__) | __ _____  ___   _ __ ___   __| | ___ _ __ ___ 
         |  ___/ '__/ _ \ \/ / | | '_ ` _ \ / _` |/ _ \ '__/ _ \\
         | |   | | |  __/>  <| |_| | | | | | (_| |  __/ | |  __/
         |_|   |_|  \___/_/\_\\__, |_| |_| |_|\__,_|\___|_|  \___|
                               __/ |                            
                              |___/                             
        """
    print(welcome_text)
    print(ascii_art)
    time.sleep(2)  # Pause for 2 seconds to allow the user to read the welcome message
 
def main():
    checker = PasswordStrengthChecker()
    
    try:
        print_welcome_message()
        checker.check_password_strength()
        checker.estimate_cracking_time()
        
        
    except KeyboardInterrupt:
        print('\nKeyboard interruption detected. Closing script ...')
        sys.exit(0)
    
if __name__ == "__main__":
    main()
    