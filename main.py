from pyautogui import getAllWindows
from MonitorHandler import MonitorHandler
from pygetwindow import getWindowsWithTitle
from win32gui import EnumWindows, IsWindowVisible, GetWindowText, MoveWindow

class changables():
    def __init__(self):
        self.padding = 5
        self.mode = "Debug"

def resizeWindow(title: str, dimensions: tuple):
    window = getWindowsWithTitle(title)[0]
    window.size = dimensions

def winPosChange(window, dimensions: tuple, positions: tuple):
    #we want only the start position of x and y
    MoveWindow(window._hWnd, positions[0], positions[2], dimensions[0], dimensions[1], True)

def windowAppendixHandler():
    allWindows = getAllWindows() #gives list of every window as win32window object
    windowsList = []
    count = 0
    for window in allWindows:
        if window.left != 0 and window.top !=0 and window.width !=0 and window.height !=0 and window.title != "" and not (window.title == 'Ayarlar'):
            windowsList.append(window)
            count += 1

    if changables().mode == "Debug":
        for window in windowsList:
            print(window)

    return windowsList, count

def winCountTemplateMatcher(count: int):
    if count == 0:
        startupMode()
    if count == 2:
        return 'AxB'
    if count > 2:
        return None

def winHandler(template: str, windowList: list, monitorHandler: MonitorHandler):
    padding = changables().padding
    if template == 'AxB':
        A = None
        B = None
        win1 = windowList[0] #make this an object
        win2 = windowList[1] #this too you idiot
        if win1.left < win2.left: #left='0' is left on the screen and vv.
            A = win1
            B = win2
        else:
            A = win2
            B = win1
        win1pos = (0+padding, int((monitorHandler.MonitorWorkableX/2)-padding), 0+padding, monitorHandler.MonitorWorkableY-padding) # (xStart -> 0+padding, xEnd -> (usableMonX/2)-padding, yStart -> 0+padding, yEnd -> usableMonY-padding)
        win2pos = (int((monitorHandler.MonitorWorkableX/2)+padding), monitorHandler.MonitorWorkableX-padding, 0+padding, monitorHandler.MonitorWorkableY-padding) #no explaining here cry lol
        win1res = (win1pos[1]-win1pos[0], win1pos[3]-win1pos[2]) #(xEnd-xStart, yEnd-yStart)
        win2res = (win2pos[1]-win2pos[0], win2pos[3]-win2pos[2]) #thinking again they should be equal
        if win1res != win2res:
            raise Exception('Error1WH')
        
        # Resize windows
        resizeWindow(win1.title, win1res)
        resizeWindow(win2.title, win2res)
        # Chnage the positions
        winPosChange(A, win1res, win1pos)
        winPosChange(B, win2res, win2pos)

        if changables().mode == "Debug":
            print("Window 1 position: {}\nWindow 2 position: {}".format(win1pos, win2pos))
            print("Window 1 resolution: {}\nWindow 2 resulotion: {}".format(win1res, win2res))

def startupMode():
    None

def main():
    monitorHandler = MonitorHandler()
    monitorHandler.setup()
    print(f'Usable monitor area X: {monitorHandler.MonitorWorkableX}\nUsable monitor area Y: {monitorHandler.MonitorWorkableY}')
    windowsList, count = windowAppendixHandler()
    print(f'found {count} windows appearing on the screen')
    print(winCountTemplateMatcher(count))
    winHandler(winCountTemplateMatcher(count=count), windowsList, monitorHandler)

main()