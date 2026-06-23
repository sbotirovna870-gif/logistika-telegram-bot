import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import math
import pandas as pd
from datetime import datetime
import requests  # Telegram bilan ishlash uchun kutubxona

# Bitta seans davomida qilingan barcha hisob-kitoblarni saqlash uchun ro'yxat
calculation_history = []

# --- TELEGRAM SOZLAMALARI ---
# Bu yerga @BotFather va @userinfobot dan olgan ma'lumotlaringizni yozasiz
BOT_TOKEN = "token"  # Masalan: "123456:ABCdefGhI..."
CHAT_ID = "id"  # Masalan: "807669797"


# --- Telegramga xabar yuborish funksiyasi ---
def send_to_telegram(text):
    if BOT_TOKEN == "BU_YERGA_TOKEN_YOZING" or CHAT_ID == "BU_YERGA_ID_YOZING":
        messagebox.showwarning("Sozlanmagan",
                               "Telegram Bot Token yoki Chat ID kiritilmagan!\nKodni ichidan ularni to'g'rilang.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


# --- Hisoblash funksiyasi ---
def calculate_trucks():
    try:
        total_weight = float(weight_entry.get())
        truck_capacity = float(capacity_entry.get())

        if truck_capacity <= 0:
            messagebox.showerror("Xato", "Mashina sig'imi 0 dan katta bo'lishi kerak!")
            return

        trucks_needed = math.ceil(total_weight / truck_capacity)
        total_capacity = trucks_needed * truck_capacity
        empty_space = total_capacity - total_weight

        result_text = (f"Jami kerakli mashinalar: {trucks_needed} ta\n"
                       f"Oxirgi mashinadagi bo'sh joy: {empty_space} kg")
        result_label.config(text=result_text, fg="green")

        calculation_history.append({
            "Vaqt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Jami yuk (kg)": total_weight,
            "Mashina sig'imi (kg)": truck_capacity,
            "Kerakli mashinalar": trucks_needed,
            "Bo'sh joy (kg)": empty_space
        })

    except ValueError:
        messagebox.showerror("Xato", "Iltimos, og'irlik va sig'im uchun faqat raqam kiriting!")


# --- Excelga eksport qilish funksiyasi ---
def export_to_excel():
    if not calculation_history:
        messagebox.showwarning("Ogohlantirish", "Eksport qilish uchun ma'lumot yo'q!")
        return
    try:
        df = pd.DataFrame(calculation_history)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel fayllar", "*.xlsx")],
            title="Hisobotni saqlash"
        )
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Muvaffaqiyat", f"Hisobot Excelga saqlandi!")
    except Exception as e:
        messagebox.showerror("Xato", f"Xatolik: {e}")


# --- Telegram tugmasi bosilgandagi funksiya ---
def send_report_click():
    if not calculation_history:
        messagebox.showwarning("Ogohlantirish", "Yuborish uchun oldin hisob-kitob qiling!")
        return

    # Oxirgi qilingan hisob-kitobni olamiz
    last_calc = calculation_history[-1]

    # Xatolikni oldini olish uchun qiymatlarni alohida o'zgaruvchilarga olamiz
    vaqt = last_calc['Vaqt']
    jami_yuk = last_calc['Jami yuk (kg)']
    sigim = last_calc["Mashina sig'imi (kg)"]
    kerakli_mashinalar = last_calc['Kerakli mashinalar']
    bosh_joy = last_calc["Bo'sh joy (kg)"]

    # Telegram xabari matni (chiroyli formatda)
    report_text = (
        f"🚚 *YANGI LOGISTIKA HISOBOTI*\n\n"
        f"📅 *Vaqt:* {vaqt}\n"
        f"📦 *Jami yuk:* {jami_yuk} kg\n"
        f"🚛 *Mashina sig'imi:* {sigim} kg\n"
        f"🔢 *Kerakli mashinalar:* {kerakli_mashinalar} ta\n"
        f"⚠️ *Bo'sh joy:* {bosh_joy} kg"
    )

    if send_to_telegram(report_text):
        messagebox.showinfo("Muvaffaqiyat", "Hisobot Telegramga muvaffaqiyatli yuborildi! 🚀")
    else:
        messagebox.showerror("Xato",
                             "Telegramga yuborishda xatolik yuz berdi!\nSozlamalarni yoki internetni tekshiring.")


# --- Interfeys (UI) QISMI ---
root = tk.Tk()
root.title("Logistika Optimizatori")
root.geometry("450x520")
root.configure(padx=20, pady=20)

title_label = tk.Label(root, text="Yuklarni Taqsimlash tizimi", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

tk.Label(root, text="Jami yuk og'irligini kiriting (kg):", font=("Arial", 10)).pack(anchor="w")
weight_entry = tk.Entry(root, width=35, font=("Arial", 12))
weight_entry.pack(pady=5)

tk.Label(root, text="Bitta mashina sig'imini kiriting (kg):", font=("Arial", 10)).pack(anchor="w")
capacity_entry = tk.Entry(root, width=35, font=("Arial", 12))
capacity_entry.pack(pady=5)

# Tugmalar
calc_button = tk.Button(root, text="Hisoblash", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=25,
                        command=calculate_trucks)
calc_button.pack(pady=10)

excel_button = tk.Button(root, text="Excelga saqlash", bg="#217346", fg="white", font=("Arial", 11, "bold"), width=25,
                         command=export_to_excel)
excel_button.pack(pady=5)

telegram_button = tk.Button(root, text="Telegramga yuborish ✈️", bg="#0088cc", fg="white", font=("Arial", 11, "bold"),
                            width=25, command=send_report_click)
telegram_button.pack(pady=5)

result_label = tk.Label(root, text="Natija bu yerda chiqadi", font=("Arial", 12, "bold"), fg="blue")
result_label.pack(pady=15)

# Oynani ochiq ushlab turuvchi asosiy buyruq (sizda shu o'chib ketgan edi)
root.mainloop()