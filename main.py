from tkinter import *
import random
import pandas
import os

BACKGROUND_COLOR = "#B1DDC6"
FONT = "Lucida Bright"
list_int = 0
still_to_learn = []


# Functions

def next_word(iscorrect, isfirst):
    global translate_list
    global temp_dict
    global still_to_learn
    temp_dict = random.choice(translate_list)
    if iscorrect is True and isfirst > 0:
        print(isfirst)
        translate_list.remove(temp_dict)
    elif iscorrect is False and isfirst > 0:
        print(translate_list)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(lang_text, text="French")
    canvas.itemconfig(flash_text, text=temp_dict["French"])
    canvas.after(10000, flip_card)


def flip_card():
    global translate_list
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(lang_text, text="English")
    canvas.itemconfig(flash_text, text=temp_dict["English"])


def correct_func():
    global translate_list
    global list_int
    list_int += 1
    next_word(True, list_int)


def incorrect_func():
    global list_int
    list_int += 1
    next_word(False, list_int)


def export():
    global translate_list
    print(translate_list)
    export_df = pandas.DataFrame.from_records(translate_list)
    export_df.to_csv("still_to_learn.csv", mode="w", index=False)


def start():
    next_word(False, 0)


def print_dict():
    global translate_list
    print(translate_list)


# Build Window

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Cards

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas = Canvas(height=526, width=800, highlightthickness=0, background=BACKGROUND_COLOR)
canvas_image = canvas.create_image(400, 263, image=card_front)
lang_text = canvas.create_text(400, 150, text="French Practice", font=(FONT, 18, "italic"))
flash_text = canvas.create_text(400, 240, text="Hit the Start Button to Begin", font=(FONT, 30, "bold"))
canvas.grid(column=0, columnspan=2, row=0)

# Buttons

checkmark = PhotoImage(file="images/right.png")
xmark = PhotoImage(file="images/wrong.png")
correct = Button(image=checkmark, highlightthickness=0, command=correct_func)
correct.grid(column=1, row=1)
incorrect = Button(image=xmark, highlightthickness=0, command=incorrect_func)
incorrect.grid(column=0, row=1)
finish = Button(text="Export List", command=export)
finish.grid(column=0, columnspan=2, row=4)
start_button = Button(text="Start", command=start)
start_button.grid(column=0, columnspan=2, row=3)

## Pandas Integration

if os.path.exists("still_to_learn.csv"):
    translate_csv = pandas.read_csv("still_to_learn.csv")
else:
    translate_csv = pandas.read_csv("data/french_words.csv")
translate_list = translate_csv.to_dict(orient="records")
print(translate_list)

# Debugging
# print_dict = Button(text="Print Dictionary", command=print_dict)
# print_dict.grid(column=0, row=3)


window.mainloop()
