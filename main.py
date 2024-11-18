from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
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
        [InlineKeyboardButton("𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/EsportsHorizon")],
        [InlineKeyboardButton("𝖰𝗎𝖾𝗋𝗒", url="https://t.me/Rizeol")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    image_url = "https://i.ibb.co/tXQVxKn/file-2417.jpg"  # Replace with your image link
    caption = (
        "𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗤𝘂𝗶𝗰𝗸𝗥𝗲𝗴𝗯𝗼𝘁 – 𝗬𝗼𝘂𝗿 𝗨𝗹𝘁𝗶𝗺𝗮𝘁𝗲 𝗧𝗼𝘂𝗿𝗻𝗮𝗺𝗲𝗻𝘁 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁!\n\n"
        "𝖧𝖾𝗅𝗅𝗈,𝖯𝗅𝖺𝗒𝖾𝗋! 𝖱𝖾𝖺𝖽𝗒 𝗍𝗈 𝖾𝗇𝗍𝖾𝗋 𝗍𝗁𝖾 𝖻𝖺𝗍𝗍𝗅𝖾𝖿𝗂𝖾𝗅𝖽?\n"
        "≡ 𝖧𝖾𝗋𝖾'𝗌 𝗁𝗈𝗐 𝖨 𝖼𝖺𝗇 𝖺𝗌𝗌𝗂𝗌𝗍 𝗒𝗈𝗎:\n"
        "/Register– 𝖱𝖾𝗀𝗂𝗌𝗍𝖾𝗋 𝗒𝗈𝗎𝗋 𝗍𝖾𝖺𝗆 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗎𝗉𝖼𝗈𝗆𝗂𝗇𝗀 𝗍𝗈𝗎𝗋𝗇𝖺𝗆𝖾𝗇𝗍\n"
        "/Query – 𝖧𝖺𝗏𝖾 𝗊𝗎𝖾𝗌𝗍𝗂𝗈𝗇𝗌? 𝖣𝗋𝗈𝗉 𝗍𝗁𝖾𝗆 𝗁𝖾𝗋𝖾, 𝖺𝗇𝖽 𝗐𝖾’𝗅𝗅 𝖺𝗌𝗌𝗂𝗌𝗍 𝗒𝗈𝗎!\n"
        "/Pay – 𝖦𝖾𝗍 𝗒𝗈𝗎𝗋 𝖰𝖱 𝖼𝗈𝖽𝖾 𝖿𝗈𝗋 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝖺𝗇𝖽 𝗌𝖾𝗇𝖽 𝗍𝗁𝖾 𝗌𝖼𝗋𝖾𝖾𝗇𝗌𝗁𝗈𝗍 𝗍𝗈 𝖼𝗈𝗇𝖿𝗂𝗋𝗆 𝗒𝗈𝗎𝗋 𝗋𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇.\n\n"
        "✥𝖲𝗍𝖺𝗒 𝗍𝗎𝗇𝖾𝖽 𝖿𝗈𝗋 𝗂𝗆𝗉𝗈𝗋𝗍𝖺𝗇𝗍 𝗎𝗉𝖽𝖺𝗍𝖾𝗌:\n⩉𝖸𝗈𝗎’𝗅𝗅 𝗋𝖾𝖼𝖾𝗂𝗏𝖾 𝖺 𝗋𝖾𝗆𝗂𝗇𝖽𝖾𝗋 1 𝖽𝖺𝗒 𝖻𝖾𝖿𝗈𝗋𝖾 𝗍𝗁𝖾 𝗍𝗈𝗎𝗋𝗇𝖺𝗆𝖾𝗇𝗍 𝖻𝖾𝗀𝗂𝗇𝗌.\n⩉𝖳𝗁𝖾 𝗋𝗈𝗈𝗆 𝖼𝗋𝖾𝖽𝖾𝗇𝗍𝗂𝖺𝗅𝗌 𝗐𝗂𝗅𝗅 𝖻𝖾 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗒𝗈𝗎 15 𝗆𝗂𝗇𝗎𝗍𝖾𝗌 𝖻𝖾𝖿𝗈𝗋𝖾 𝗍𝗁𝖾 𝗆𝖺𝗍𝖼𝗁 𝗌𝗍𝖺𝗋𝗍𝗌."
    )
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=caption,
        reply_markup=reply_markup,
    )

# /query Command - Directs users to @Rizeol
def query(update: Update, context):
    update.message.reply_text("𝖥𝗈𝗋 𝖺𝗇𝗒 𝗊𝗎𝖾𝗋𝗂𝖾𝗌 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 @Rizeol")

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
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")

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
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")

