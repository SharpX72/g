import telebot
from telebot import types

API_TOKEN = '8173392198:AAGtcVk3uoKVnrsKdQ3LX0TByW8_zHojuXs'  # Replace with your actual Telegram bot API token
bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store registered users
registered_users = {}

# Replace with your actual channel link
CHANNEL_LINK = 'https://t.me/+GgdLoUSOMv0wNDNl'  # Replace with your actual channel link

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "Welcome to the Sharp Crackers Giveaway Bot!\nPlease register by clicking the button below."
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    register_button = types.KeyboardButton("Register for Giveaway")
    rules_button = types.KeyboardButton("Rules")
    channel_button = types.KeyboardButton("Join Channel")
    markup.add(register_button, rules_button, channel_button)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Registration handler
@bot.message_handler(func=lambda message: message.text == "Register for Giveaway")
def register(message):
    msg = bot.send_message(message.chat.id, "Please enter your name to register:")
    bot.register_next_step_handler(msg, process_registration)

def process_registration(message):
    user_id = message.chat.id
    user_name = message.text
    registered_users[user_id] = user_name

    # Save the name to the file
    save_to_file(user_name)

    # Confirmation message
    confirmation_text = f"Thank you, {user_name}! You have been registered for the giveaway!"
    bot.send_message(user_id, confirmation_text)

    # Show buttons for further actions
    show_actions(user_id)

def save_to_file(user_name):
    with open("giveaway_participants.txt", "a") as file:
        file.write(user_name + "\n")

def show_actions(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    view_participants_button = types.KeyboardButton("View Participants")
    cancel_button = types.KeyboardButton("Cancel Registration")
    rules_button = types.KeyboardButton("Rules")
    channel_button = types.KeyboardButton("Join Channel")
    markup.add(view_participants_button, cancel_button, rules_button, channel_button)
    bot.send_message(user_id, "What would you like to do next?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "View Participants")
def view_participants(message):
    if registered_users:
        participants = "\n".join(registered_users.values())
        bot.send_message(message.chat.id, f"Participants:\n{participants}")
    else:
        bot.send_message(message.chat.id, "No participants registered yet.")

@bot.message_handler(func=lambda message: message.text == "Cancel Registration")
def cancel_registration(message):
    user_id = message.chat.id
    if user_id in registered_users:
        del registered_users[user_id]
        remove_from_file(message.text)  # Remove user from the file as well
        bot.send_message(user_id, "Your registration has been canceled.")
    else:
        bot.send_message(user_id, "You are not registered.")

def remove_from_file(user_name):
    with open("giveaway_participants.txt", "r") as file:
        lines = file.readlines()
    with open("giveaway_participants.txt", "w") as file:
        for line in lines:
            if line.strip("\n") != user_name:
                file.write(line)

@bot.message_handler(func=lambda message: message.text == "Rules")
def send_rules(message):
    rules_text = (
        "Giveaway Rules:\n"
        "1. You must be a member of the SHARP CRACKS channel.\n"
        "2. You can only register once.\n"
        "3. Winners will be chosen randomly.\n"
        "4. The giveaway ends on [insert end date].\n"
        "5. The winners will be announced in the channel."
        "5. THANK YOU DIL SE SHARP CRACKS."
    )
    bot.send_message(message.chat.id, rules_text)

@bot.message_handler(func=lambda message: message.text == "Join Channel")
def join_channel(message):
    bot.send_message(message.chat.id, f"Click here to join the channel: {CHANNEL_LINK}")

# Run the bot
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)
