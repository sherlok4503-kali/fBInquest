import json
import sys
import os
import time
import getpass
import requests
from dotenv import load_dotenv

# Load environment variables (App ID & Secret) from .env file
load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# Color codes for Linux terminal
if sys.platform in ["linux", "linux2"]:
    W = "\033[0m"
    G = "\033[32;1m"
    R = "\033[31;1m"
else:
    W = ""
    G = ""
    R = ""

# Ensure the 'cookie' directory exists
os.makedirs('cookie', exist_ok=True)

# Banner Function
def banner():
    print(W + "\n" + "F B I".center(44))
    print(W + "     [" + G + "Facebook Information" + W + "]\n")

# Show program details
def show_program():
    print(G)
    print("                    INFORMATION")
    print("------------------------------------------------------")
    print("    Author:      Hak9")
    print("    Name:        Facebook Information")
    print("    Version:     Full Version")
    print("    Date:        August 13, 2018")
    print("    Jabber:      xhak9x@jabber.de")
    print("\n* If you find any errors or problems, please contact the author.")
    print(W)

# Display available commands
def commands():
    print(G)
    print("COMMAND             DESCRIPTION")
    print("------------------- ---------------------------------")
    print("get_info           Show information about your friend")
    print("token              Generate access token (OAuth 2.0)")
    print("cat_token          Show your access token")
    print("rm_token           Remove access token")
    print("refresh_token      Refresh long-lived access token")
    print("clear              Clear terminal")
    print("help               Show help")
    print("about              Show information about this program")
    print("exit               Exit the program")
    print(W)

# Validate access token before using it
def validate_token(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    try:
        response = requests.get(url, timeout=5)
        user_data = response.json()
        if "error" in user_data:
            print(f"[!] Invalid token: {user_data['error']['message']}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        print("[!] Network error. Check your internet connection.")
        return False
    except requests.exceptions.Timeout:
        print("[!] Request timed out.")
        return False

# OAuth 2.0 authentication (User must manually input their token)
def get_token():
    print("[!] Facebook now requires OAuth 2.0 for authentication.")
    print("[!] Follow these steps to get your access token:")
    print("1. Go to: https://developers.facebook.com/tools/explorer/")
    print("2. Select your App and request 'public_profile' and 'email' permissions.")
    print("3. Generate a User Access Token and paste it below.")
    token = input("[?] Enter your access token: ")

    if not validate_token(token):
        print("[!] Invalid token. Please try again.")
        return

    token_file = "cookie/token.log"
    with open(token_file, "w") as b:
        b.write(token)
        print("[*] Access token saved successfully.")

# Fetch user details using stored access token
def fetch_user_details():
    token_file = "cookie/token.log"
    
    if not os.path.exists(token_file):
        print("[!] No token found. Please login first.")
        return

    try:
        with open(token_file, "r") as file:
            token = file.read().strip()

        if not validate_token(token):
            print("[!] Invalid or expired token. Please login again.")
            return

        response = requests.get(f"https://graph.facebook.com/me?fields=name,email&access_token={token}", timeout=5)
        user_data = response.json()

        if "error" in user_data:
            print(f"[!] Error: {user_data['error']['message']}")
        else:
            print(f"[+] User: {user_data.get('name', 'N/A')}")
            print(f"[+] Email: {user_data.get('email', 'N/A')}")
    except requests.exceptions.ConnectionError:
        print("[!] Network error. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("[!] Request timed out.")

# Refresh long-lived access token (requires APP_ID & APP_SECRET)
def refresh_token():
    token_file = "cookie/token.log"
    if not os.path.exists(token_file):
        print("[!] No token found. Please login first.")
        return

    with open(token_file, "r") as file:
        old_token = file.read().strip()

    url = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={old_token}"
    
    try:
        response = requests.get(url)
        new_token = response.json().get("access_token")

        if new_token:
            with open(token_file, "w") as file:
                file.write(new_token)
            print("[*] Token refreshed successfully!")
        else:
            print("[!] Failed to refresh token. Please login again.")
    except requests.exceptions.ConnectionError:
        print("[!] Network error. Token refresh failed.")

# Remove access token
def remove_token():
    token_file = "cookie/token.log"
    if os.path.exists(token_file):
        os.remove(token_file)
        print("[*] Access token removed successfully.")
    else:
        print("[!] No token found.")

# Main menu
def main():
    banner()
    show_program()
    
    while True:
        command = input("\nEnter command (type 'help' for options): ").strip().lower()
        
        if command == "help":
            commands()
        elif command == "get_info":
            fetch_user_details()
        elif command == "token":
            get_token()
        elif command == "rm_token":
            remove_token()
        elif command == "refresh_token":
            refresh_token()
        elif command == "exit":
            print("Exiting...")
            sys.exit()
        else:
            print("[!] Invalid command. Type 'help' for a list of valid commands.")

if __name__ == "__main__":
    main()
