from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import pymongo
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://Cenzo:Cenzo123@cenzo.azbk1.mongodb.net/")
db = client["esports_db"]
registered_ids = db["registered_ids"]
registrations = db["registrations"]
approved_teams = db["approved_teams"]
stats = db["stats"]
queries = db["queries"]

OWNER_ID = 6663845789 # Replace with your owner ID
LOG_GROUP_ID = -1002360512395  # Replace with your log group ID
BOT_TOKEN = "7690782362:AAGX57kDAHcCoCs6xr1JqxoBg5TuPGDutjM"  # Replace with your bot token

# Global Variables
TOURNAMENT_MODE = "off"  # Default mode: off

# Commands Implementation

# /start Command
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Updates", url="https://t.me/updates_channel")],
        [InlineKeyboardButton("Support Chat", url="https://t.me/support_chat")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    image_url = "https://i.ibb.co/NFXHprf/file-2404.jpg"  # Replace with your image link
    caption = (
        "Welcome to the eSports Tournament Bot!\n\n"
        "Use /register to register for tournaments and /query for queries."
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=caption,
        reply_markup=reply_markup,
    )

# /query Command - Directs users to @Rizeol
def query(update: Update, context):
    update.message.reply_text("For queries, please contact @Rizeol.")

# /add Command
def add(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        ids = update.message.text.split()[1:]  # Split command and IDs
        if ids:
            registered_ids.delete_many({})  # Clear existing IDs
            for uid in ids:
                registered_ids.insert_one({"uid": uid})
            update.message.reply_text("IDs added successfully.")
        else:
            update.message.reply_text("Please provide Telegram UIDs.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /aBroadcast Command
def a_broadcast(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        message = " ".join(context.args)
        if message:
            ids = registered_ids.find()
            for user in ids:
                try:
                    context.bot.send_message(chat_id=user["uid"], text=message)
                except Exception:
                    continue
            update.message.reply_text("Broadcast sent successfully.")
        else:
            update.message.reply_text("Please provide a message to broadcast.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /reset Command
def reset(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        registered_ids.delete_many({})
        update.message.reply_text("All IDs have been reset.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /mode Command
def mode(update: Update, context):
    global TOURNAMENT_MODE
    if update.message.from_user.id == OWNER_ID:
        if len(context.args) == 1 and context.args[0] in ["off", "solo", "squad"]:
            TOURNAMENT_MODE = context.args[0]
            update.message.reply_text(f"Tournament mode set to {TOURNAMENT_MODE}.")
        else:
            update.message.reply_text("Usage: /mode [off/solo/squad]")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /register Command
def register(update: Update, context):
    if TOURNAMENT_MODE == "off":
        keyboard = [[InlineKeyboardButton("Updates", url="https://t.me/updates_channel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Tournament registration is currently closed.", reply_markup=reply_markup)
    elif TOURNAMENT_MODE == "solo":
        update.message.reply_text("Enter your BGMI UID and In-Game Name (format: UID NAME).")
        # Further implementation for collecting details goes here...
    elif TOURNAMENT_MODE == "squad":
        update.message.reply_text("Enter your Team Name, 4 Players' UIDs, and Names.")
        # Further implementation for collecting details goes here...

# /check Command
def check(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        approved = approved_teams.find()
        if approved.count() > 0:
            response = "Currently Registered Teams:\n\n"
            for team in approved:
                response += f"Team Name: {team['team_name']}\nPlayers:\n"
                for player in team['players']:
                    response += f"- {player['uid']} ({player['name']})\n"
                response += "\n"
            update.message.reply_text(response)
        else:
            update.message.reply_text("No approved teams found.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /stats Command
def stats_command(update: Update, context):
    total_matches = stats.find_one({"type": "matches"}) or {"count": 0}
    solo_matches = stats.find_one({"type": "solo"}) or {"count": 0}
    squad_matches = stats.find_one({"type": "squad"}) or {"count": 0}
    total_users = stats.find_one({"type": "users"}) or {"count": 0}
    total_players = stats.find_one({"type": "players"}) or {"count": 0}
    
    response = (
        f"Total Matches Played: {total_matches['count']}\n"
        f"Solo Matches Played: {solo_matches['count']}\n"
        f"Squad Matches Played: {squad_matches['count']}\n"
        f"Total Users: {total_users['count']}\n"
        f"Total Players: {total_players['count']}\n"
        f"Tournament Status: {TOURNAMENT_MODE.capitalize()}\n"
    )
    update.message.reply_text(response)

# /broadcast Command
def broadcast(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        message = " ".join(context.args)
        if message:
            users = stats.find_one({"type": "users"}) or {"user_ids": []}
            for user_id in users.get("user_ids", []):
                try:
                    context.bot.send_message(chat_id=user_id, text=message)
                except Exception:
                    continue
            update.message.reply_text("Broadcast sent successfully.")
        else:
            update.message.reply_text("Please provide a message to broadcast.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# /pay Command
def pay(update: Update, context):
    image_link = "https://i.ibb.co/LvwtRf1/file-2407.jpg"  # Replace with your payment QR code image link
    caption = "Please send the payment screenshot to @Rizeol with your BGMI UID and In-Game Name."
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_link,
        caption=caption,
    )

# Approval Log Function
def log_registration_approval(team, context):
    team_name = team["team_name"]
    players = team["players"]
    msg = f"New Registration Pending:\nTeam Name: {team_name}\n"
    
    # Add each player’s information to the log message
    for player in players:
        msg += f"Player UID: {player['uid']}, In-Game Name: {player['name']}\n"
    
    # Create an approval button for the team
    approve_button = InlineKeyboardButton("Approve", callback_data=f"approve_{team_name}")
    keyboard = [[approve_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the log message to the log group with the approval button
    context.bot.send_message(
        chat_id=LOG_GROUP_ID, 
        text=msg, 
        reply_markup=reply_markup
    )

# Approve Registration Function
def approve_registration(update: Update, context):
    query = update.callback_query
    team_name = query.data.split("_")[1]
    
    # Find the team and approve it
    team = registrations.find_one({"team_name": team_name})
    if team:
        # Insert the team into the approved teams collection
        approved_teams.insert_one(team)
        # Remove the team from the unapproved registrations collection
        registrations.delete_one({"team_name": team_name})

        query.answer()
        
        # Send a new message confirming the approval to the original message
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Team {team_name} has been approved!"
        )
        
        # Log the approval to the log group with approval button
        log_registration_approval(team, context)
      

# Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("aBroadcast", a_broadcast))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("mode", mode))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("stats", stats_command))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(CommandHandler("query", query))
    
    dp.add_handler(CallbackQueryHandler(approve_registration, pattern="^approve_"))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
