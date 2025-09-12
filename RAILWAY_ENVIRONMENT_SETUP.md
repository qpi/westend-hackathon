# Railway Environment Variables Setup

## 🚀 Telegram Bot Environment Variables

A Railway deployment-ben be kell állítani a következő környezeti változókat:

### 1. **TELEGRAM_SUBSCRIBERS**
```
TELEGRAM_SUBSCRIBERS=8121891526,7911211065
```

**Magyarázat:**
- `8121891526` - Mihály Kuprivecz (@mkuprivecz)
- `7911211065` - Peter Perecz (@peterperecz)
- Vesszővel elválasztva, szóközök nélkül

### 2. **Railway Dashboard Beállítás**

1. Menjen a Railway dashboard-ra
2. Válassza ki a projekt-et
3. **Variables** tab
4. **Add Variable**:
   - **Name**: `TELEGRAM_SUBSCRIBERS`
   - **Value**: `8121891526,7911211065`
5. **Deploy** gomb

### 3. **Új Feliratkozó Hozzáadása**

Ha új feliratkozót szeretne hozzáadni:

1. **Railway Dashboard** → **Variables**
2. **TELEGRAM_SUBSCRIBERS** szerkesztése
3. Új Chat ID hozzáadása vesszővel:
   ```
   8121891526,7911211065,NEW_CHAT_ID
   ```
4. **Save** és **Redeploy**

### 4. **Chat ID Megtalálása**

Új feliratkozó Chat ID-jának megtalálása:

1. Új felhasználó küldje el `/start` parancsot a bot-nak
2. Futtassa lokálisan: `python test_telegram_bot.py`
3. Keresse meg az új Chat ID-t a kimenetben
4. Adja hozzá a Railway environment variable-hoz

### 5. **Ellenőrzés**

A Railway alkalmazásban a sidebar mutatni fogja:
```
👥 Feliratkozók száma: 2
```

Ha ez nem jelenik meg, ellenőrizze:
- Environment variable helyesen van-e beállítva
- Deployment sikeresen lefutott-e
- Nincsenek-e szóközök a Chat ID-k között
