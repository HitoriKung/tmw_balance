import ttkbootstrap as tb
from ttkbootstrap.constants import *
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

            # Format balance
            balance = f"{int(balance_raw[:-2]):,}.{balance_raw[-2:]}"

            mobile_no = response_data['data']['mobile_no']
            updated_at = response_data['data']['updated_at']
            text_area.tag_configure("blue", foreground="blue")
            text_area.delete(1.0, tb.END)

            # Display balance in the text area
            text_area.insert(tb.END, f"ยอดเงินคงเหลือ: ", "normal")
            text_area.insert(tb.END, balance, "blue")
            text_area.insert(tb.END, f" บาท\nหมายเลขโทรศัพท์: {mobile_no}\nข้อมูลเมื่อ: {updated_at}", "normal")

            # Save balance to a file if the checkbox is selected
            if save_to_file_var.get():
                with open("balance.txt", "w") as file:
                    file.write(f"{balance}")

        else:
            messagebox.showerror("Error", "ไม่สามารถดึงข้อมูลได้ โปรดเช็คข้อมูลของท่านใหม่อีกครั้ง")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

root = tb.Window(themename="simplex")
root.title("เช็คยอดเงินจากทรูมันนี่วอลเล็ท")
root.geometry("500x260")

tb.Label(root, text="โทเคน:", font=("Arial", 12)).pack(pady=5)
token_entry = tb.Entry(root, width=50, show="*", font=("Arial", 12))
token_entry.pack(pady=5)

save_to_file_var = tb.BooleanVar()
save_to_file_checkbox = tb.Checkbutton(root, text="บันทึกยอดเงิน", variable=save_to_file_var, bootstyle=PRIMARY)
save_to_file_checkbox.pack(pady=5)

check_button = tb.Button(root, text="ตรวจสอบ", command=check_balance, bootstyle=SUCCESS)
check_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, width=60, height=15, font=("Arial", 12))
text_area.pack(pady=10)

root.mainloop()
