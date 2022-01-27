import sys
import re
import PySimpleGUI as sg
import asyncio
import WAH_WhatsApp_Automation_helper
from WAH_WhatsApp_Automation_helper.MongoDb_Service import *


def create_layout():
    layout_login = [
        [sg.Text("Log - In")],
        [sg.Text("User Name:", size=(9, 1)), sg.InputText(key="username_log_in")],
        [sg.Text("Password:", size=(9, 1)), sg.InputText(password_char='*', key="password_log_in")],
        [sg.Text("", key="rand", size=(20, 1))],
        [sg.Text("", key="login_status", size=(25, 1))],
        [sg.Button("Connect"), sg.Button("Sign Up Now"), sg.Button("Quit")],
    ]

    control_panel_column = [
        [sg.Text("Control Panel", size=[13, 1]), sg.Button("Log-Out")],
        [sg.Text("Work on:", size=[13, 1]), sg.InputText(size=(25, 1), enable_events=True, key="Name")],
        [sg.Text("Destination:", size=[13, 1]), sg.InputText(size=(25, 1), enable_events=True, key="dast")],
        [sg.Text("Message Content:", size=[13, 1]), sg.InputText(size=(25, 1), enable_events=True, key="msg_content")],
        # [sg.Text("Target number:", size=[15, 1])],
        # [sg.Radio("single target", "RADIO", key="single")],
        # [sg.Radio("multiple targets", "RADIO", key="multiple")],
        [sg.Input(key="StartTime", size=(13, 1)),
         sg.CalendarButton("Start action at", close_when_date_chosen=True, target="StartTime", location=(0, 0),
                           no_titlebar=False)],
        [sg.Text("Functions:", size=[10, 1])],
        [sg.Button("Mark Unread as Read")],
        [sg.Button("Send Message"), sg.Button("Last Seen")],
    ]
    output_column = [
        [sg.Text("Output:")],
        [sg.Text(size=(40, 1), key="-OUTPUT-")],
        [sg.Listbox(values=[], enable_events=False, size=(40, 20), key="-OUTPUT LIST-")],
        [sg.Button("End Action"), sg.Button("Clear")],
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
        [sg.Text('First Name:', size=(13, 1)), sg.InputText(enable_events=True, key='f_name_sign_up')],
        [sg.Text('Last Name:', size=(13, 1)), sg.InputText(enable_events=True, key='l_name_sign_up')],
        [sg.Text('Email:', size=(13, 1)), sg.InputText(enable_events=True, key='email_sign_up')],
        [sg.Text('User Name:', size=(13, 1)), sg.InputText(enable_events=True, key='user_name_sign_up')],
        [sg.Text('Password:', size=(13, 1)),
         sg.InputText(enable_events=True, key='password_sign_up', password_char='*')],
        [sg.Text('Repeat Password:', size=(13, 1)),
         sg.InputText(enable_events=True, key='re_password_sign_up', password_char='*')],
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
    elif check_field_exists("UserName", values["user_name_sign_up"]):
        values_invalid.append("User Name already exists")
        is_valid = False
    if len(values["password_sign_up"]) == 0:
        values_invalid.append("Password is required")
        is_valid = False
    elif len(values["password_sign_up"]) < 5:
        values_invalid.append("Password should be at least 6 chars")
        is_valid = False
    if values["password_sign_up"] != values["re_password_sign_up"]:
        values_invalid.append("Passwords don't match")
        is_valid = False
    elif check_field_exists("Password", values["password_sign_up"]):
        values_invalid.append("Password already exists")
        is_valid = False
    return is_valid, values_invalid


def validate_last_seen(values):
    is_valid = True
    values_invalid = []
    if len(values["Name"]) == 0:
        values_invalid.append("Work on is required")
        is_valid = False
    if values["dast"] == 0:
        values_invalid.append("Destination is required if you want to send updates to your phone")
    return is_valid, values_invalid


def validate_send_msg(values):
    is_valid = True
    values_invalid = []
    if len(values["dast"]) == 0:
        values_invalid.append("Destination required")
        is_valid = False
    if len(values["msg_content"]) == 0:
        values_invalid.append("Message Content required")
        is_valid = False

    # if not values["single"] and not values[""]:
    #     values_invalid.append("Target number are required")
    #     is_valid = False
    return is_valid, values_invalid


def generate_error_message(values_invalid):
    error_message = ""
    for value in values_invalid:
        error_message += value + "\n"
    return error_message


def get_targets(targets_string):
    targets = targets_string.split(",")
    for i in range(len(targets)):
        targets[i] = targets[i].strip()
    return targets


async def ui():
    output = []
    last_seen = False
    connected_on, online_status, name_last, dast_last = None, False, "", ""
    while True:
        event, values = WAH_WhatsApp_Automation_helper.window.read(timeout=1)
        WAH_WhatsApp_Automation_helper.STATE = "ready"
        if event == "Quit" or event == sg.WIN_CLOSED:
            if WAH_WhatsApp_Automation_helper.window["main_panel"].visible:
                WAH_WhatsApp_Automation_helper.wah.quit()
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
                add_new_user(f_name=values["f_name_sign_up"], l_name=values["l_name_sign_up"],
                             email=values["email_sign_up"], username=values["user_name_sign_up"],
                             password=values["password_sign_up"])
                WAH_WhatsApp_Automation_helper.window["sign_up_panel"].update(visible=False)
                WAH_WhatsApp_Automation_helper.window["main_panel"].update(visible=True)
                WAH_WhatsApp_Automation_helper.wah.start()
        elif event == "Connect":
            if check_user_exists(values["username_log_in"], values["password_log_in"]):
                WAH_WhatsApp_Automation_helper.window["login_panel"].update(visible=False)
                WAH_WhatsApp_Automation_helper.window["main_panel"].update(visible=True)
                WAH_WhatsApp_Automation_helper.wah.start()
            else:
                WAH_WhatsApp_Automation_helper.window["login_status"].update("Wrong User Name or Password")
        elif event == "Last Seen":
            is_valid, values_invalid = validate_last_seen(values)
            if not is_valid:
                sg.popup(generate_error_message(values_invalid))
            else:
                last_seen = True
                name_last, dast_last = values["Name"], values["dast"]
                output.append(f"online check for {name_last} :")
                output.append("Starting...")
                WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
                WAH_WhatsApp_Automation_helper.wah.last_seen_move(values["Name"])
        elif event == "End Action":
            if last_seen:
                output.append("Action Stopped.")
                WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
                last_seen = False
            else:
                output.append("No action detected")
                WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
        elif event == "Send Message":
            is_valid, values_invalid = validate_send_msg(values)
            if not is_valid:
                sg.popup(generate_error_message(values_invalid))
            else:
                for target in get_targets(values["dast"]):
                    if values["StartTime"]:
                        output.append(f"Will send {values['msg_content']} to {target} at {values['StartTime']}")
                        WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
                        WAH_WhatsApp_Automation_helper.wah.send_message_on_time(send_to=target,
                                                                                message=values["msg_content"],
                                                                                send_on_time=values['StartTime'])
                    else:
                        output.append(f"Sending {values['msg_content']} to {target}")
                        WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
                        WAH_WhatsApp_Automation_helper.wah.send_message(send_to=target, message=values["msg_content"])
        elif event == "Log-Out":
            WAH_WhatsApp_Automation_helper.window["login_panel"].update(visible=True)
            WAH_WhatsApp_Automation_helper.window["main_panel"].update(visible=False)
        elif event == "Mark Unread as Read":
            output.append(f"reading all unread chats..")
            WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
            WAH_WhatsApp_Automation_helper.wah.read_all_unread_messages()
            output.append(f"all Chats been read")
            WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
        elif event == "Clear":
            output.clear()
            WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
        if last_seen:
            online_string, connected_on, online_status = WAH_WhatsApp_Automation_helper.wah.last_seen_run(name_last,
                                                                                                          dast_last,
                                                                                                          online_status,
                                                                                                          connected_on)
            if online_string:
                output.append(online_string)
                WAH_WhatsApp_Automation_helper.window["-OUTPUT LIST-"].update(output)
        await asyncio.sleep(0)
