from tkinter import filedialog as fd
filename = fd.askopenfilename(title="Open .tmx File.")
dir = fd.askdirectory()
for x in range(5):
    for y in range(6):
        f = open(f"{dir}/24cM_x{x}_y{y}.tmx", "w")
        f.write(open(filename, "r").read())