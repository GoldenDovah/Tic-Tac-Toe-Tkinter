import tkinter
from tkinter.constants import DISABLED, NORMAL
from PIL import ImageTk,Image
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def App():
    global root, playground_buttons
    root = tkinter.Tk()
    playground_buttons = []
    root.iconbitmap( default = resource_path("dev/tic-tac-toe.ico") )
    root.title("Tic-Tac-Toe")
    app_width = 2.45
    app_height = 1.4
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - ( screen_width/(app_width*2) )
    y = (screen_height/2) - ( screen_height/(app_height*2) )
    root.geometry('%dx%d+%d+%d' % ( int(screen_width/app_width), int(screen_height/app_height), x, y) )
    main_menu()
    root.mainloop()

def main_menu():
    global button_bot, button_player, canvas_main_menu
    frame_main_menu = tkinter.Frame(root, bg = '#616E7C' )
    frame_main_menu.pack( expand = True, fill = 'both' )
    for i in range(2):
        tkinter.Grid.rowconfigure(frame_main_menu, i, weight = 1)
        tkinter.Grid.columnconfigure(frame_main_menu, i, weight = 1)
    canvas_main_menu = tkinter.Canvas(frame_main_menu, bg = '#616E7C' )
    canvas_main_menu.grid( row = 0, columnspan = 2 )
    button_bot = tkinter.Button(frame_main_menu, text = "Play against bot", bg = '#7B8794', command = lambda: choose_symbol(frame_main_menu, 'bot') )
    button_bot.grid( row = 1, column = 0, sticky = 'EW', padx = 20, pady = 20 )
    button_player = tkinter.Button(frame_main_menu, text = "Play against player 2", bg = '#7B8794',\
    command = lambda: choose_symbol(frame_main_menu, 'player') )
    button_player.grid( row = 1, column = 1, sticky = 'EW', padx = 20, pady = 20 )
    frame_main_menu.bind('<Configure>', resize_main_menu )

def choose_symbol(frame_main_menu, gamemode):
    global label_choose_symbol, button_x, button_o
    frame_main_menu.pack_forget()
    frame_choose_symbol = tkinter.Frame(root, bg = '#616E7C' )
    frame_choose_symbol.pack( expand = True, fill = 'both' )
    for i in range(2):
        tkinter.Grid.rowconfigure(frame_choose_symbol, i, weight = 1)
        tkinter.Grid.columnconfigure(frame_choose_symbol, i, weight = 1)
    label_choose_symbol = tkinter.Label(frame_choose_symbol, text = 'Choose Symbol\nFor Player 1', bg = '#616E7C' )
    label_choose_symbol.grid( row = 0, columnspan = 2 )
    button_x = tkinter.Button(frame_choose_symbol, text = 'X', command = lambda: switch_play(0,frame_choose_symbol,frame_main_menu,'X',gamemode), fg = '#dc342e' )
    button_x.grid( row = 1, column = 0 )
    button_o = tkinter.Button(frame_choose_symbol, text = 'O', command = lambda: switch_play(1,frame_choose_symbol,frame_main_menu,'O',gamemode), fg = '#376cb6' )
    button_o.grid( row = 1, column = 1 )
    frame_choose_symbol.bind('<Configure>', resize_choose_symbol)

def resize_choose_symbol(e):
    font_size = int( (e.height + (e.width/3) )/40 )
    label_choose_symbol.configure( font = ('Helvetica',2*font_size) )
    button_x.configure( font = ('Arial Bold',4*font_size), bd = 4 )
    button_o.configure( font = ('Arial Bold',4*font_size), bd = 4 )

def switch_play( increment, frame_choose_symbol, frame_main_menu, choice, gamemode ):
    global clicks, player1_choice
    clicks = increment
    player1_choice = choice
    frame_choose_symbol.pack_forget()
    play(frame_main_menu, gamemode)

