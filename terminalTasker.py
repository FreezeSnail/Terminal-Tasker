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

def jobMenu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
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

    i = 0
    for job in jobs.getJobList():
        output = "Company: " + str(job['Company'])  + " Posistion: " + str(job['Posistion']) + " Date: " + str(job['Date'])+ " Status: "  + str(job['Status'])

        stdscr.addstr(cursor_y + i, cursor_x, output)
        i += 1

def mainMenu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
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

        # Declaration of strings
    title = "Curses example"[:width-1]
    subtitle = "Written by Clay McLeod"[:width-1]
    keystr = "Last key pressed: {}".format(k)[:width-1]

    if k == 0:
        keystr = "No key press detected..."[:width-1]

    #jobModule
    stdscr.addstr(str(jobs.print()))

        # Centering calculations
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
    start_y = int((height // 2) - 2)

        # Rendering some text
    whstr = "Width: {}, Height: {}".format(width, height)
    stdscr.addstr(0, 0, whstr, curses.color_pair(1))

    # Rendering title
    stdscr.addstr(start_y, start_x_title, title)

        # Print rest of text
    stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
    stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        #jobModule
        
    stdscr.move(cursor_y, cursor_x)
        
    



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


        if(k == ord('j')):
            menuMode = MENU.JOB
        elif(k == ord('m')):
            menuMode = MENU.MAIN

        #switchcase for modes
        if (menuMode == MENU.MAIN):
            curses.wrapper(mainMenu)
        elif (menuMode == MENU.JOB):
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