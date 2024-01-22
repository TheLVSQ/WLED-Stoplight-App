import json, requests


def check_server(server_ip):
    # Check if the server is online and is a WLED device
    try:
        # Send a GET request to the server
        response = requests.get(f"http://{server_ip}/json/info")
        # Check if the response is valid
        if response.status_code == 200 and response.json()["brand"] == "WLED":
            #print out an ascii art of "LETS GOOO"
            print("""
             _          _   _                                     
            | |        | | ( )                                    
            | |     ___| |_|/ ___    __ _  ___   ___   ___   ___  
            | |    / _ \ __| / __|  / _` |/ _ \ / _ \ / _ \ / _ \ 
            | |___|  __/ |_  \__ \ | (_| | (_) | (_) | (_) | (_) |
            \_____/\___|\__| |___/  \__, |\___/ \___/ \___/ \___/ 
                                    __/ |                        
                                    |___/
            """)

            return True
        elif response.status_code == 200 and response.json()["brand"] != "WLED":
            print("The server is online, but it is not a WLED device. Please make sure you have entered the correct IP Address.")
            return False
        else:
            return False
    except:
        return False

def update_start_end():
    start_time = input("Please enter the start time (in 24h format, e.g., 08:00:00 for 8am): ")
    end_time = input("Please enter the end time (in 24h format, e.g., 23:00:00 for 11pm): ")

    # Check if the start and end times are valid
    #all characters should be numbers except for the colon
    # the format should be HH:MM
    # the hour should be between 00 and 23
    # the minute should be between 00 and 59
    # the start time should be before the end time
    if start_time[0:2].isdigit() and start_time[3:5].isdigit() and start_time[2] == ":" and end_time[0:2].isdigit() and end_time[3:5].isdigit() and end_time[2] == ":" and int(start_time[0:2]) >= 0 and int(start_time[0:2]) <= 23 and int(start_time[3:5]) >= 0 and int(start_time[3:5]) <= 59 and int(end_time[0:2]) >= 0 and int(end_time[0:2]) <= 23 and int(end_time[3:5]) >= 0 and int(end_time[3:5]) <= 59 and start_time < end_time:
        return (start_time, end_time)
    else:
        print("The start and end times are not valid. Please try again.")
        update_start_end()
        print("Press control + c to exit the script.")

def main():
    #print out a cool ascii art banner:
    print("""
    __      __.__  ___________.__       .__  __
    /  \    /  \__|/   _____/|__| _____|__|/  |_
    \   \/\/   /  |\_____  \ |  |/  ___/  \   __\\
     \        /|  |/        \|  |\___ \|  ||  |
      \__/\  / |__/_______  /|__/____  >__||__|
           \/              \/         \/
    """)
    print("WLED Stoplight Config Creator\n")

    # Ask the user for the necessary information
    print("This script will create a config.json file for the WLED Stoplight. Please enter the following information:\n")

    server_ip = input("Please enter the WLED server IP (example 192.168.1.10): ")
    
    server_check = check_server(server_ip)
    
    if server_check == False:
        print("The server is not online. Please make sure it is online with a valid IP Address.")
        print("Would you like to try again? (y/n)")
        try_again = input("")
        if try_again == "y":
            main()
        else:
            print("Exiting...")
            exit()
    elif server_check == True:
        print("The server is online. Continuing...")

    print("\n This script is designed to run each day from defined start and end time. The default start time is 06:00:00 (6am) and the default end time is 23:59:59 (11:59pm). Would you like to change these values? (y/n)")
    change_start_end = input("")

    if change_start_end == "y":

        start_time, end_time = update_start_end()

    else:
        start_time = "06:00:00"
        end_time = "23:59:00"


    # Store the information in a dictionary
    config = {
        "server_ip": server_ip,
        "start_time": start_time,
        "end_time": end_time
    }

    # Write the dictionary to a JSON file
    with open('wled_config.json', 'w') as f:
        json.dump(config, f)

    # Print a confirmation message to the user
    print("SUCCESS!\n")
    print("Settings saved. You can now run the WLED Stoplight script.")
    
if __name__ == "__main__":
    main()