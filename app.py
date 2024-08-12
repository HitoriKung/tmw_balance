import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

def check_balance():
    token = token_entry.get()
    headers = {
        'Authorization': f'Bearer {token}',
    }

    try:
        response = requests.get('https://apis.truemoneyservices.com/account/v1/balance', headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get('status') == 'ok':
            balance_raw = response_data['data']['balance']

            balance = f"{int(balance_raw[:-2]):,}.{balance_raw[-2:]}"

            mobile_no = response_data['data']['mobile_no']
            updated_at = response_data['data']['updated_at']
            text_area.tag_configure("blue", foreground="blue")
            text_area.delete(1.0, tk.END)

            text_area.insert(tk.END, f"ยอดเงินคงเหลือ: ", "normal")
            text_area.insert(tk.END, balance, "blue")
            text_area.insert(tk.END, f" บาท\nหมายเลขโทรศัพท์: {mobile_no}\nข้อมูลเมื่อ: {updated_at}", "normal")
        else:
            messagebox.showerror("Error", "ไม่สามารถดึงข้อมูลได้ โปรดเช็คข้อมูลของท่านใหม่อีกครั้ง")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("เช็คยอดเงินจากทรูมันนี่วอลเล็ท")

tk.Label(root, text="โทเคน:").pack(pady=5)
token_entry = tk.Entry(root, width=50, show="*")
token_entry.pack(pady=5)

check_button = tk.Button(root, text="ตรวจสอบ", command=check_balance)
check_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, width=60, height=15)
text_area.pack(pady=10)

root.mainloop()