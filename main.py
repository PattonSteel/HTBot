from bot import Bot
import json

def main():
    #Read the data JSON
    with open('config.json','r') as file:
        data = json.load(file)

    # Create bot object and run
    bot = Bot()
    bot.run(data.get("bot_token"))

if __name__ == "__main__":
    main()