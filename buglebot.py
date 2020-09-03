"""Main entry file"""
import buglebot
import buglebot.config


def main():
    buglebot.bot.run(buglebot.config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
