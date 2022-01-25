import random
import asyncio
import WAH_WhatsApp_Automation_helper
import PySimpleGUI as sg
from WAH_WhatsApp_Automation_helper.GUI import generate_error_message


async def background():
    while True:
        rando = random.randint(2, 20000)
        if WAH_WhatsApp_Automation_helper.STATE != "init":
            WAH_WhatsApp_Automation_helper.window["rand"].update(rando)
        await asyncio.sleep(0)
