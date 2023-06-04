import pygame as pg
import asyncio
import time
import sys

pg.init()
info = pg.display.Info()
win_width = info.current_w
win_height = info.current_h
win_dimension = (win_width, win_height)
boundary_size: int = 30 # how large the boundary is
win = pg.display.set_mode(win_dimension, pg.FULLSCREEN)
background_col = GREY = [128, 128, 128]
BLACK = [0,0,0]
name = ""
large_font = 72
screen = pg.display.set_mode((640, 480))
font = pg.font.Font(None, 32)
clock = pg.time.Clock()
input_box = pg.Rect(100, 100, 140, 32)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
name = ''
exit = False


def is_valid(num):
    if (num >= 48 and num <= 57) or (num >= 97 and num <= 122) or (num == 46) or (num == 32):
        return True
    else:
        return False

def input_text(): 
    return "Please enter the requested information. Then press Enter or Return to continue. Press ESC to exit or inform the observer of your decision. \n\n"

def draw_boundaries(display=win):
    #pg.draw.rect(display, BLACK, pg.Rect(win_width - boundary_size, 0, boundary_size, win_height - boundary_size)) # right
    pg.draw.rect(display, BLACK, pg.Rect(win_width - boundary_size, 0, boundary_size, win_height)) # right
    pg.draw.rect(display, BLACK, pg.Rect(0, 0, boundary_size, win_height)) # left
    pg.draw.rect(display, BLACK, pg.Rect(0, 0, win_width, boundary_size)) # top
    pg.draw.rect(display, BLACK, pg.Rect(0, win_height - boundary_size, win_width, boundary_size)) # bottom
    #pg.display.update()


def multi_line_message(text, textsize, pos=((win_width-(win_width/10)), win_height), color=BLACK, display=win):
    """function to split text message to multiple lines and blit to display window."""
    # -- Make a list of strings split by the "\n", and each list contains words of that line as elements.
    #font = pg.font.SysFont("arial", textsize)
    #words = [word.split(" ") for word in text.splitlines()]
    print(f'{text=} {textsize=} {pos=} {color=}')
    
    too_big = True 
    final_text_x = 0

    # -- Get the width required to render an empty space
    #space_w = font.size(" ")[0]  # .size method returns dimension in width and height. [0] gets the width
    #max_w, max_h = ((win_width-(win_width/10)), win_height)
    #text_x, text_y = pos

    while too_big == True:
        font = pg.font.SysFont("arial", textsize)
        words = [word.split(" ") for word in text.splitlines()]
        space_w = font.size(" ")[0]  # .size method returns dimension in width and height. [0] gets the width
        max_w, max_h = ((win_width-(win_width/10)), win_height)
        text_x, text_y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, True, color)  # get surface for each word
                word_w, word_h = word_surface.get_size()  # get size for each word
                if text_x + word_w >= max_w:  # if the a word exceeds the line length limit
                    text_x = (win_width/10)  # reset the x
                    text_y += word_h  # start a new row
                display.blit(word_surface, (text_x, text_y))  # blit the text onto surface according to pos
                text_x += word_w + space_w  # force a space between each word
            final_text_x = text_x
            text_x = (win_width/10)  # reset the x
            text_y += word_h  # start a new row
        if text_y <= win_height - boundary_size - 20:
            too_big = False
        else: 
            textsize -= 3 # if too big for display then shrink the textsize and try again
            win.fill(background_col)
        draw_boundaries()
    pg.display.flip()
    #assert 1 == 0 This works


async def main():
    
    
    while True:
        print(user_info("hi! "))
        await asyncio.sleep(0)

def user_info(type):

    pg.mouse.set_visible(False)
    pg.display.flip()
    exit = False
    text = ''
    done = False
    name = ''
    while True:
        for event in pg.event.get():
            #name = name + str(pg.K_RETURN) this showed us that the code really was 13
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_ESCAPE or event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    exit_key = event.key
                    exit = True
                    #assert 1 == 9 it hits here. this means enter is recognized

                elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                    name = name[:-1] #delete last letter
                #elif is_valid(event.key):
                else:
                    if (pg.key.get_mods() & pg.KMOD_CAPS) or (pg.key.get_mods() & pg.KMOD_SHIFT):
                        name = name + chr(event.key).upper()
                    else:
                        name = name + str(event.key)
                        
        if exit == True:
            multi_line_message("leaving now!" + type + name, large_font, ((win_width - (win_width / 10)), 120))
            time.sleep(2)
            break


        win.fill(background_col) #display input
        multi_line_message(input_text() + type + name, large_font, ((win_width - (win_width / 10)), 120))
        #assert 1==0 #reaches here and interesting things happen!

    if exit_key == pg.K_RETURN or exit_key == pg.K_KP_ENTER:
        #assert 1 == 0 #it doesn't reach here
        return name # If the user enters then we proceed with game
    else:
       pg.quit()
       sys.exit()


asyncio.run(main())