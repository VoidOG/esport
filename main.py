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
    global TOURNAMENT_MODE
    user = update.message.from_user
    chat_id = update.message.chat_id
    message = update.message.text

    if TOURNAMENT_MODE == "off":
        keyboard = [[InlineKeyboardButton("Updates", url="https://t.me/updates_channel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Tournament registration is currently closed.", reply_markup=reply_markup
        )
    else:
        # Prompt user for team details
        update.message.reply_text(
            "Please provide your team credentials in the following format:\n"
            "Team name\n"
            "Player's UID with in-game name (e.g. 1234567890 Horizon)"
        )
        
        # Save the registration status temporarily for later use
        context.user_data['registration_status'] = 'awaiting_credential_details'

def handle_team_details(update: Update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    message = update.message.text

    # Check if the user is providing the team details
    if 'registration_status' in context.user_data and context.user_data['registration_status'] == 'awaiting_credential_details':
        # Split the message into team name and players' UID with username
        details = message.split("\n")
        if len(details) < 2:
            update.message.reply_text("Please provide both the team name and player details in the correct format.")
            return

        team_name = details[0].strip()
        player_details = details[1].strip()

        # Send confirmation to the user
        update.message.reply_text(
            "Registration successful!\nNow /pay and send the payment screenshot to @Rizeol."
        )

        # Send details to the log group
        mode_text = f"Tournament Mode: {TOURNAMENT_MODE.capitalize()}"
        log_text = (
            f"**New Tournament Registration**\n"
            f"User: [{user.full_name}](tg://user?id={user.id})\n"
            f"User ID: `{user.id}`\n"
            f"Team: {team_name}\n"
            f"Player Details: {player_details}\n"
            f"{mode_text}\n"
        )
        
        # Add an approval button
        approve_button = InlineKeyboardButton(
            "Approve", callback_data=f"approve_{user.id}"
        )
        reply_markup = InlineKeyboardMarkup([[approve_button]])

        # Send to log group and store the log message ID
        log_message = context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=log_text,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

        # Save registration data to MongoDB
        team_data = {
            "user_id": user.id,
            "team_name": team_name,
            "player_details": player_details,
            "mode": TOURNAMENT_MODE,
            "approved": False,
            "log_message_id": log_message.message_id,  # Store log message ID
        }

        registrations.insert_one(team_data)

        # Clear the registration status
        context.user_data['registration_status'] = None

# /check Command
def check(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        approved = approved_teams.find()
        if approved_teams.count_documents({}) > 0:
            response = "Currently Registered Teams:\n\n"
            for team in approved:
                # Use .get() to avoid KeyError
                team_name = team.get('team_name', 'Unknown')
                response += f"Team Name: {team_name}\nPlayers:\n"
                
                players = team.get('players', [])
                for player in players:
                    response += f"- {player.get('uid', 'Unknown')} ({player.get('name', 'Unknown')})\n"
                
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
    team_name = team.get("team_name", "N/A")  # Use .get() to avoid KeyError
    players = team.get("players", [])
    msg = f"New Registration Pending:\nTeam Name: {team_name}\n"
    
    # Add each player’s information to the log message
    for player in players:
        msg += f"Player UID: {player.get('uid', 'N/A')}, In-Game Name: {player.get('name', 'N/A')}\n"
    
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
    user_id = query.data.split("_")[1]
    
    # Find the registration in MongoDB
    registration = registrations.find_one({"user_id": int(user_id)})
    if registration:
        # Mark as approved
        approved_teams.insert_one(registration)
        registrations.delete_one({"user_id": int(user_id)})

        # Notify in the log group by replying to the original message
        context.bot.send_message(
            chat_id=LOG_GROUP_ID,
            text=f"✅ Registration approved for User ID: {user_id}",
            reply_to_message_id=registration["log_message_id"]  # Reply to the original registration log message
        )

        # Notify the user about approval
        try:
            context.bot.send_message(
                chat_id=int(user_id),
                text="🎉 Your registration has been approved! Get ready to participate."
            )
        except Exception as e:
            logger.error(f"Failed to send approval message to {user_id}: {e}")
    else:
        query.edit_message_text("❌ Registration not found or already approved.") 


#clear command to wipe data from /check
def clear(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        try:
            # Clear all approved teams from the database
            approved_teams.delete_many({})  # Delete all entries in the collection

            # Send confirmation to the owner
            update.message.reply_text("✅ All approved teams have been cleared.")
            
            # Optionally, notify the log group that data has been cleared
            context.bot.send_message(
                chat_id=LOG_GROUP_ID,
                text="⚠️ All approved teams data has been wiped out by the owner."
            )
        except Exception as e:
            update.message.reply_text(f"❌ Error occurred while clearing data: {str(e)}")
            logger.error(f"Error clearing approved teams data: {e}")
    else:
        update.message.reply_text("❌ You are not authorized to use this command.")
      

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
