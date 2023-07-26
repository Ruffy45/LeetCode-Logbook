import tkinter as tk
import requests
import datetime
import os

def convert_timestamp_to_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def fetch_and_display_submissions():
    username = username_entry.get()
    api_url = f"https://leetcode.com/graphql?query=query%20{{recentSubmissionList(username:%22{username}%22)%20{{title%20timestamp%20statusDisplay%20lang}}}}"
    response = requests.get(api_url)
    data = response.json()

    submissions_listbox.delete(0, tk.END)
    if "data" in data and "recentSubmissionList" in data["data"]:
        submissions = data["data"]["recentSubmissionList"]

        current_week = None
        file_name = None
        for submission in submissions:
            title = submission["title"]
            timestamp = submission["timestamp"]
            status = submission["statusDisplay"]
            lang = submission["lang"]
            time_string = convert_timestamp_to_datetime(timestamp)
            submission_info = f"{title}, {time_string}, {status}, {lang}"

            # Get the week number for the current submission
            week_number = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%U')

            # Create a new file for each week
            if week_number != current_week:
                current_week = week_number
                file_name = f"submissions_week_{current_week}.txt"

            # Append the submission to the corresponding file with the weekly heading
            with open(file_name, "a") as file:
                file.write(f"Week {current_week}\n")
                file.write(submission_info + "\n")

            submissions_listbox.insert(tk.END, submission_info)
    else:
        submissions_listbox.insert(tk.END, "Failed to fetch recent submissions.")

# Tkinter application setup
root = tk.Tk()
root.title("LeetCode Submissions Logger")
root.geometry("500x400")

# Username input field
username_label = tk.Label(root, text="Enter LeetCode Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

# Fetch submissions button
fetch_button = tk.Button(root, text="Fetch Submissions", command=fetch_and_display_submissions)
fetch_button.pack(pady=10)

# Submissions listbox
submissions_listbox = tk.Listbox(root, width=60, height=15)
submissions_listbox.pack(pady=10)

root.mainloop()



