import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import main


def welcome_page():
    sg.theme("Material2")
    layout = [[sg.Image(r"C:\Users\lenovo\Dropbox\LearningPython\Tana\Tana-Assistant\tana logo 2.png")],
              [sg.Text("Welcome", size=(
                  30, 1), justification='center', font=("Calibri", 25), relief=sg.RELIEF_RIDGE)],
              [sg.Text("sign in for help with google tasks", size=(
                  30, 1), justification='center', font=("Calibri", 14), relief=sg.RELIEF_RIDGE)],
              [sg.Button("Sign in"),  sg.Button('Exit')]]
    return sg.Window("Welcome to Tana", layout, size=(300, 200), resizable=False, no_titlebar=False, grab_anywhere=True,  finalize=True)


# TODO:
# button for signing in to google image
def main_page():
    sg.theme("Material2")
    layout = [[sg.Image(r"C:\Users\lenovo\Dropbox\LearningPython\Tana\Tana-Assistant\tana logo 2.png")],
              [sg.Text("What can I help you with?", size=(
                  30, 1), justification='center', font=("Calibri", 25), relief=sg.RELIEF_RIDGE)],
              [sg.Text("try saying ....", size=(
                  30, 1), justification='center', font=("Calibri", 14), relief=sg.RELIEF_RIDGE)], ]
    return sg.Window("Tana - Virtual Assistant", layout, size=(400, 200), resizable=False, no_titlebar=False, grab_anywhere=True,  finalize=True)


# will most likely have a run main page function and a run welcome page function because diff button
def run_welcome_page():
    window = welcome_page()
    while True:             # Event Loop
        window, event = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            # window.close()
    window.close()


def run_main_page():
    window = main_page()
    while True:             # Event Loop
        window, event = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
            # window.close()
    window.close()


# run_main_page()
# run_welcome_page()
