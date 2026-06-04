import asyncio
import os
import sys
import uvloop  # ⚡ Quantum Speed Engine
from pyrogram import Client, compose
from pyrogram.errors import Unauthorized, AuthKeyUnregistered
from config import API_ID, API_HASH, BOT_TOKENS, LOGGER, WORKERS, LOG_GROUP_ID
import database  # DB Initialization

# ==========================================
# ⚡ UVLOOP INSTALLATION (C++ LEVEL SPEED)
# ==========================================
# Pyrogram ke normal asyncio ko hatakar superfast engine lagayega
uvloop.install()

# Sessions folder check
if not os.path.exists("sessions"):
    os.makedirs("sessions")

# Ek global list, takii plugins mein agar 1 bot se dusre bot ko command deni ho to kaam aaye
MATRIX_NODES = []

async def boot_matrix():
    LOGGER.info("🚀 Booting up the Yuki Matrix Core Engine...")
    
    valid_bots = 0

    for index, token in enumerate(BOT_TOKENS, start=1):
        try:
            bot = Client(
                name=f"sessions/Node_{index}",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                plugins=dict(root="plugins"),
                workers=WORKERS,  # 🔥 Quantum Workers Load (Config se)
                in_memory=False
            )
            MATRIX_NODES.append(bot)
            valid_bots += 1
            
        except Unauthorized:
            LOGGER.error(f"❌ Token {index} is Invalid or Revoked!")
        except Exception as e:
            LOGGER.error(f"⚠️ Failed to configure Node {index}: {e}")

    if valid_bots == 0:
        LOGGER.error("💀 FATAL ERROR: No valid bots found. Matrix Grid Down!")
        sys.exit(1)

    LOGGER.info(f"🔥 Grid Active! Igniting {valid_bots} Nodes with {WORKERS} Workers each...")
    
    # 🚀 Pyrogram Compose - Saare bots ek saath crash-free challenge
    await compose(MATRIX_NODES)
    
    LOGGER.info("🛑 All Nodes offline. Matrix Engine Shut Down.")

if __name__ == "__main__":
    try:
        # ☠️ YUKI MATRIX HACKER BANNER ☠️
        print("\n" + "="*50)
        print(" ☠️  Y U K I   M A T R I X   E N G I N E   ☠️ ")
        print("="*50 + "\n")
        
        asyncio.run(boot_matrix())
    except KeyboardInterrupt:
        print("\n")
        LOGGER.warning("⚠️ System manually halted by Boss (Ctrl+C).")
    except Exception as e:
        LOGGER.error(f"💀 Core Engine Crash: {e}")
