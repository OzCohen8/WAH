import WAH_WhatsApp_Automation_helper
import asyncio

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WAH_WhatsApp_Automation_helper.wait_list())
    loop.close()
