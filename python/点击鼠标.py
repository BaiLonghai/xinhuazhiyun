import pyautogui

# 定义一个全局变量来存储鼠标坐标
mouse_pos = None


def on_press(key):
    """
    在按下 F9 键时，记录当前鼠标坐标；在按下 F10 键时，点击之前记录的鼠标坐标。

    参数:
        key (keyboard.Key): 按下的键。

    返回值:
        无。
    """
    global mouse_pos
    try:
        # 在按下 F9 键时，记录当前鼠标坐标
        if key == keyboard.Key.f9:
            mouse_pos = pyautogui.position()
            print(f"Mouse position recorded: {mouse_pos}")
        # 在按下 F10 键时，点击之前记录的鼠标坐标
        elif key == keyboard.Key.f10:
            if mouse_pos is not None:
                pyautogui.click(mouse_pos)
                print(f"Clicked at {mouse_pos}")
            else:
                print("No mouse position recorded")
    except Exception as e:
        print(f"An error occurred: {e}")


# 创建一个 "keyboard" 对象并监听键盘事件
import keyboard

keyboard.on_press(on_press)

# 保持运行状态，直到按下 "esc" 键
print("Press 'ESC' to quit")
keyboard.wait("esc")
