#!/usr/bin/env python3
"""
Telegram Bot Diagnosztika és Teszt
"""

import requests
import json
from datetime import datetime

# Bot adatok
BOT_TOKEN = "8228985225:AAEiVjOqciFSnByLEy9gdofMvcylaqdszbc"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def test_bot_info():
    """Bot információk lekérése"""
    print("🤖 BOT INFORMÁCIÓK TESZTELÉSE")
    print("=" * 50)
    
    try:
        url = f"{BASE_URL}/getMe"
        response = requests.get(url, timeout=10)
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Bot név: {bot_info.get('first_name')}")
                print(f"✅ Bot username: @{bot_info.get('username')}")
                print(f"✅ Bot ID: {bot_info.get('id')}")
                print(f"✅ Bot aktív: {bot_info.get('is_bot')}")
                return True
            else:
                print(f"❌ API hiba: {data}")
                return False
        else:
            print(f"❌ HTTP hiba: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Kapcsolódási hiba: {e}")
        return False

def get_updates():
    """Legutóbbi üzenetek lekérése (chat ID-k megtalálásához)"""
    print("\n📨 LEGUTÓBBI ÜZENETEK LEKÉRÉSE")
    print("=" * 50)
    
    try:
        url = f"{BASE_URL}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                updates = data.get('result', [])
                print(f"📊 Talált üzenetek száma: {len(updates)}")
                
                chat_ids = set()
                for update in updates[-10:]:  # Utolsó 10 üzenet
                    if 'message' in update:
                        chat = update['message']['chat']
                        chat_id = chat['id']
                        chat_type = chat['type']
                        
                        if chat_type == 'private':
                            first_name = chat.get('first_name', 'Ismeretlen')
                            last_name = chat.get('last_name', '')
                            username = chat.get('username', 'nincs username')
                            print(f"👤 Privát chat: {first_name} {last_name} (@{username})")
                        else:
                            title = chat.get('title', 'Ismeretlen csoport')
                            print(f"👥 Csoport chat: {title}")
                        
                        print(f"   Chat ID: {chat_id}")
                        print(f"   Típus: {chat_type}")
                        chat_ids.add(chat_id)
                        print()
                
                if chat_ids:
                    print(f"🎯 Elérhető Chat ID-k: {list(chat_ids)}")
                    return list(chat_ids)
                else:
                    print("⚠️ Nincsenek elérhető chat ID-k.")
                    print("💡 Küldjön egy üzenetet a bot-nak Telegramban, majd futtassa újra!")
                    return []
            else:
                print(f"❌ API hiba: {data}")
                return []
        else:
            print(f"❌ HTTP hiba: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return []

def send_test_message(chat_id):
    """Teszt üzenet küldése"""
    print(f"\n📤 TESZT ÜZENET KÜLDÉSE: {chat_id}")
    print("=" * 50)
    
    message = f"""
🧪 <b>TESZT ÜZENET</b>

🤖 Bot: WestEnd Forecast Bot
📅 Idő: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 Státusz: Teszt üzenet

✅ Ha ezt az üzenetet látja, a bot működik!

🔗 Következő lépés: Használja a Streamlit alkalmazást előrejelzés generálásához.
"""
    
    try:
        url = f"{BASE_URL}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message.strip(),
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                message_info = data.get('result', {})
                print(f"✅ Üzenet sikeresen elküldve!")
                print(f"   Message ID: {message_info.get('message_id')}")
                print(f"   Chat ID: {message_info.get('chat', {}).get('id')}")
                return True
            else:
                print(f"❌ API hiba: {data}")
                return False
        else:
            print(f"❌ HTTP hiba: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return False

def send_prediction_test():
    """Előrejelzés formátumú teszt üzenet"""
    print(f"\n🎯 ELŐREJELZÉS TESZT ÜZENET")
    print("=" * 50)
    
    # Teszt adatok
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
    
    # Üzenet formázása
    date_str = test_data['date'].strftime('%Y-%m-%d (%A)')
    day_emoji = "🎯"
    weather_emoji = "☀️"
    trend_emoji = "📉"
    
    message = f"""
🏬 <b>WestEnd Látogatószám Előrejelzés</b>

📅 <b>Dátum:</b> {date_str} {day_emoji}
{weather_emoji} <b>Időjárás:</b> {test_data['temperature']}°C, {test_data['rainfall']}mm csapadék
💰 <b>Marketing:</b> {test_data['marketing_spend']:,.0f} EUR

{trend_emoji} <b>ELŐREJELZÉS: {test_data['prediction']:,.0f} fő</b>

📊 <b>Összehasonlítás:</b>
• {test_data['context_type'].capitalize()} átlagtól: <b>{test_data['percentage_diff_context']:+.1f}%</b>
• Globális átlagtól: <b>{test_data['percentage_diff_global']:+.1f}%</b>

📈 <b>Referencia értékek:</b>
• {test_data['context_type'].capitalize()} átlag: {test_data['context_avg']:,.0f} fő
• Globális átlag: {test_data['global_avg']:,.0f} fő

🎯 <b>Státusz:</b> 🟡 Átlag alatti forgalom

⏰ <i>Generálva: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>
"""
    
    return message.strip()

def main():
    """Fő teszt függvény"""
    print("🔍 TELEGRAM BOT TELJES DIAGNOSZTIKA")
    print("=" * 60)
    
    # 1. Bot info teszt
    if not test_bot_info():
        print("\n❌ Bot kapcsolat sikertelen! Ellenőrizze a token-t.")
        return
    
    # 2. Updates lekérése
    chat_ids = get_updates()
    
    if not chat_ids:
        print("\n💡 TEENDŐK:")
        print("1. Nyissa meg Telegramot")
        print("2. Keresse meg: @westend_forecast_bot")
        print("3. Küldjön egy üzenetet: /start")
        print("4. Futtassa újra ezt a scriptet")
        return
    
    # 3. Teszt üzenetek küldése
    for chat_id in chat_ids:
        print(f"\n🎯 TESZT CHAT ID: {chat_id}")
        
        # Egyszerű teszt üzenet
        if send_test_message(chat_id):
            print("✅ Egyszerű üzenet OK")
        else:
            print("❌ Egyszerű üzenet sikertelen")
            continue
        
        # Előrejelzés formátumú üzenet
        prediction_message = send_prediction_test()
        
        try:
            url = f"{BASE_URL}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': prediction_message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Előrejelzés formátumú üzenet OK")
            else:
                print(f"❌ Előrejelzés üzenet sikertelen: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Előrejelzés üzenet hiba: {e}")
    
    print(f"\n🎉 DIAGNOSZTIKA BEFEJEZVE!")
    print("Ha minden teszt sikeres volt, a Streamlit alkalmazásban is működnie kell.")

if __name__ == "__main__":
    main()
