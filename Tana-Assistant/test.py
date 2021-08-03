import PySimpleGUI as Sg

layout = [[Sg.Multiline("", disabled=True, key="ml")],
          [Sg.Button("update", key="button")]]

window1 = Sg.Window("").Layout(layout).Finalize()

ml_obj = window1.FindElement("ml")
ml_obj.Update(disabled=True)

while True:
    b, v = window1.Read(timeout=0)

    if b == "button":
        ml_obj.Update(disabled=False)
        ml_obj.Update("ok, ok")
        ml_obj.Update(disabled=True)

    if b is None:
        break

    else:
        pass
