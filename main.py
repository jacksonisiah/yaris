from __future__ import annotations

from dotenv import load_dotenv

from chloe.chloe import Chloe

load_dotenv()

bot = Chloe()

if __name__ == "__main__":
    bot.run()
