#!/usr/bin/env python3
"""
Test Broadcast Functionality
============================

Test sending broadcast messages to all subscribers.
"""

from telegram_integration import send_prediction_to_telegram
from datetime import datetime

def test_broadcast():
    """Test broadcast to all subscribers"""
    print("🧪 BROADCAST TESZT")
    print("="*50)
    
    # Test data
    prediction_data = {
        'prediction': 15200,
        'date': datetime(2025, 9, 12),
        'temperature': 23,
        'rainfall': 0.0,
        'marketing_spend': 600,
        'is_holiday': False,
        'is_school_break': False,
        'global_avg': 11042,
        'context_avg': 9218,
        'context_type': 'hétköznapi',
        'percentage_diff_global': 37.6,
        'percentage_diff_context': 64.9
    }
    
    print("📡 Broadcast küldése MINDEN feliratkozónak...")
    print("📊 Előrejelzés: 15,200 fő")
    print("📅 Dátum: 2025-09-12")
    print()
    
    # Send broadcast (no chat_id = broadcast to all)
    success, message = send_prediction_to_telegram(prediction_data, None)
    
    if success:
        print("✅ BROADCAST SIKERES!")
        print(f"📊 {message}")
    else:
        print("❌ BROADCAST SIKERTELEN!")
        print(f"🔍 Hiba: {message}")

if __name__ == "__main__":
    test_broadcast()
