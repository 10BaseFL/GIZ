import subprocess
import sys
from tkinter import *
from tkinter import ttk

class Tmgch:
    def __init__(self, имя, голод, жажда, энергия, счастье):
        self.имя = имя
        self.голод = голод
        self.жажда = жажда
        self.энергия = энергия
        self.счастье = счастье

    def покормить(self):
        if not is_playing_action:
            self.голод = min(100, self.голод + 30)
            change_animation('eat.gif', 2000)
            обновить()

    def напоить(self):
        if not is_playing_action:
            self.жажда = min(100, self.жажда + 30)
            change_animation('drink.gif', 3000)
            обновить()

    def поиграть(self):
        if not is_playing_action:
            self.счастье = min(100, self.счастье + 30)
            self.энергия = max(0, self.энергия - 15)
            self.голод = max(0, self.голод - 15)
            change_animation('run.gif', 3000)
            обновить()

    def спать(self):
        if not is_playing_action:
            self.энергия = min(100, self.энергия + 40)
            self.голод = max(0, self.голод - 20)
            self.жажда = max(0, self.жажда - 35)
            self.счастье = max(0, self.счастье - 5)
            change_animation('sleep.gif', 5000)
            обновить()

current_frames = []
animation_after_id = None
is_playing_action = False


def load_frames(filename):
    frames = []
    idx = 0
    while True:
        try:
            frames.append(PhotoImage(file=filename, format=f'gif -index {idx}'))
            idx += 1
        except Exception:
            break
    return frames


def update_gif(ind):
    global animation_after_id
    if not current_frames: return

    ind = ind % len(current_frames)
    frame = current_frames[ind]
    gif_label.configure(image=frame)
    animation_after_id = root.after(100, update_gif, ind + 1)

def change_animation(filename, duration=None):
    global current_frames, animation_after_id, is_playing_action
    if animation_after_id:
        root.after_cancel(animation_after_id)

    try:
        new_frames = load_frames(filename)
        if not new_frames:
            print(f"Файл {filename} не найден или пуст")
            return

        current_frames = new_frames
        update_gif(0)

        if duration:
            is_playing_action = True
            root.after(duration, set_idle_animation)
    except Exception as e:
        print(f"Ошибка смены анимации: {e}")


def set_idle_animation():
    global is_playing_action
    is_playing_action = False
    if pet.голод < 31 or pet.жажда < 31 or pet.счастье < 31 or pet.энергия < 31:
        change_animation('needs.gif')
    else:
        change_animation('okey.gif')

def cikl():
    if not is_playing_action:
        pet.голод = max(0, pet.голод - 2)
        pet.жажда = max(0, pet.жажда - 5)
        pet.энергия = max(0, pet.энергия - 5)
        pet.счастье = max(0, pet.счастье - 3)
        обновить()
        set_idle_animation()
    root.after(5000, cikl)




pet = Tmgch("Подсолнух", 70, 70, 70, 70)

root = Tk()
root.title("Тамагочи")
root.iconbitmap('100.ico')
root.geometry("600x750+1460+400")
root.configure(background="#1976d2")

gif_label = Label(root)
gif_label.pack(pady=10)

stats_frame = Frame(root)
stats_frame.pack(pady=10)

label_hunger = Label(stats_frame, text="", font=("Arial", 12))
label_hunger.pack()
label_thirst = Label(stats_frame, text="", font=("Arial", 12))
label_thirst.pack()
label_energy = Label(stats_frame, text="", font=("Arial", 12))
label_energy.pack()
label_happiness = Label(stats_frame, text="", font=("Arial", 12))
label_happiness.pack()


def обновить():
    label_hunger.config(text=f"Голод: {pet.голод}/100")
    label_thirst.config(text=f"Жажда: {pet.жажда}/100")
    label_energy.config(text=f"Энергия: {pet.энергия}/100")
    label_happiness.config(text=f"Счастье: {pet.счастье}/100")

tetris_proc = None

def monitor_tetris():
    global tetris_proc
    if tetris_proc is not None and tetris_proc.poll() is None:
        pet.счастье = min(100, pet.счастье + 6)
        обновить()
        root.after(3000, monitor_tetris)
    else:
        tetris_proc = None
        set_idle_animation()

def tetriss():
    global tetris_proc
    if tetris_proc is not None and tetris_proc.poll() is None:
        return
    try:
        tetris_proc = subprocess.Popen([sys.executable, 'TETRIS.py'])
        monitor_tetris()
    except Exception as e:
        print(f"Не удалось запустить игру: {e}")


btn_frame = Frame(root, bg="#1976d2")
btn_frame.pack(pady=10)

btn_feed = Button(btn_frame, text="Покормить", command=pet.покормить, font=("Arial", 10), bg="#4caf50", fg="white")
btn_feed.grid(row=0, column=0, padx=5, pady=5)

btn_drink = Button(btn_frame, text="Напоить", command=pet.напоить, font=("Arial", 10), bg="#2196f3", fg="white")
btn_drink.grid(row=0, column=1, padx=5, pady=5)

btn_play = Button(btn_frame, text="Поиграть", command=pet.поиграть, font=("Arial", 10), bg="#ff9800", fg="white")
btn_play.grid(row=1, column=0, padx=5, pady=5)

btn_sleep = Button(btn_frame, text="Спать", command=pet.спать, font=("Arial", 10), bg="#673ab7", fg="white")
btn_sleep.grid(row=1, column=1, padx=5, pady=5)

btn_tetris = Button(btn_frame, text="Играть в Тетрис", command=tetriss, font=("Arial", 10), bg="#795548", fg="white")
btn_tetris.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

обновить()
set_idle_animation()
cikl()

root.mainloop()

