import sys,os
import curses
from enum import Enum


class MENU(Enum):
    MAIN = 0
    JOB = 1



from jobTracker import JobModule
jobs = JobModule()


menuMode = MENU.MAIN

def quit(stdscr):
    jobs.save()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def menuSelect(k):
    if(k == ord('j')):
        return 0,  MENU.JOB
    elif(k == ord('m')):
        return 0, MENU.MAIN

    return 1, 0


menu = ["test1", "test2"]
def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()



def jobMenu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    height, width = stdscr.getmaxyx()

    while(1):
        stdscr.clear()
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)
        print_menu(stdscr, cursor_y)

        i = 0
        for job in jobs.getJobList():
            output = "Company: " + str(job['Company'])  + " Posistion: " + str(job['Posistion']) + " Date: " + str(job['Date'])+ " Status: "  + str(job['Status'])

            stdscr.addstr(cursor_y + i, cursor_x, output)
            i += 1

        stdscr.addstr(cursor_y + i, cursor_x, str(cursor_y))

        _, menuMode = menuSelect(k)

        #switchcase for modes
        if (menuMode == MENU.MAIN):
            break

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        

def mainMenu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    height, width = stdscr.getmaxyx()

    while(menuSelect(k)):
        stdscr.clear()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

          
            
        stdscr.move(cursor_y, cursor_x)

        _, menuMode = menuSelect(k)

        #switchcase for modes
        if (menuMode == MENU.MAIN):
            curses.wrapper(mainMenu)
        elif (menuMode == MENU.JOB):
            curses.wrapper(jobMenu)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        
    



def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    global menuMode
    # Clear and refresh the screen for a blank canvas
    stdscr.erase()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)


        _, menuMode = menuSelect(k)

        #switchcase for modes
        
        if (menuMode == MENU.JOB):
            curses.wrapper(jobMenu)

        # Centering calculations 
        start_y = int((height // 2) - 2)
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        
        #Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    curses.wrapper(quit)


def main():
    
    jobs.load()
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()