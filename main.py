import asyncio
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

# Global list for inter-bot communication
MATRIX_NODES = []

async def boot_matrix():
    LOGGER.info("🚀 𝐁ᴏᴏᴛɪɴɢ 𝐔ᴘ 𝐓ʜᴇ 𝐌ᴀᴅᴀʀᴀ 𝐌ᴀᴛʀɪx 𝐂ᴏʀᴇ 𝐄ɴɢɪɴᴇ...")

    valid_bots = 0

    # 🎛️ STEP 1: NODES CONFIGURATION
    for index, token in enumerate(BOT_TOKENS, start=1):
        try:
            bot = Client(
                name=f"Node_{index}", # 🔥 'sessions/' hata diya, ab seedha RAM me banega
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                plugins=dict(root="plugins"),
                workers=WORKERS,  # ⚡ Quantum Workers Load
                in_memory=True  # 🔥 THE SILVER BULLET (Isse kabhi database lock nahi hoga) 🔥
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
    started_nodes = []
    for node in MATRIX_NODES:
        try:
            await node.start()
            started_nodes.append(node)
            LOGGER.info(f"✅ {node.name} Online & Synced!")
            await asyncio.sleep(1.5)  # 🔥 THE MAGIC DELAY
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

    # 🔌 STEP 4: GRACEFUL SHUTDOWN (Ctrl+C dabane par crash hone se bachayega)
    LOGGER.info("🛑 Shutting down Matrix Nodes gracefully...")
    for node in started_nodes:
        try:
            await node.stop()
        except Exception:
            pass
    LOGGER.info("🔌 Matrix Engine Completely Offline.")

if __name__ == "__main__":
    try:
        # ☠️ MADARA SIX PATHS BANNER ☠️
        print("\n" + "=" * 60)
        print(" ☠️  M A D A R A   S I X   P A T H S   E N G I N E   ☠️ ")
        print("=" * 60 + "\n")

        asyncio.run(boot_matrix())

    except KeyboardInterrupt:
        print("\n")
        LOGGER.warning("⚠️ System manually halted by Master (Ctrl+C).")

    except Exception as e:
        LOGGER.error(f"💀 Core Engine Crash: {e}")
