from tkinter import *
import pandas as pd
import random
from PIL import Image, ImageTk
import typing

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_bg, image=front)
    canvas.itemconfig(card_title, fill="black", text="French")
    canvas.itemconfig(card_word, fill="black", text=f"{current_card['French']}")
    flip_timer = window.after(3000, func=flip)

def known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip():
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=f"{current_card['English']}")
    canvas.itemconfig(card_bg, image=back)



window = Tk()
window.title("Flash Cards")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)
window.geometry("1000x700")

# Timer 
flip_timer = window.after(3000, func=flip)

# Front card 
canvas = Canvas(width=800, height=526, highlightthickness=0)
front = PhotoImage(file="images/card_front.png")

# Back card
back = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=front)

canvas.config(bg=BACKGROUND_COLOR)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 40, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# Right image
check_image = Image.open("images/right.png")
check_image = ImageTk.PhotoImage(check_image)
known_button = Button(image=check_image, highlightthickness=0, command=known)
known_button.grid(column=1, row=1)

# Wrong image
wrong_image = Image.open("images/wrong.png")
wrong_image = ImageTk.PhotoImage(wrong_image)
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()

window.mainloop()