def play(frame_main_menu, gamemode):
    global frame_play, button_retry, button_back, frame_playground, clicks, frame_score, draw_label, player1_label, player2_label, opponent_choice
    if player1_choice == 'X':
        opponent_choice = 'O'
    else:
        opponent_choice = 'X'
    frame_play = tkinter.Frame(root, bg = '#616E7C' )
    frame_play.pack( expand = True, fill = 'both' )
    for i in range(2):
        tkinter.Grid.columnconfigure(frame_play, i, weight = 1)
    for i in range(3):
        tkinter.Grid.rowconfigure(frame_play, i, weight = 1)
    frame_playground = tkinter.Frame(frame_play, highlightbackground="white", highlightthickness = 2 )
    frame_playground.grid( row = 0, columnspan = 2, pady = 20 )
    frame_playground.grid_propagate(0)
    for i in range(3):
        tkinter.Grid.rowconfigure(frame_playground, i, weight = 1)
        tkinter.Grid.columnconfigure(frame_playground, i, weight = 1)
    j = k = 0
    playground_buttons.clear()
    for i in range(1,10):
        button_tic = tkinter.Button(frame_playground )
        if gamemode == 'player':
            button_tic.configure( command = lambda button_tic = button_tic: play_against_player_algorithm( button_tic ) )
        else:
            button_tic.configure( command = lambda button_tic = button_tic: play_against_bot_algorithm( button_tic ) )
        button_tic.grid( row = j, column = k )
        if i % 2 == 1:
            button_tic.configure( bg = '#29384d')
        else:
            button_tic.configure( bg = '#e6eded')
        playground_buttons.append( button_tic )
        k += 1
        if i % 3 == 0:
            j += 1
            k = 0
    frame_score = tkinter.Frame(frame_play, bg = '#616E7C' )
    frame_score.grid( row = 1, columnspan = 2, sticky = 'NSEW' )
    for i in range(3):
        tkinter.Grid.columnconfigure(frame_score, i, weight = 1)
    for i in range(2):
        tkinter.Grid.rowconfigure(frame_score, i, weight = 1)
    score_label = tkinter.Label(frame_score, text = 'Score', bg = '#616E7C')
    score_label.grid( row = 0, columnspan = 3 )
    player1_label = tkinter.Label(frame_score, text = 'Player 1:\t0', bg = '#616E7C')
    player1_label.grid( row = 1, column = 0 )
    draw_label = tkinter.Label(frame_score, text = 'Draw:\t0', bg = '#616E7C')
    draw_label.grid( row = 1, column = 1 )
    player2_label = tkinter.Label(frame_score, bg = '#616E7C')
    player2_label.grid( row = 1, column = 2 )
    if gamemode == 'player':
        player2_label.configure( text = 'Player 2:\t0' )
    else:
        player2_label.configure( text = 'Bot:\t0' )
    button_retry = tkinter.Button(frame_play, text = "Retry", bg = '#7B8794', command = play_retry )
    button_retry.grid( row = 2, column = 0, sticky = 'EW', padx = 20, pady = 20 )
    button_back = tkinter.Button(frame_play, text = "Back", bg = '#7B8794', \
    command = lambda: play_back(frame_play, frame_main_menu) )
    button_back.grid( row = 2, column = 1, sticky = 'EW', padx = 20, pady = 20 )
    frame_play.bind('<Configure>', resize_play )

def play_retry():
    global clicks
    if player1_choice == 'X':
        clicks = 0
    else:
        clicks = 1
    for button in playground_buttons:
        button.configure( text = '', state = NORMAL )

def shared_algorithm( button_tic ):
    global clicks
    if clicks % 2 == 0:
        button_tic.configure( text = 'X', disabledforeground = '#dc342e', state = DISABLED )
    else:
        button_tic.configure( text = 'O', disabledforeground = '#376cb6', state = DISABLED )
    clicks += 1
    if ( playground_buttons[0].cget('text') == playground_buttons[1].cget('text') == playground_buttons[2].cget('text') and\
    playground_buttons[0].cget('text') != '') :
        score_update( playground_buttons[0].cget('text') )
    elif ( playground_buttons[3].cget('text') == playground_buttons[4].cget('text') == playground_buttons[5].cget('text') and\
    playground_buttons[3].cget('text') != '') :
        score_update( playground_buttons[3].cget('text') )
    elif ( playground_buttons[6].cget('text') == playground_buttons[7].cget('text') == playground_buttons[8].cget('text') and\
    playground_buttons[6].cget('text') != '') :
        score_update( playground_buttons[6].cget('text') )
    elif ( playground_buttons[0].cget('text') == playground_buttons[3].cget('text') == playground_buttons[6].cget('text') and\
    playground_buttons[0].cget('text') != '') :
        score_update( playground_buttons[0].cget('text') )
    elif ( playground_buttons[1].cget('text') == playground_buttons[4].cget('text') == playground_buttons[7].cget('text') and\
    playground_buttons[1].cget('text') != '') :
        score_update( playground_buttons[1].cget('text') )
    elif ( playground_buttons[2].cget('text') == playground_buttons[5].cget('text') == playground_buttons[8].cget('text') and\
    playground_buttons[2].cget('text') != '') :
        score_update( playground_buttons[2].cget('text') )
    elif ( playground_buttons[0].cget('text') == playground_buttons[4].cget('text') == playground_buttons[8].cget('text') and\
    playground_buttons[0].cget('text') != '') :
        score_update( playground_buttons[0].cget('text') )
    elif ( playground_buttons[2].cget('text') == playground_buttons[4].cget('text') == playground_buttons[6].cget('text') and\
    playground_buttons[2].cget('text') != ''):
        score_update( playground_buttons[2].cget('text') )
    elif playground_buttons[0].cget('text') != '' and playground_buttons[1].cget('text') != '' and playground_buttons[2].cget('text') != ''\
    and playground_buttons[3].cget('text') != '' and playground_buttons[4].cget('text') != '' and playground_buttons[5].cget('text') != ''\
    and playground_buttons[6].cget('text') != '' and playground_buttons[7].cget('text') != '' and playground_buttons[8].cget('text') != '':
        score_update('draw')
    else:
        return 0
    return 1

