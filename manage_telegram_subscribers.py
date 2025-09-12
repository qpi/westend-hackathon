#!/usr/bin/env python3
"""
Telegram Subscribers Management Script
=====================================

Script to manage Telegram bot subscribers for the WestEnd forecast bot.
"""

import sys
import os
from telegram_integration import telegram_notifier

def show_subscribers():
    """Show all current subscribers"""
    print(f"\n👥 Jelenlegi feliratkozók ({len(telegram_notifier.chat_ids)}):")
    if telegram_notifier.chat_ids:
        for i, chat_id in enumerate(telegram_notifier.chat_ids, 1):
            print(f"  {i}. {chat_id}")
    else:
        print("  Nincs feliratkozó.")

def add_subscriber():
    """Add a new subscriber"""
    chat_id = input("\n📝 Adja meg az új feliratkozó Chat ID-ját: ").strip()
    if chat_id:
        if telegram_notifier.add_subscriber(chat_id):
            print(f"✅ Feliratkozó hozzáadva: {chat_id}")
        else:
            print(f"⚠️ A feliratkozó már létezik: {chat_id}")
    else:
        print("❌ Érvénytelen Chat ID")

def remove_subscriber():
    """Remove a subscriber"""
    show_subscribers()
    if not telegram_notifier.chat_ids:
        return
    
    chat_id = input("\n📝 Adja meg a törlendő Chat ID-t: ").strip()
    if chat_id:
        if telegram_notifier.remove_subscriber(chat_id):
            print(f"✅ Feliratkozó törölve: {chat_id}")
        else:
            print(f"❌ Feliratkozó nem található: {chat_id}")
    else:
        print("❌ Érvénytelen Chat ID")

def test_broadcast():
    """Send a test broadcast message"""
    if not telegram_notifier.chat_ids:
        print("❌ Nincs feliratkozó a teszteléshez")
        return
    
    test_data = {
        'prediction': 12500,
        'date': '2025-09-12',
        'temperature': 22,
        'rainfall': 0.0,
        'marketing_spend': 400,
        'is_holiday': False,
        'is_school_break': False,
        'global_avg': 11042,
        'context_avg': 9218,
        'context_type': 'hétköznapi',
        'percentage_diff_global': 13.2,
        'percentage_diff_context': 35.6
    }
    
    print(f"\n📡 Teszt broadcast küldése {len(telegram_notifier.chat_ids)} feliratkozónak...")
    success, message = telegram_notifier.send_prediction_summary(test_data, None)
    
    if success:
        print(f"✅ Teszt broadcast sikeres!")
        print(f"📊 {message}")
    else:
        print(f"❌ Teszt broadcast sikertelen: {message}")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("📱 WestEnd Telegram Bot - Feliratkozó Kezelő")
        print("="*50)
        print("1. 👥 Feliratkozók megtekintése")
        print("2. ➕ Feliratkozó hozzáadása")
        print("3. ➖ Feliratkozó törlése")
        print("4. 📡 Teszt broadcast küldése")
        print("5. 🚪 Kilépés")
        print("-"*50)
        
        choice = input("Válasszon opciót (1-5): ").strip()
        
        if choice == '1':
            show_subscribers()
        elif choice == '2':
            add_subscriber()
        elif choice == '3':
            remove_subscriber()
        elif choice == '4':
            test_broadcast()
        elif choice == '5':
            print("👋 Viszlát!")
            break
        else:
            print("❌ Érvénytelen választás")

if __name__ == "__main__":
    main()
