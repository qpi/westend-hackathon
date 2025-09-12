# 📱 WestEnd Telegram Bot Integráció

## 🤖 Bot Információk

- **Bot neve**: WestEnd látogatószám előrejelző bot
- **Username**: @westend_forecast_bot
- **Bot ID**: westend_forecast_bot

## 🚀 Új Funkció: Broadcast Üzenetek
A bot most **minden feliratkozónak** küldi az előrejelzéseket, nem csak egy konkrét Chat ID-ra!

### 👥 Feliratkozás
1. Keresse meg a `@westend_forecast_bot` bot-ot Telegramban
2. Küldje el a `/start` parancsot
3. Automatikusan feliratkozik az értesítésekre

### 📢 Broadcast Működés
- Ha **nincs Chat ID megadva** → Minden feliratkozó megkapja
- Ha **van Chat ID megadva** → Csak az adott személy kapja meg

## 🚀 Használat

### 1. Bot Elindítása Telegramban

1. Nyissa meg a Telegram alkalmazást
2. Keresse meg a `@westend_forecast_bot` bot-ot
3. Kattintson a **"Start"** gombra vagy írja be: `/start`

### 2. Chat ID Megszerzése

A Chat ID-t több módon megszerezheti:

#### Módszer 1: Bot üzenet
1. Írjon bármilyen üzenetet a bot-nak
2. A bot válaszában megkapja a Chat ID-t

#### Módszer 2: Telegram API
1. Írjon üzenetet a bot-nak
2. Nyissa meg böngészőben: `https://api.telegram.org/bot8228985225:AAEiVjOqciFSnByLEy9gdofMvcylaqdszbc/getUpdates`
3. Keresse meg a `"chat":{"id":` részt

#### Módszer 3: Harmadik fél szolgáltatás
1. Keresse meg a `@userinfobot` bot-ot Telegramban
2. Küldje el neki a `/start` parancsot
3. Megkapja a saját Chat ID-jét

### 3. Streamlit Alkalmazásban Beállítás

1. **Navigáció**: Nyissa meg a Streamlit alkalmazást
2. **Sidebar**: A bal oldali menüben találja a "📱 Telegram Értesítések" részt
3. **Bot Teszt**: Kattintson a "🔗 Bot Kapcsolat Tesztelése" gombra
4. **Chat ID**: Adja meg a Chat ID-t (opcionális)
5. **Engedélyezés**: Kapcsolja be a "📨 Telegram értesítések engedélyezése" opciót

### 4. Előrejelzés Küldése

1. Töltse ki az előrejelzési paramétereket
2. Kattintson az "🔮 Látogatószám Előrejelzése" gombra
3. Ha a Telegram értesítések engedélyezve vannak, automatikusan küld üzenetet

## 📨 Üzenet Formátum

A bot a következő formátumban küldi az előrejelzéseket:

```
🏬 WestEnd Látogatószám Előrejelzés

📅 Dátum: 2024-06-15 (Saturday) 🎯
🌤️ Időjárás: 25°C, 0mm csapadék
💰 Marketing: 500 EUR

📈 ELŐREJELZÉS: 12,500 fő

📊 Összehasonlítás:
• Hétvégi átlagtól: +15.2%
• Globális átlagtól: +8.7%

📈 Referencia értékek:
• Hétvégi átlag: 12,800 fő
• Globális átlag: 11,119 fő

🎯 Státusz: 🟢 Átlag feletti forgalom

⏰ Generálva: 2024-06-15 14:30:25
```

## 🔧 Hibaelhárítás

### Bot nem válaszol
- Ellenőrizze, hogy a bot aktív-e: `/start` parancs
- Próbálja újra elindítani a bot-ot

### Chat ID hibás
- Győződjön meg róla, hogy a Chat ID számokból áll
- Negatív számok is lehetségesek (csoportok esetén)

### Értesítések nem érkeznek
1. Ellenőrizze a Streamlit sidebar beállításokat
2. Tesztelje a bot kapcsolatot
3. Győződjön meg róla, hogy a Chat ID helyes

### API hibák
- Ellenőrizze az internetkapcsolatot
- A bot token érvényes és aktív

## 🔒 Biztonsági Megjegyzések

- A bot token bizalmas információ
- Ne ossza meg másokkal a bot token-t
- A Chat ID személyes azonosító

## 📞 Támogatás

Ha problémába ütközik:
1. Ellenőrizze a Streamlit alkalmazás hibaüzeneteit
2. Tesztelje a bot kapcsolatot
3. Győződjön meg róla, hogy minden beállítás helyes

## 🎯 Funkciók

### Automatikus Értesítések
- Minden előrejelzés után automatikus üzenet
- Részletes statisztikák és összehasonlítások
- Színes emoji-k a könnyebb olvashatóságért

### Opcionális Chat ID
- Ha nincs megadva Chat ID, minden regisztrált chat-re küld
- Specifikus Chat ID megadásával célzott küldés

### Státusz Visszajelzés
- Sikeres küldés megerősítése
- Hibaüzenetek részletes leírással
