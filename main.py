import discord
from discord.ext import commands
import logging
import random
# import regex

from my_secrets import DISCORD_BOT_TOKEN

BotIntents = discord.Intents.default()
BotIntents.message_content = True
BotIntents.members = True

bot = commands.Bot(command_prefix="!", intents=BotIntents)

DICE_VALUE2IMAGE_STR = {
    -1: ":brown_square: ",
    0: ":white_large_square: ",
    1: ":green_square: ",
}

SKILL_VALUE2NAME = {
    12: "Legendary+++",
    11: "Legendary+++",
    10: "Legendary++",
    9: "Legendary+",
    8: "Legendary",
    7: "Epic",
    6: "Fantastic",
    5: "Superb",
    4: "Great",
    3: "Good",
    2: "Fair",
    1: "Average",
    0: "Mediocre",
    -1: "Poor",
    -2: "Terrible",
    -3: "Terrible+",
    -4: "Terrible++",
    -5: "Terrible+++",
    -6: "Terrible++++",
}
SKILL_NAME2VALUE = {v: k for k, v in SKILL_VALUE2NAME.items()}


def roll_fate_dice(number_dice: int) -> tuple[str, int]:
    rolls = [random.randint(-1, 1) for _ in range(number_dice)]
    value = sum(rolls)
    s = " ".join([DICE_VALUE2IMAGE_STR[v] for v in rolls])
    return s, value


def parse_roll_command(user_input: str) -> tuple[str, int]:
    """
    Expecting one of these input formats:
    * /roll
    * /roll climbing
    * /roll acrobticts +2
    """
    user_input = user_input.lower().removeprefix('/roll ').strip()
    words = user_input.split()

    if len(words) == 0:
        return "skill", 0

    if len(words) == 1:
        return words[0], 0
    else:
        try:
            skill_modifier = int(words[1])
        except Exception:
            # todo: add warning or something
            skill_modifier = 0
        return words[0], skill_modifier


@bot.event
async def on_ready():
    print(f"Super Fate Bot started: {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    if msg.lower().startswith("/roll"):
        try:
            skill_name, skill_modifier = parse_roll_command(msg)
            dice_result_str, roll_value = roll_fate_dice(4)

            bot_reply_msg = (
                f"{message.author.name}: Your {skill_name}({skill_modifier:+}) check {dice_result_str}\n"
                f"=> {roll_value:+}{skill_modifier:+} = **{roll_value+skill_modifier:+} "
                f"[{SKILL_VALUE2NAME.get(roll_value + skill_modifier, "Extrem!!")}]**"
            )
            await message.reply(bot_reply_msg)

        except Exception as e:
            await message.reply(f"Uhhhh! Internal error: {e!r}")

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)


# Irrelevant commands from tutorial :-)
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")


def main():
    log_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )
    bot.run(DISCORD_BOT_TOKEN, log_handler=log_handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    main()
