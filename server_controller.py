import pyautogui
import time
import pywinauto

class ServerController:
    def stop_program(self, name):
        if(name == '1'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 788))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))

        if(name == '2'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 813))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))

        if (name == '3'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 840))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))


        if (name == '5'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 880))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))


        if (name == '6'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 903))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))
        
        if (name == '7'):
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 928))
            pywinauto.keyboard.send_keys('^c')
            pywinauto.mouse.click(button='left', coords=(1683, 760))
            pywinauto.mouse.click(button='left', coords=(1512, 863))




    def start_program(self, name):
        if(name == '1'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 788)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)

        if(name == '2'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 813)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)

        if (name == '3'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 840)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)
        
        if (name == '5'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 880)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)

        if (name == '6'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 903)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)
        
        if (name == '7'):
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 928)
            pyautogui.hotkey('up')
            pyautogui.hotkey('enter')
            pyautogui.click(1683, 760)
            pyautogui.click(1512, 863)