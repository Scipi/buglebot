"""Main entry file"""
import bugle_bot
import bugle_bot.config


def main():
    bugle_bot.client.run(bugle_bot.config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
