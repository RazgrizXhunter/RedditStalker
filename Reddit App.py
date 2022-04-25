import requests
import json
from datetime import datetime

actions = ["comments", "submitted"]
url = "https://www.reddit.com/{}/{}/{}.json?limit=1"

def main():
    show_menu()

def show_menu():
	print("Welcome to the stalker app for Reddit!\n")
	target = input("Who do you wanna stalk?\nu/")
	
	if check_activity(target):
		print("Active in the last hour.")
	else:
		print("Inactive in the last hour.")

def check_activity(target):
	was_active = False

	for action in actions:
		if was_active:
			break

		info = get_target_info("user", target, action)
		last_date = get_date_from_info(info)

		print("Action: {}, Date of action: {}, UTC Now: {}".format(action, last_date, datetime.utcnow()))

		if last_date is not None:
			time_elapsed = (datetime.utcnow() - last_date).seconds / 3600
			was_active = time_elapsed <= 1
	
	return was_active

def get_target_info(subject, target, action):
	formatted_url = url.format(subject, target, action)

	result = requests.get(formatted_url, headers = {"User-Agent": "Last seen on Reddit"})

	if result.status_code == 404:
		print("User does not exist")
		input("Press enter to exit")
		exit(-1)

	return result.json()

def get_date_from_info(info):
	entries = info["data"]["children"]
	
	if len(entries) > 0:
		return datetime.utcfromtimestamp(entries[0]["data"]["created_utc"])
	else:
		return None

if __name__ == "__main__":
    main()

input("Press enter to exit.")
