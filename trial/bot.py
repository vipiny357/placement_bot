import os
import requests
from datetime import datetime

TOKEN = "5747160333:AAEqLmWuK1NK9tTA59z62r08e6VEjnqFwQw"

chat_id = "-820273028"  # placement bot group

li = '''[['Very Important Annoucement for all TE '], ['Seminar on Cybersecurity - Register by today end of the day'], ['Removal of the Names of BE Students from Placement List'], ['Economic Times Campus Stars'], ['LTI Mindtree - Session on How to Prepare for Interviews'], ['Amazon 
WoW Learning Platform for Engg Students'], ['TVS Motors Result'], ['Credit Suisse - Internship Test on 28 Feb (TODAY)'], ['Trilogy - Intern Hiring - Test Update'], ['Online Expert Talk by VOIS - 03 March 2023']]'''

URL = f"https://api.telegram.org/bot{TOKEN}"

ress = requests.get(f"{URL}/sendMessage?chat_id={chat_id}&text={li}")
# req=requests.get(url)