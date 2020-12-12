import os
from tkinter import *

root = Tk()
root.title("제목 없음 - Windows 메모장")
root.geometry("640x480")

filename = "mynote.txt"

# 메뉴
menu = Menu(root)


def open_file():
    if os.path.isfile(filename):  # 파일 있으면 True, 없으면 False
        with open(filename, 'r', encoding="utf8") as file:
            text.delete("1.0", END)  # 텍스트 위젯 본문 삭제
            text.insert(END, file.read())  # 파일 내용을 본문에 입력


def save_file():
    with open(filename, 'w', encoding="utf8") as file:
        file.write(text.get("1.0", END))    # 모든 내용을 가져와서 저장


menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="열기", command=open_file)
menu_file.add_command(label="저장", command=save_file)
menu_file.add_separator()
menu_file.add_command(label="끝내기", command=root.quit)
menu.add_cascade(label="파일", menu=menu_file)
menu.add_cascade(label="편집")
menu.add_cascade(label="서식")
menu.add_cascade(label="보기")
menu.add_cascade(label="도움말")

scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")


text = Text(root, yscrollcommand=scrollbar.set)
text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=text.yview)


root.config(menu=menu)
root.mainloop()
