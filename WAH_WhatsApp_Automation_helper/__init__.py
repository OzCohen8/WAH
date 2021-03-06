import asyncio
import PySimpleGUI as sg
from WAH_WhatsApp_Automation_helper.GUI import ui, create_layout
from WAH_WhatsApp_Automation_helper.Background import background
from WAH_WhatsApp_Automation_helper.MongoDb_Service import *
from WAH_WhatsApp_Automation_helper.whats_app_functions import *

sg.change_look_and_feel("DarkTeal1")
STATE = "init"
wah = WhatsApp()
window = sg.Window(title="WAA - WhatsApp Automation and Helper", layout=create_layout(), margins=(20, 20),)


async def wait_list():
    await asyncio.wait([asyncio.create_task(background()), asyncio.create_task(ui())])



    # p1 = Process(target=whatsapp.check_online, args=("אבא","כללי"))
    # p2 = Process(target=whatsapp.send_message_on_time, args=("אבא", "תשלח ב 00:31", "00:47 20/1/2022"))
    # processes = list()
    # processes.append(p2)
    # processes.append(p1)
    #
    # for p in processes:
    #     p.start()