# /reset Command
def reset(update: Update, context):
    if update.message.from_user.id == OWNER_ID:
        registered_ids.delete_many({})
        update.message.reply_text("All IDs have been reset.")
    else:
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")

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
        update.message.reply_text("𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗎𝗍𝗁𝗈𝗋𝗂𝗓𝖾𝖽 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")

# /register Command
def register(update: Update, context):
    global TOURNAMENT_MODE
    user = update.message.from_user
    chat_id = update.message.chat_id
    message = update.message.text

    if TOURNAMENT_MODE == "off":
        keyboard = [[InlineKeyboardButton("𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/EsportsHorizon")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "𝖭𝗈 𝖲𝖼𝗁𝖾𝖽𝗎𝗅𝖾𝖽 𝖳𝗈𝗎𝗋𝗇𝖺𝗆𝖾𝗇𝗍𝗌 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖿𝗈𝗋 𝖱𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇.\n𝖶𝖺𝗍𝖼𝗁 𝗈𝗎𝗍 𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝗍𝗈 𝗀𝖾𝗍 𝗎𝗉𝖽𝖺𝗍𝖾𝖽 𝗐𝗁𝖾𝗇𝖾𝗏𝖾𝗋 𝖺 𝗌𝖼𝗁𝖾𝖽𝗎𝗅𝖾𝖽 𝖽𝗋𝗈𝗉𝗌.", reply_markup=reply_markup
        )
    else:
        # Prompt user for team details
        update.message.reply_text(
            "𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗒𝗈𝗎𝗋 𝗍𝖾𝖺𝗆 𝖼𝗋𝖾𝖽𝖾𝗇𝗍𝗂𝖺𝗅𝗌 𝗂𝗇 𝗍𝗁𝖾 𝖿𝗈𝗅𝗅𝗈𝗐𝗂𝗇𝗀 𝖿𝗈𝗋𝗆𝖺𝗍:\n"
            "𝖸𝗈𝗎𝗋 𝖳𝖾𝖺𝗆 𝖭𝖺𝗆𝖾\n"
            "𝖸𝗈𝗎𝗋 𝖴𝖨𝖣 𝗐𝗂𝗍𝗁 𝗒𝗈𝗎𝗋 𝖨𝗇-𝗀𝖺𝗆𝖾 𝖭𝖺𝗆𝖾/n(𝖨𝖿 𝖲𝗊𝗎𝖺𝖽 𝖳𝗈𝗎𝗋𝗇𝖺𝗆𝖾𝗇𝗍  𝖠𝖽𝖽 𝗈𝗍𝗁𝖾𝗋 𝗉𝗅𝖺𝗒𝖾𝗋𝗌 𝖴𝖨𝖣 𝖺𝗇𝖽 𝖨𝗇-𝗀𝖺𝗆𝖾 𝖭𝖺𝗆𝖾 𝗂𝗇 𝗍𝗁𝖾 𝗌𝖺𝗆𝖾 𝗅𝗂𝗇𝖾 𝗇𝗈𝗍 𝗂𝗇 𝖺𝗇𝗈𝗍𝗁𝖾𝗋 𝗅𝗂𝗇𝖾)\n"
            "𝖤𝗑𝖺𝗆𝗉𝗅𝖾\n\n"
            "𝖳𝖾𝖺𝗆 𝖧𝗈𝗋𝗂𝗓𝗈𝗇\n"
            "123456789 𝖧𝗈𝗋𝗂𝗓𝗈𝗇, 987654321 𝖤𝗌𝗉𝗈𝗋𝗍𝗌 ...."
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
            update.message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖻𝗈𝗍𝗁 𝗍𝗁𝖾 𝗍𝖾𝖺𝗆 𝗇𝖺𝗆𝖾 𝖺𝗇𝖽 𝗉𝗅𝖺𝗒𝖾𝗋 𝖽𝖾𝗍𝖺𝗂𝗅𝗌 𝗂𝗇 𝗍𝗁𝖾 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝖿𝗈𝗋𝗆𝖺𝗍.")
            return

        team_name = details[0].strip()
        player_details = details[1].strip()

        # Send confirmation to the user
        update.message.reply_text(
            "𝖱𝖾𝗀𝗂𝗌𝗍𝖾𝗋𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!\n𝖭𝗈𝗐 /pay 𝖺𝗇𝖽 𝗌𝖾𝗇𝖽 𝗍𝗁𝖾 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝗌𝖼𝗋𝖾𝖾𝗇𝗌𝗁𝗈𝗍 𝗐𝗂𝗍𝗁 𝗒𝗈𝗎𝗋 𝗉𝗅𝖺𝗒𝖾𝗋𝗌 𝖼𝗋𝖾𝖽𝖾𝗇𝗍𝗂𝖺𝗅𝗌 𝗍𝗈 @Rizeol 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝗋𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖾𝖽."
        )

        # Send details to the log group
        mode_text = f"𝗧𝗼𝘂𝗿𝗻𝗮𝗺𝗲𝗻𝘁 𝗠𝗼𝗱𝗲: {TOURNAMENT_MODE.capitalize()}"
        log_text = (
            f"𝗡𝗲𝘄 𝗧𝗼𝘂𝗿𝗻𝗮𝗺𝗲𝗻𝘁 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻\n"
            f"𝗨𝘀𝗲𝗿: [{user.full_name}](tg://user?id={user.id})\n"
            f"𝗨𝘀𝗲𝗿 𝗜𝗗: `{user.id}`\n"
            f"𝗧𝗲𝗮𝗺: `{team_name}`\n"
            f"𝗣𝗹𝗮𝘆𝗲𝗿 𝗗𝗲𝘁𝗮𝗶𝗹𝘀: `{player_details}`\n"
            f"{mode_text}\n"
        )
        
        # Add an approval button
        approve_button = InlineKeyboardButton(
            "𝖠𝗉𝗉𝗋𝗈𝗏𝖾", callback_data=f"approve_{user.id}"
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
                response += f"𝗧𝗲𝗮𝗺 𝗡𝗮𝗺𝗲: {team_name}\n𝗨𝘀𝗲𝗿:\n"
                
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
    image_link = "https://i.ibb.co/XtBnPVq/file-2430.jpg"  # Replace with your payment QR code image link
    caption = "𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝗍𝗁𝖾 𝗉𝖺𝗒𝗆𝖾𝗇𝗍 𝗌𝖼𝗋𝖾𝖾𝗇𝗌𝗁𝗈𝗍 𝗍𝗈 @Rizeol 𝗐𝗂𝗍𝗁 𝗒𝗈𝗎𝗋 𝖡𝖦𝖬𝖨 𝖴𝖨𝖣 𝖺𝗇𝖽 𝖨𝗇-𝖦𝖺𝗆𝖾 𝖭𝖺𝗆𝖾 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝗋𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖾𝖽."
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_link,
        caption=caption,
    )

# Approval Log Function
def log_registration_approval(team, context):
    team_name = team.get("team_name", "N/A")  # Use .get() to avoid KeyError
    players = team.get("players", [])
    msg = f"𝗡𝗲𝘄 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗣𝗲𝗻𝗱𝗶𝗻𝗴:\n𝗧𝗲𝗮𝗺 𝗡𝗮𝗺𝗲: {team_name}\n"
    
    # Add each player’s information to the log message
    for player in players:
        msg += f"Player UID: {player.get('uid', 'N/A')}, In-Game Name: {player.get('name', 'N/A')}\n"
    
    # Create an approval button for the team
    approve_button = InlineKeyboardButton("𝖠𝗉𝗉𝗋𝗈𝗏𝖾", callback_data=f"approve_{team_name}")
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
            text=f"𝖱𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖾𝖽 𝖿𝗈𝗋 𝖴𝗌𝖾𝗋 𝖨𝖣: {user_id}",
            reply_to_message_id=registration["log_message_id"]  # Reply to the original registration log message
        )

        # Notify the user about approval
        try:
            context.bot.send_message(
                chat_id=int(user_id),
                text="𝖸𝗈𝗎𝗋 𝗋𝖾𝗀𝗂𝗌𝗍𝗋𝖺𝗍𝗂𝗈𝗇 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖺𝗉𝗉𝗋𝗈𝗏𝖾𝖽! 𝖸𝗈𝗎'𝗅𝗅 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝗋𝗈𝗈𝗆 𝖼𝗋𝖾𝖽𝖾𝗇𝗍𝗂𝖺𝗅𝗌 𝖻𝖾𝖿𝗈𝗋𝖾 15 𝗆𝗂𝗇𝗎𝗍𝖾𝗌 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝗆𝖺𝗍𝖼𝗁 𝗍𝗂𝗆𝖾 𝖺𝗇𝖽 𝖺 𝗇𝗈𝗍𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝗈𝗇𝖾 𝖽𝖺𝗒 𝖻𝖾𝖿𝗈𝗋𝖾 𝖻𝗒 𝗆𝖾."
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
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(CommandHandler("query", query))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_team_details))
    dp.add_handler(CallbackQueryHandler(approve_registration, pattern="^approve_"))
    dp.add_handler(CommandHandler("clear", clear))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
