import asyncio
import os
import sys
import uvloop  # ⚡ Quantum Speed Engine
from pyrogram import Client, idle
from pyrogram.errors import Unauthorized
from config import API_ID, API_HASH, BOT_TOKENS, LOGGER, WORKERS

# 🔥 MAIN FIX: Database ab Core folder se aayega
from core import database  

# ==========================================
# ⚡ UVLOOP INSTALLATION (C++ LEVEL SPEED)
# ==========================================
uvloop.install()

# Sessions folder check
if not os.path.exists("sessions"):
    os.makedirs("sessions")

# Global list for inter-bot communication
MATRIX_NODES = []

async def boot_matrix():
    LOGGER.info("🚀 Booting up the Monster Matrix Core Engine...")

    valid_bots = 0

    # 🎛️ STEP 1: NODES CONFIGURATION
    for index, token in enumerate(BOT_TOKENS, start=1):
        try:
            bot = Client(
                name=f"sessions/Node_{index}", # 🔥 Har bot ka unique session
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                plugins=dict(root="plugins"),
                workers=WORKERS,  # ⚡ Quantum Workers Load
                in_memory=False
            )
            MATRIX_NODES.append(bot)
            valid_bots += 1
        except Exception as e:
            LOGGER.error(f"⚠️ Failed to configure Node {index}: {e}")

    if valid_bots == 0:
        LOGGER.error("💀 FATAL ERROR: No valid bots found. Matrix Grid Down!")
        sys.exit(1)

    LOGGER.info(f"🔥 Grid Active! Igniting {valid_bots} Nodes with {WORKERS} Workers each...")

    # 🚀 STEP 2: STAGGERED IGNITION SYSTEM (Database Lock Bypass)
    # Ham compose() use nahi karenge, kyuki wo sabko ek sath fire karta hai.
    # Ham ek-ek karke bots start karenge (1.5s delay ke sath) taaki SQLite lock na ho!
    
    started_nodes = []
    for node in MATRIX_NODES:
        try:
            await node.start()
            started_nodes.append(node)
            LOGGER.info(f"✅ {node.name.split('/')[-1]} Online & Synced!")
            await asyncio.sleep(1.5)  # 🔥 THE MAGIC DELAY (No Database Lock Error)
        except Unauthorized:
            LOGGER.error(f"❌ Token for {node.name} is Invalid or Revoked!")
        except Exception as e:
            LOGGER.error(f"⚠️ Failed to start {node.name}: {e}")

    if not started_nodes:
        LOGGER.error("💀 All nodes failed to start. Aborting.")
        sys.exit(1)

    LOGGER.info("😈 ALL NODES ARE FULLY OPERATIONAL. MATRIX IS LIVE! 😈")

    # 🛑 STEP 3: IDLE MANAGER (System ko zinda rakhega)
    await idle()

    # 🔌 STEP 4: GRACEFUL SHUTDOWN (Ctrl+C dabane par database corrupt hone se bachayega)
    LOGGER.info("🛑 Shutting down Matrix Nodes gracefully...")
    for node in started_nodes:
        try:
            await node.stop()
        except Exception:
            pass
    LOGGER.info("🔌 Matrix Engine Completely Offline.")

if __name__ == "__main__":
    try:
        # ☠️ MONSTER MATRIX HACKER BANNER ☠️
        print("\n" + "="*50)
        print(" ☠️  M O N S T E R   M A T R I X   E N G I N E   ☠️ ")
        print("="*50 + "\n")

        asyncio.run(boot_matrix())
    except KeyboardInterrupt:
        print("\n")
        LOGGER.warning("⚠️ System manually halted by Master (Ctrl+C).")
    except Exception as e:
        LOGGER.error(f"💀 Core Engine Crash: {e}")
