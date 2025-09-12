#!/usr/bin/env python3
"""
Test Streamlit Telegram Integration
"""

from datetime import datetime
from telegram_integration import send_prediction_to_telegram

def test_streamlit_integration():
    """Test the exact same function that Streamlit uses"""
    
    print("🧪 STREAMLIT TELEGRAM INTEGRÁCIÓ TESZT")
    print("=" * 50)
    
    # Ugyanazok az adatok, mint amit a Streamlit küld
    prediction_data = {
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
    
    chat_id = "8121891526"
    
    print(f"📤 Üzenet küldése Chat ID-ra: {chat_id}")
    print(f"📊 Előrejelzés: {prediction_data['prediction']:,.0f} fő")
    print(f"📅 Dátum: {prediction_data['date']}")
    print()
    
    try:
        success, error_msg = send_prediction_to_telegram(prediction_data, chat_id)
        
        if success:
            print("✅ SIKERES! Telegram üzenet elküldve!")
            print("🎉 Ellenőrizze a Telegram alkalmazást!")
        else:
            print("❌ SIKERTELEN!")
            print(f"🔍 Hiba: {error_msg}")
            
            print("\n💡 Lehetséges okok:")
            print("• Internetkapcsolat probléma")
            print("• Telegram API nem elérhető")
            print("• Chat ID hibás")
            print("• Bot nincs elindítva")
            
    except Exception as e:
        print(f"❌ KIVÉTEL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_streamlit_integration()
