"""
Telegram Bot Integration for WestEnd Forecast
============================================

Telegram bot integration for sending prediction results.
"""

import requests
import logging
from datetime import datetime
import streamlit as st
import json

# Telegram Bot Configuration
BOT_TOKEN = "8228985225:AAEiVjOqciFSnByLEy9gdofMvcylaqdszbc"
BOT_USERNAME = "westend_forecast_bot"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Telegram bot notification handler using HTTP requests"""

    def __init__(self, token: str = BOT_TOKEN):
        """Initialize the Telegram bot"""
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_ids = set()  # Store chat IDs of users who interacted with the bot
        self.subscribers_file = "telegram_subscribers.txt"  # File to store subscribers
        self.load_subscribers()  # Load existing subscribers

    def load_subscribers(self):
        """Load subscribers from file"""
        try:
            if os.path.exists(self.subscribers_file):
                with open(self.subscribers_file, 'r') as f:
                    for line in f:
                        chat_id = line.strip()
                        if chat_id:
                            self.chat_ids.add(chat_id)
                logger.info(f"Loaded {len(self.chat_ids)} subscribers from file")
            else:
                # Add default subscriber (Mihály)
                self.chat_ids.add("8121891526")
                self.save_subscribers()
                logger.info("Created new subscribers file with default subscriber")
        except Exception as e:
            logger.error(f"Error loading subscribers: {e}")
            # Add default subscriber as fallback
            self.chat_ids.add("8121891526")

    def save_subscribers(self):
        """Save subscribers to file"""
        try:
            with open(self.subscribers_file, 'w') as f:
                for chat_id in self.chat_ids:
                    f.write(f"{chat_id}\n")
            logger.info(f"Saved {len(self.chat_ids)} subscribers to file")
        except Exception as e:
            logger.error(f"Error saving subscribers: {e}")

    def add_subscriber(self, chat_id: str):
        """Add a new subscriber"""
        if chat_id not in self.chat_ids:
            self.chat_ids.add(chat_id)
            self.save_subscribers()
            logger.info(f"Added new subscriber: {chat_id}")
            return True
        return False

    def remove_subscriber(self, chat_id: str):
        """Remove a subscriber"""
        if chat_id in self.chat_ids:
            self.chat_ids.remove(chat_id)
            self.save_subscribers()
            logger.info(f"Removed subscriber: {chat_id}")
            return True
        return False

    def send_prediction_summary(self, prediction_data: dict, chat_id: str = None):
        """
        Send prediction summary to Telegram using HTTP requests

        Args:
            prediction_data: Dictionary containing prediction results
            chat_id: Specific chat ID to send to (optional, if None sends to all subscribers)

        Returns:
            tuple: (success: bool, error_message: str)
        """
        try:
            message = self._format_prediction_message(prediction_data)

            if chat_id:
                # Send to specific chat only
                success, error_msg = self._send_message(chat_id, message)
                if success:
                    logger.info(f"Prediction sent to specific chat {chat_id}")
                    return True, "Success"
                else:
                    logger.error(f"Failed to send to specific chat {chat_id}: {error_msg}")
                    return False, error_msg
            else:
                # Send to ALL subscribers (broadcast)
                if not self.chat_ids:
                    logger.warning("No subscribers found, adding default subscriber")
                    self.chat_ids.add("8121891526")
                    self.save_subscribers()

                successful_sends = 0
                failed_sends = 0
                error_messages = []

                logger.info(f"Broadcasting to {len(self.chat_ids)} subscribers")

                for subscriber_chat_id in self.chat_ids:
                    success, error_msg = self._send_message(subscriber_chat_id, message)
                    if success:
                        successful_sends += 1
                        logger.info(f"✅ Sent to subscriber: {subscriber_chat_id}")
                    else:
                        failed_sends += 1
                        error_messages.append(f"❌ Failed to send to {subscriber_chat_id}: {error_msg}")
                        logger.error(f"Failed to send to subscriber {subscriber_chat_id}: {error_msg}")

                # Return overall result
                if successful_sends > 0:
                    result_msg = f"Broadcast completed: {successful_sends} successful, {failed_sends} failed"
                    logger.info(result_msg)
                    if failed_sends > 0:
                        result_msg += f". Errors: {'; '.join(error_messages[:3])}"  # Show first 3 errors
                    return True, result_msg
                else:
                    error_msg = f"All broadcasts failed. Errors: {'; '.join(error_messages)}"
                    logger.error(error_msg)
                    return False, error_msg

        except Exception as e:
            error_msg = f"Error sending Telegram message: {e}"
            logger.error(error_msg)
            return False, error_msg

    def _send_message(self, chat_id: str, message: str) -> tuple[bool, str]:
        """Send a message using HTTP request"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }

            logger.info(f"Sending message to chat_id: {chat_id}")
            logger.info(f"URL: {url}")
            logger.info(f"Message length: {len(message)} characters")

            response = requests.post(url, json=payload, timeout=30)

            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    logger.info(f"Message sent successfully: {data}")
                    return True, "Success"
                else:
                    error_msg = f"API returned ok=false: {data}"
                    logger.error(error_msg)
                    return False, error_msg
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Telegram API error: {error_msg}")
                return False, error_msg

        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout error: {e}"
            logger.error(error_msg)
            return False, error_msg
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {e}"
            logger.error(error_msg)
            return False, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"HTTP request error: {e}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def _format_prediction_message(self, data: dict) -> str:
        """Format prediction data into a nice Telegram message"""
        
        # Extract data
        prediction = data.get('prediction', 0)
        date = data.get('date', datetime.now())
        temperature = data.get('temperature', 0)
        rainfall = data.get('rainfall', 0)
        marketing = data.get('marketing_spend', 0)
        is_holiday = data.get('is_holiday', False)
        is_school_break = data.get('is_school_break', False)
        
        # Context data
        global_avg = data.get('global_avg', 0)
        context_avg = data.get('context_avg', 0)
        context_type = data.get('context_type', 'hétköznapi')
        percentage_diff_global = data.get('percentage_diff_global', 0)
        percentage_diff_context = data.get('percentage_diff_context', 0)
        
        # Format date
        date_str = date.strftime('%Y-%m-%d (%A)') if isinstance(date, datetime) else str(date)
        
        # Determine day type emoji
        day_emoji = "🎉" if is_holiday else ("📚" if is_school_break else ("🎯" if date.weekday() >= 5 else "💼"))
        
        # Weather emoji
        weather_emoji = "🌧️" if rainfall > 5 else ("☀️" if temperature > 25 else ("❄️" if temperature < 5 else "🌤️"))
        
        # Trend emoji
        trend_emoji = "📈" if percentage_diff_context > 10 else ("📉" if percentage_diff_context < -10 else "➡️")
        
        message = f"""
🏬 <b>WestEnd Látogatószám Előrejelzés</b>

📅 <b>Dátum:</b> {date_str} {day_emoji}
{weather_emoji} <b>Időjárás:</b> {temperature}°C, {rainfall}mm csapadék
💰 <b>Marketing:</b> {marketing:,.0f} EUR

{trend_emoji} <b>ELŐREJELZÉS: {prediction:,.0f} fő</b>

📊 <b>Összehasonlítás:</b>
• {context_type.capitalize()} átlagtól: <b>{percentage_diff_context:+.1f}%</b>
• Globális átlagtól: <b>{percentage_diff_global:+.1f}%</b>

📈 <b>Referencia értékek:</b>
• {context_type.capitalize()} átlag: {context_avg:,.0f} fő
• Globális átlag: {global_avg:,.0f} fő

🎯 <b>Státusz:</b> {"🟢 Átlag feletti forgalom" if percentage_diff_context > 10 else ("🟡 Átlag alatti forgalom" if percentage_diff_context < -10 else "🔵 Átlagos forgalom")}

⏰ <i>Generálva: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
        
        return message.strip()
    
    def add_chat_id(self, chat_id: str):
        """Add a chat ID to the notification list"""
        self.chat_ids.add(chat_id)
        logger.info(f"Added chat ID: {chat_id}")
    
    def remove_chat_id(self, chat_id: str):
        """Remove a chat ID from the notification list"""
        self.chat_ids.discard(chat_id)
        logger.info(f"Removed chat ID: {chat_id}")
    
    def test_connection(self) -> bool:
        """Test if the bot token is valid using HTTP request"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    username = bot_info.get('username', 'Unknown')
                    logger.info(f"Bot connected successfully: {username}")
                    return True
                else:
                    logger.error(f"Bot API error: {data}")
                    return False
            else:
                logger.error(f"HTTP error: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            return False
        except Exception as e:
            logger.error(f"Bot connection failed: {e}")
            return False

# Global instance
telegram_notifier = TelegramNotifier()

def send_prediction_to_telegram(prediction_data: dict, chat_id: str = None):
    """
    Send predictions to Telegram

    Args:
        prediction_data: Dictionary containing prediction results
        chat_id: Optional specific chat ID to send to

    Returns:
        tuple: (success: bool, error_message: str)
    """
    try:
        return telegram_notifier.send_prediction_summary(prediction_data, chat_id)
    except Exception as e:
        error_msg = f"Error in send_prediction_to_telegram: {e}"
        logger.error(error_msg)
        return False, error_msg

def test_telegram_connection() -> bool:
    """Test Telegram bot connection"""
    try:
        return telegram_notifier.test_connection()
    except Exception as e:
        logger.error(f"Error testing Telegram connection: {e}")
        return False

# Streamlit integration functions
def add_telegram_settings_to_sidebar():
    """Add Telegram settings to Streamlit sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Telegram Értesítések")

    # Show subscriber count
    subscriber_count = len(telegram_notifier.chat_ids)
    st.sidebar.info(f"👥 Feliratkozók száma: **{subscriber_count}**")
    
    # Test connection button
    if st.sidebar.button("🔗 Bot Kapcsolat Tesztelése"):
        with st.sidebar:
            with st.spinner("Telegram bot tesztelése..."):
                if test_telegram_connection():
                    st.success("✅ Bot kapcsolat OK!")
                else:
                    st.error("❌ Bot kapcsolat sikertelen!")
    
    # Chat ID input
    chat_id = st.sidebar.text_input(
        "💬 Chat ID",
        value="8121891526",  # Alapértelmezett Chat ID
        help="Adja meg a Telegram chat ID-t az értesítések fogadásához. Alapértelmezett: 8121891526 (Mihály Kuprivecz)"
    )
    
    # Enable/disable notifications
    enable_notifications = st.sidebar.checkbox(
        "📨 Telegram értesítések engedélyezése",
        value=True,
        help="Ha be van kapcsolva, minden előrejelzés után Telegram üzenetet küld."
    )
    
    return chat_id, enable_notifications

if __name__ == "__main__":
    # Test the integration
    test_data = {
        'prediction': 12500,
        'date': datetime(2024, 6, 15),
        'temperature': 25,
        'rainfall': 0,
        'marketing_spend': 500,
        'is_holiday': False,
        'is_school_break': False,
        'global_avg': 11119,
        'context_avg': 12800,
        'context_type': 'hétvégi',
        'percentage_diff_global': 12.4,
        'percentage_diff_context': -2.3
    }
    
    print("Testing Telegram integration...")
    if test_telegram_connection():
        print("✅ Bot connection successful!")
        # Uncomment to test sending a message
        # send_prediction_to_telegram(test_data)
    else:
        print("❌ Bot connection failed!")
