import customtkinter as ctk

root = ctk.CTk()

root.geometry("750x500")
root.title("Prayer App")
root.iconbitmap("logo.ico")

title_label = ctk.CTkLabel(root, text="Prayer App", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(padx = 10, pady = (40,20))

scrollableInterface = ctk.CTkScrollableFrame(root, width=500, height=400)
scrollableInterface.pack(padx = 10, pady = 10)

root.mainloop()