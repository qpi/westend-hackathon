#!/usr/bin/env python3
"""
Manual Subscriber Addition Script
=================================

Quick script to manually add the second subscriber.
"""

from telegram_integration import telegram_notifier

def main():
    print("📱 WestEnd Telegram Bot - Manual Subscriber Addition")
    print("="*50)
    
    # Show current subscribers
    print(f"👥 Jelenlegi feliratkozók ({len(telegram_notifier.chat_ids)}):")
    for i, chat_id in enumerate(telegram_notifier.chat_ids, 1):
        print(f"  {i}. {chat_id}")
    
    # Add the second subscriber (assuming it's a colleague)
    print("\n➕ Második feliratkozó hozzáadása...")
    
    # You can replace this with the actual Chat ID of the second person
    second_subscriber = input("Adja meg a második feliratkozó Chat ID-ját: ").strip()
    
    if second_subscriber:
        if telegram_notifier.add_subscriber(second_subscriber):
            print(f"✅ Feliratkozó hozzáadva: {second_subscriber}")
        else:
            print(f"⚠️ A feliratkozó már létezik: {second_subscriber}")
        
        # Show updated list
        print(f"\n👥 Frissített feliratkozók ({len(telegram_notifier.chat_ids)}):")
        for i, chat_id in enumerate(telegram_notifier.chat_ids, 1):
            print(f"  {i}. {chat_id}")
    else:
        print("❌ Érvénytelen Chat ID")

if __name__ == "__main__":
    main()
