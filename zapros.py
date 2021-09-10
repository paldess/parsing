import requests

response = requests.get("https://i.instagram.com/api/v1/friendships/47892002753/following/?count=12", headers={'user_agent': 'Instagram 155.0.0.37.107'})

print()