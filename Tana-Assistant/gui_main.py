import PySimpleGUI as sg
import voice
import threading
import time
import file_handler

LOGO = r"C:\Users\lenovo\Dropbox\LearningPython\Tana\Tana-Assistant\assets\tana_logo_2.png"


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
               [sg.Multiline("", size=(100, 10), disabled=True, text_color="grey", background_color="white",
                             justification='left', font=("Calibri", 13), key="-Response-")],
               [loader]

               ]

    layout = [[sg.Column(layout1, visible=False, key='-COL1-'), sg.Column(layout2, visible=False,
                                                                          key='-COL2-'), sg.Column(layout3, visible=True, key='-COL3-')]]
    return sg.Window("Tana", layout, size=(450, 600), background_color="white", resizable=False, no_titlebar=False, grab_anywhere=True,  finalize=True)


def split_for_type_writer_effect(string):
    list = []
    for index in range(len(string)):

        if index == 0:
            list.append(string[index])
        else:
            list.append(f"{list[index-1]} {string[index]}")

    return list


def text_effect_display(text, key, window):
    DELAY = 0.025  # increase for slower type writer like effect
    split_list = split_for_type_writer_effect(text)

    for char in split_list:
        window[key].update(value=char)
        time.sleep(DELAY)


def listen_thread(window):
    command = voice.listen()
    if ("Audio Error" in command):  # if audio error (usually stalled input) just keep waiting
        return

    elif ("Request Failed" in command):
        window.write_event_value("-Internet Error-", "")
        return

    elif ("Device Error" in command):
        window.write_event_value("-Device Error-", "")
        return

    text_effect_display(command, "-Command-", window)
    # window["-Command-"].update(value=command)

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

    while 1:
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

            try:
                voice.respond("What can I help you with?")
                listen(window)
                initial_query = False
            except Exception as ex:
                sg.popup(f"Ooops no internet please reconnect and restart Tana")
                break

        elif event == '-Internet Error-':
            sg.popup(":( no internet please reconnect and restart Tana")
            break

        elif event == '-Device Error-':
            sg.popup(":( make sure to have a default microphone enabled")
            break

        elif event == '-Listen Thread Done-':
            listen(window)
            slow_animate = False
            # break

        if event == sg.WIN_CLOSED:
            break

    window.close()
