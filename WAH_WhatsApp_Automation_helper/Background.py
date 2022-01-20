import random
import asyncio
import WAH_WhatsApp_Automation_helper


async def background():
    while True:
        rando = random.randint(2, 20000)
        if WAH_WhatsApp_Automation_helper.STATE != "init":
            WAH_WhatsApp_Automation_helper.window["login_status"].update(rando)
        await asyncio.sleep(0)
