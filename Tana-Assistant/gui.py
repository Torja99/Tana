import PySimpleGUI as sg
import auth
import voice
import threading
import time

LOGO = r"C:\Users\lenovo\Dropbox\LearningPython\Tana\Tana-Assistant\assets\tana_logo_2.png"


def welcome_page():
    sg.theme("Material 2")
    sg.theme_background_color("white")
    google_base64 = b"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"
    layout = [[sg.Image(LOGO, background_color="white")],
              [sg.Text("Welcome", size=(
                  30, 1), background_color="white", justification='center', font=("Calibri", 25), relief=sg.RELIEF_RIDGE)],
              [sg.Button('', image_data=google_base64, tooltip="sign in",
                         button_color=("white", "white"), border_width=0, key='Sign In')]]
    return (sg.Window("Tana", layout, size=(
        300, 200), resizable=False, no_titlebar=False, grab_anywhere=True, background_color="white", finalize=True))


def run_welcome_page(creds, SCOPES):
    window = welcome_page()

    while True:  # Event Loop
        event, values = window.read()
        if (event == "Sign In"):
            auth.auth_flow(creds, SCOPES)
            break
        if event == sg.WIN_CLOSED:
            break
    window.close()
    run_main_page()


def main_page():
    sg.theme("Material 2")
    sg.theme_background_color("white")

    layout1 = [[sg.Image(LOGO, background_color="white")],
               [sg.Text("What can I help you with?", size=(
                   150, 1), background_color="white", justification='center', font=("Calibri", 15),  relief=sg.RELIEF_RIDGE)],
               ]
    layout2 = [[sg.Image(LOGO, background_color="white")],
               [sg.Text("try saying ....", size=(
                   45, 1), background_color="white", justification='center', font=("Calibri", 14), relief=sg.RELIEF_RIDGE)],
               [sg.Text("\"create task get groceries\"", size=(
                   45, 1), background_color="white", text_color=("grey"), justification='center', font=("Calibri", 14), relief=sg.RELIEF_RIDGE)],
               [sg.Text("\"what's the weather in Toronto\"", size=(
                   45, 1), justification='center', background_color="white",  text_color=("grey"), font=("Calibri", 14), relief=sg.RELIEF_RIDGE)],
               ]

    logo = sg.Image(LOGO, background_color="white")
    loader = sg.Image(r"assets\loader.gif",
                      background_color="white", key="-Load-")
    layout3 = [[logo],

               [sg.Text("What can I help you with?", size=(100, 1),  background_color="white",
                        justification='left', font=("Calibri", 13))],

               [sg.Text("",  size=(100, 1), text_color="grey", background_color="white",
                        justification='right', font=("Calibri", 13), key="-Command-")],
               [sg.Text("", size=(100, 1),  background_color="white",
                        justification='left', font=("Calibri", 13), key="-Response-")],
               [loader]

               ]

    # ----------- Create actual layout using Columns and a row of Buttons
    layout = [[sg.Column(layout1, visible=False, key='-COL1-'), sg.Column(layout2, visible=False,
                                                                          key='-COL2-'), sg.Column(layout3, visible=True, key='-COL3-')]]
    return sg.Window("Tana", layout, size=(400, 300), background_color="white", resizable=False, no_titlebar=False, grab_anywhere=True,  finalize=True)


def split_for_type_writer_effect(string):
    list = []
    for index in range(len(string)):

        if index == 0:
            list.append(string[index])
        else:
            list.append(list[index-1] + string[index])

    return list


def text_effect_display(text, key, window):
    DELAY = 0.025  # increase for slower type writer like effect
    split_list = split_for_type_writer_effect(text)

    for char in split_list:
        window[key].update(value=char)
        time.sleep(DELAY)


def listen_thread(window):
    command = voice.listen()
    if (command == "Audio Error"):  # if audio error (usually stalled input) just keep waiting
        window.write_event_value("-Listen Thread Done-", "")
        return
    # window["-Response-"].update(value="")

    text_effect_display(command, "-Command-", window)

    window.write_event_value("-Handle Command Begin-", "")
    response = voice.handle_command(command)

    if (response == "Goodbye!"):
        text_effect_display(response, "-Response-", window)
        time.sleep(1)
        window.write_event_value(sg.WINDOW_CLOSED, "")

    text_effect_display(response, "-Response-", window)
    time.sleep(4)  # time for user to read answer before it is erased
    window["-Command-"].update(value="")
    window["-Response-"].update(value="")
    window.write_event_value("-Listen Thread Done-", "")


def listen(window):
    threading.Thread(target=listen_thread, args=(
        window,), daemon=True).start()


def run_main_page():
    window = main_page()
    load_gif = window["-Load-"]
    slow_animate = False
    initial_query = True

    while True:
        event, values = window.read(timeout=10)

        if slow_animate:
            load_gif.update_animation(
                load_gif.Filename, time_between_frames=40)
        else:
            load_gif.update_animation(
                load_gif.Filename, time_between_frames=25)

        if event == "-Handle Command Begin-":
            slow_animate = True

        if initial_query:

            voice.respond("What can I help you with?")
            listen(window)
            initial_query = False

        elif event == '-Listen Thread Done-':
            listen(window)
            slow_animate = False

        if event == sg.WIN_CLOSED:
            break

    window.close()
