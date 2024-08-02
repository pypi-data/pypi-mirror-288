import tkinter as tk  
from tkinter import messagebox  
  
# 定义一个函数，该函数在点击按钮时被调用  
def on_button_click():  
    # 从输入框中获取文本  
    user_input = entry.get()  
    # 将获取到的文本显示在标签上  
    label.config(text=f"你输入的是: {user_input}")  
  
# 创建主窗口  
root = tk.Tk()  
root.title("Tkinter 小案例")  
  
# 设置窗口大小  
root.geometry("300x150")  
  
# 创建一个标签  
label = tk.Label(root, text="请输入一些文本:", font=("Arial", 12))  
label.pack(pady=10)  # 使用pack布局管理器，并添加垂直填充  
  
# 创建一个输入框  
entry = tk.Entry(root, font=("Arial", 12), width=30)  
entry.pack()  
  
# 创建一个按钮，点击时调用on_button_click函数  
button = tk.Button(root, text="显示", command=on_button_click)  
button.pack(pady=10)  # 添加垂直填充  
  
# 进入主事件循环  
root.mainloop()  