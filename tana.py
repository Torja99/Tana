import wolframalpha
import wikipedia
import PySimpleGUI as sg
client = wolframalpha.Client(app_id="8E4WW5-HR875K642A")


sg.theme("Dark")
# things inside window
layout = [[sg.Text("Enter a command"), sg.InputText()],
          [sg.Text(size=(40, 1), key='-OUTPUT-')],
          [sg.Button("Ok", bind_return_key=True), sg.Button("Cancel")]]

# creating the window
window = sg.Window("Tana", layout)

while True:
    event, values = window.read()
    if event in (None, "Cancel"):
        break
    try:
        res = client.query(values[0])
        wolfram_res = next(res.results).text
        sg.popup_no_wait("Wolfram Result: " + wolfram_res)
    except BaseException:

        wiki_res = wikipedia.summary(values[0], sentences=2)
        sg.popup_no_wait("Wikipedia Result: " + wiki_res)
        window['-OUTPUT-'].update("Not a valid command")

window.close()