enabled_buttons = []
def play_against_bot_algorithm( button_tic ):
    global clicks
    enabled_buttons.clear()
    game_done = shared_algorithm(button_tic)
    if game_done == 0:
        for i in range( len(playground_buttons) ):
            if playground_buttons[i].cget('state') == 'normal' :
                enabled_buttons.append( playground_buttons[i] )
        if opponent_choice == 'O':
            opponent_color = '#376cb6'
        else:
            opponent_color = '#dc342e'
        shared_algorithm( enabled_buttons[ random.randint(0, len(enabled_buttons) - 1) ] )

def play_against_player_algorithm( button_tic ):
    shared_algorithm(button_tic)

def score_update( winner ):
    if winner == 'draw':
        draw_text = draw_label.cget('text')
        draw_text = draw_text.split('\t')
        draw_label.configure( text = draw_text[0] + '\t' + str( int(draw_text[1]) + 1) )
    elif winner == player1_choice:
        player1_text = player1_label.cget('text')
        player1_text = player1_text.split('\t')
        player1_label.configure( text = player1_text[0] + '\t' + str( int(player1_text[1]) + 1) )
    else:
        player2_text = player2_label.cget('text')
        player2_text = player2_text.split('\t')
        player2_label.configure( text = player2_text[0] + '\t' + str( int(player2_text[1]) + 1) )
    for button in playground_buttons:
        button.configure( state = DISABLED, disabledforeground = 'gray' )

def resize_play(e):
    font_size = int( (e.height + (e.width/3) )/40 )
    frame_playground.configure( width = int(e.width/1.2), height = int(e.height/1.3) )
    frame_playground.grid_propagate(0)
    for button in playground_buttons:
        button.configure( width = int( e.width/(1.2*3) ), height = int(e.height/(1.3*3) ), font = ('Arial Bold',4*font_size) )
    for child in frame_score.winfo_children():
        child.configure( font = ('Helvetica',font_size//2) )
    button_retry.configure( font = ('Helvetica',font_size) )
    button_back.configure( font = ('Helvetica',font_size) )

def play_back(frame_play, frame_main_menu):
    frame_play.pack_forget()
    frame_main_menu.pack( expand = True, fill = 'both' )

def resize_main_menu(e):
    global image_main_menu
    font_size = int( (e.height + (e.width/3) )/40 )
    canvas_main_menu.configure( width = int(e.width/1.2), height = int(e.height/1.3) )
    image_main_menu = Image.open( resource_path("dev/tic-tac-toe main menu.png") )
    wpercent = (int(e.width/1.2)/float(image_main_menu.size[0]))
    hsize = int((float(image_main_menu.size[1])*float(wpercent)))
    image_main_menu = image_main_menu.resize((int(e.width/1.2),hsize), Image.ANTIALIAS)
    image_main_menu = ImageTk.PhotoImage( image_main_menu )
    canvas_main_menu.create_image( 0, 0, image = image_main_menu, anchor = 'nw' )
    canvas_main_menu.configure( height = hsize)
    button_bot.configure( font = ('Helvetica',font_size) )
    button_player.configure( font = ('Helvetica',font_size) )

if __name__ == "__main__":
    App()