import sys
import re
import PySimpleGUI as sg
import asyncio
import WAH_WhatsApp_Automation_helper
from WAH_WhatsApp_Automation_helper.MongoDb_Service import *


def create_layout():
    layout_login = [
        [sg.Text("")],
        [sg.Text("Password: "), sg.InputText(password_char='*', key="password")],
        [sg.Text("", key="login_status", size=(20, 1))],
        [sg.Button("Connect"), sg.Button("Sign Up Now"), sg.Button("Quit")],
    ]

    control_panel_column = [
        [sg.Text("Control Panel")],
        [sg.Text("global Functions:")],
        [sg.Button("Mark all Unread as Read")],
        [sg.Text("personal Functions:")],
        [sg.Button("Send Message"), sg.Button("Last Seen")],
        [sg.Text("Work on:"), sg.InputText(size=(25, 1), enable_events=True, key="-Name-")],
    ]
    output_column = [
        [sg.Text("OutPut:")],
        [sg.Text(size=(40, 1), key="-OUTPUT-")],
        [sg.Listbox(values=[], enable_events=True, size=(30, 18), key="-OUTPUT LIST-")],
    ]
    layout_main = [
        [
            sg.Column(control_panel_column),
            sg.VSeperator(),
            sg.Column(output_column),
        ]
    ]

    layout_sign_up = [
        [sg.Text('Sign Up Now!')],
        [sg.Text('Please enter your Name, Email, Username and password')],
        [sg.Text('First Name:', size=(10, 1)), sg.InputText(enable_events=True, key='f_name_sign_up')],
        [sg.Text('Last Name:', size=(10, 1)), sg.InputText(enable_events=True, key='l_name_sign_up')],
        [sg.Text('Email:', size=(10, 1)), sg.InputText(enable_events=True, key='email_sign_up')],
        [sg.Text('User Name:', size=(10, 1)), sg.InputText(enable_events=True, key='user_name_sign_up')],
        [sg.Text('Password:', size=(10, 1)), sg.InputText(enable_events=True, key='password_sign_up')],
        [sg.Button("Sign Up"), sg.Cancel("Cancel")]
    ]

    col_login = sg.Column(layout_login, key="login_panel")
    col_main = sg.Column(layout_main, key="main_panel", visible=False)
    col_sign_up = sg.Column(layout_sign_up, key="sign_up_panel", visible=False)

    layout = [
        [sg.Pane([col_login, col_main, col_sign_up], relief=sg.RELIEF_FLAT)]
    ]

    return layout


def validate_sign_up(values):
    name_reg = r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
    email_reg = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    is_valid = True
    values_invalid = []
    if len(values["f_name_sign_up"]) == 0:
        values_invalid.append("First Name is required")
        is_valid = False
    elif not re.search(name_reg, values["f_name_sign_up"]):
        is_valid = False
        values_invalid.append("First Name should contain only characters")
    if len(values["l_name_sign_up"]) == 0:
        values_invalid.append("Last Name is required")
        is_valid = False
    elif not re.search(name_reg, values["l_name_sign_up"]):
        is_valid = False
        values_invalid.append("Last Name should contain only characters")
    if len(values["email_sign_up"]) == 0:
        values_invalid.append("Email is required")
        is_valid = False
    elif not re.search(email_reg, values["email_sign_up"]):
        values_invalid.append("Email is not valid")
        is_valid = False
    if len(values["user_name_sign_up"]) == 0:
        values_invalid.append("User Name is required")
        is_valid = False
    elif len(values["user_name_sign_up"]) < 4:
        values_invalid.append("User Name should be at least 5 chars")
        is_valid = False
    if len(values["password_sign_up"]) == 0:
        values_invalid.append("Password is required")
        is_valid = False
    elif len(values["password_sign_up"]) < 5:
        values_invalid.append("Password should be at least 6 chars")
        is_valid = False
    return is_valid, values_invalid


def generate_error_message(values_invalid):
    error_message = ""
    for value in values_invalid:
        error_message += value + "\n"
    return error_message


async def ui():
    while True:
        event, values = WAH_WhatsApp_Automation_helper.window.read(timeout=1)
        WAH_WhatsApp_Automation_helper.STATE = "ready"
        if event == "Quit" or event == sg.WIN_CLOSED:
            sys.exit()
        elif event == "Sign Up Now":
            WAH_WhatsApp_Automation_helper.window["login_panel"].update(visible=False)
            WAH_WhatsApp_Automation_helper.window["sign_up_panel"].update(visible=True)
        elif event == "Cancel":
            WAH_WhatsApp_Automation_helper.window["login_panel"].update(visible=True)
            WAH_WhatsApp_Automation_helper.window["sign_up_panel"].update(visible=False)
        elif event == "Sign Up":
            is_valid, values_invalid = validate_sign_up(values)
            if not is_valid:
                sg.popup(generate_error_message(values_invalid))
            else:
                add_new_user(f_name=values["f_name_sign_up"], l_name=values["l_name_sign_up"], email=values["email_sign_up"], username=values["user_name_sign_up"],password=values["password_sign_up"])
                WAH_WhatsApp_Automation_helper.window["sign_up_panel"].update(visible=False)
                WAH_WhatsApp_Automation_helper.window["main_panel"].update(visible=True)
        elif event == "Connect":
            WAH_WhatsApp_Automation_helper.window["login_panel"].update(visible=False)
            WAH_WhatsApp_Automation_helper.window["main_panel"].update(visible=True)
        await asyncio.sleep(0)
