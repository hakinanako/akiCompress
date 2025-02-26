import customtkinter as ctk
import tkinter.filedialog as filedialog

from compressor.Compressor import Compression

def compress_file():
    input_path = filedialog.askopenfilename(title="选择要压缩的文件")
    if not input_path:
        return
    output_path = filedialog.asksaveasfilename(title="保存压缩后的文件为")
    if not output_path:
        return
    try:
        Compression.compress_file(input_path, output_path)
        result_label.configure(text="压缩成功！")
    except Exception as e:
        result_label.configure(text=f"压缩失败：{str(e)}")

def decompress_file():
    input_path = filedialog.askopenfilename(title="选择要解压的文件")
    if not input_path:
        return
    output_path = filedialog.asksaveasfilename(title="保存解压后的文件为")
    if not output_path:
        return
    try:
        Compression.decompress_file(input_path, output_path)
        result_label.configure(text="解压成功！")
    except Exception as e:
        result_label.configure(text=f"解压失败：{str(e)}")

app = ctk.CTk()

app.geometry("300x150")

compress_button = ctk.CTkButton(master=app, text="压缩文件", command=compress_file, width=200)
compress_button.pack(pady=20)

decompress_button = ctk.CTkButton(master=app, text="解压文件", command=decompress_file, width=200)
decompress_button.pack(pady=20)

result_label = ctk.CTkLabel(master=app, text="", width=300)
result_label.pack(pady=10)

app.mainloop()
