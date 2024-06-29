import tkinter as tk
from tkinter import messagebox
import instaloader
import pandas as pd
import re

class InstagramScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Scraper")

        self.label = tk.Label(root, text="Enter Instagram Username:")
        self.label.pack()

        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.label_password = tk.Label(root, text="Enter Instagram Password:")
        self.label_password.pack()

        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.pack()

        self.label_target = tk.Label(root, text="Enter Target Username:")
        self.label_target.pack()

        self.target_entry = tk.Entry(root)
        self.target_entry.pack()

        self.scrape_button = tk.Button(root, text="Scrape", command=self.scrape)
        self.scrape_button.pack()

        self.result_text = tk.Text(root, height=20, width=50)
        self.result_text.pack()

    def scrape(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        target = self.target_entry.get()

        if not username or not password or not target:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Scraping data for {target}...\n")

        try:
            data = self.scrape_instagram(username, password, target)
            self.save_to_excel(data, target)
            self.result_text.insert(tk.END, "Scraping completed and saved to Excel.")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {e}")

    def scrape_instagram(self, username, password, target):
        L = instaloader.Instaloader()

        # Login with the provided username and password
        L.login(username, password)

        # Get target profile
        profile = instaloader.Profile.from_username(L.context, target)

        user_data = []

        # Iterate over the followees
        for followee in profile.get_followees():
            user_info = {
                'username': followee.username,
                'fullname': followee.full_name,
                'bio': followee.biography,
                'external_url': followee.external_url,
                'email': '',
                'phone': ''
            }

            # You can extract email and phone from the biography if present
            email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
            phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')
            user_info['email'] = email_pattern.findall(followee.biography)
            user_info['phone'] = phone_pattern.findall(followee.biography)

            user_data.append(user_info)

        return user_data

    def save_to_excel(self, data, username):
        df = pd.DataFrame(data)
        df.to_excel(f"{username}_following.xlsx", index=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramScraperApp(root)
    root.mainloop()
