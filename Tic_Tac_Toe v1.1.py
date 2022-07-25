from tkinter import *
from tkinter.constants import DISABLED, NORMAL
from PIL import ImageTk,Image
import random
import sys
import os
import socket
import threading
import urllib.request
from time import sleep


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.server_port = 0
        self.opponent_retry = False
        self.player_retry = False
        self.winner = ''
        self.playground_buttons = []
        self.enabled_buttons = []
        self.iconbitmap( default = resource_path("dev/tic-tac-toe.ico") )
        self.title("Tic-Tac-Toe")
        self.app_width = 2.1
        self.app_height = 1.3
        self.main_menu()
        self.center(self)
        self.mainloop()

    def center(self, win):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width/2) - ( screen_width/(win.app_width*2) )
        y = (screen_height/2) - ( screen_height/(win.app_height*2) )
        win.geometry('%dx%d+%d+%d' % ( int(screen_width/win.app_width), int(screen_height/win.app_height), x, y) )
    
    def main_menu(self):
        self.frame_menu = Frame(self, bg = '#616E7C' )
        self.frame_menu.pack( expand = True, fill = 'both' )
        for i in range(2):
            Grid.rowconfigure(self.frame_menu, i, weight = 1)
        for i in range(4):
            Grid.columnconfigure(self.frame_menu, i, weight = 1)
        self.canvas_menu = Canvas(self.frame_menu, bg = '#616E7C' )
        self.canvas_menu.grid( row = 0, columnspan = 4 )
        self.button_bot = Button(self.frame_menu, text = "Play Against Bot", bg = '#7B8794', 
            command = lambda: self.choose_symbol('bot'), activebackground = '#7B87B4')
        self.button_bot.grid( row = 1, column = 0, sticky = 'EW', padx = 10, pady = 10 )
        self.button_local = Button(self.frame_menu, text = "Play Locally", bg = '#7B8794',
        command = lambda: self.choose_symbol('player'), activebackground = '#7B87B4')
        self.button_local.grid( row = 1, column = 1, sticky = 'EW', padx = 10, pady = 10 )
        self.button_online = Button(self.frame_menu, text = "Play Online", bg = '#7B8794',
        command = self.play_online, activebackground = '#7B87B4')
        self.button_online.grid( row = 1, column = 2, sticky = 'EW', padx = 10, pady = 10 )
        self.button_lan = Button(self.frame_menu, text = "Play On LAN", bg = '#7B8794',
        command = self.play_lan, activebackground = '#7B87B4')
        self.button_lan.grid( row = 1, column = 3, sticky = 'EW', padx = 10, pady = 10 )
        self.frame_menu.bind('<Configure>', self.resize_main_menu )


    def play_lan(self):
        self.insert_username()


    def clientLAN_connect(self):
        while True:
            try:
                self.client.connect(('127.0.0.1', self.client_port))
                print(f"CLIENT LAN CONNECTED WITH {self.client_port}")
                self.opponent_username = self.client.recv(1024).decode()
                break
            except Exception as e:
                print(f"LAN: {e}")
                if e.__str__() == "[WinError 10038] An operation was attempted on something that is not a socket":
                    print(f"LAN: No Connection established, disconnecting...")
                    break


    def serverLAN_connect(self):
        self.server_port = 50001
        self.client_port = 50002
        self.opponent_username = ''
        try:
            self.server.bind(('', self.server_port))
            self.server.listen(5)
            threading.Thread(target = self.clientLAN_connect).start()
            self.sender, addr = self.server.accept()
        except Exception as e:
            print(e)
            self.server_port, self.client_port = self.client_port, self.server_port
            self.server.bind(('', self.server_port))
            self.server.listen(5)
            threading.Thread(target = self.clientLAN_connect).start()
            self.sender, addr = self.server.accept()
        print(f"SERVER LAN CONNECTED WITH {self.server_port}")
        self.sender.send(self.username.encode())
        while not self.opponent_username:
            pass
        self.after_cancel(self.waiting_id)
        self.window_connect.destroy()
        self.play("LAN")


    def play_online(self):
        for child in self.winfo_children():
            child.pack_forget()
        self.frame_online = Frame(self, bg = '#616E7C')
        self.frame_online.pack( expand = True, fill = 'both')
        for i in range(2):
            Grid.columnconfigure(self.frame_online, i, weight = 1)
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        self.label_ip = Label(self.frame_online, text = f"Public IP: {external_ip}", bg = '#616E7C')
        self.label_ip.grid(row = 0, columnspan = 2, pady = 20 )
        frame = Frame(self.frame_online, bg = '#616E7C')
        frame.grid(row = 1, columnspan = 2)
        Grid.rowconfigure(self.frame_online, 1, weight = 1)
        self.label_host = Label(frame, text = "Opponent IP:", bg = '#616E7C')
        self.label_host.grid(row = 0, column = 0, padx = 5, pady = 5 )
        self.entry_host = Entry(frame)
        self.entry_host.grid(row = 0, column = 1, padx = 5, pady = 5 )
        self.label_port = Label(frame, text = "Port:", bg = '#616E7C')
        self.label_port.grid(row = 1, column = 0, padx = 5, pady = 5 )
        self.entry_port = Entry(frame)
        self.entry_port.grid(row = 1, column = 1, padx = 5, pady = 5 )
        self.label_username = Label(frame, text = "Username:", bg = '#616E7C')
        self.label_username.grid(row = 2, column = 0, padx = 5, pady = 5 )
        self.entry_username = Entry(frame)
        self.entry_username.grid(row = 2, column = 1, padx = 5, pady = 5 )
        self.button_connect = Button(self.frame_online, text = "Connect", bg = '#7B8794', command = self.connect, activebackground = '#7B87B4')
        self.button_connect.grid(row = 2, column = 0, padx = 20, pady = 20, sticky = 'EW')
        self.button_back = Button(self.frame_online, text = "Back", bg = '#7B8794', command = self.back, activebackground = '#7B87B4')
        self.button_back.grid( row = 2, column = 1, padx = 20, pady = 20, sticky = 'EW')
        self.frame_online.bind('<Configure>', self.resize_online )


    def confirm_name(self, frame):
        self.username = self.entry_username.get()
        for child in frame.winfo_children():
            child.grid_forget()
        self.server = socket.socket()
        self.client = socket.socket()
        threading.Thread(target = self.serverLAN_connect).start()
        self.insert_wait(frame)


    def insert_username(self):
        self.window_connect = Toplevel()
        self.window_connect.app_width = 4
        self.window_connect.app_height = 5
        frame = Frame(self.window_connect, bg = '#616E7C')
        frame.pack(expand = True, fill = 'both')
        label_username = Label(frame, text = "Username: ", bg = '#616E7C', font = ('Helvetica', 19))
        label_username.grid(row = 0, column = 0, padx = (30,5), pady = 20)
        self.entry_username = Entry(frame, font = ('Helvetica', 19), width = 12)
        self.entry_username.focus_force()
        self.entry_username.grid(row = 0, column = 1, padx = 5, pady = 20 )
        btn = Button(frame, text = "Confirm", command = lambda: self.confirm_name(frame), bg = '#7B8794', activebackground = '#7B87B4', font = ('Helvetica', 19))
        btn.grid(row = 1, columnspan = 2, column = 0, padx = 30, pady = 20)
        self.center(self.window_connect)

    def insert_wait(self, frame):
        self.label_wait = Label(frame, text = "Waiting On Opponent.", bg = '#616E7C', font = ('Helvetica', 19))
        self.label_wait.grid(row = 0, column = 0, padx = 30, pady = 20)
        self.waiting_id = self.after(500, self.waiting)
        btn = Button(frame, text = "Leave", command = self.stop_connection, bg = '#7B8794', activebackground = '#7B87B4', font = ('Helvetica', 19))
        btn.grid(row = 1, column = 0, padx = 30, pady = 20)
        Grid.columnconfigure(frame, 0, weight = 1)
        self.window_connect.protocol( "WM_DELETE_WINDOW" , self.stop_connection )
        #self.center(self.window_connect)


    def connect(self):
        self.server = socket.socket()
        self.client = socket.socket()
        #receive.recv(2048)
        self.opponent_ip = self.entry_host.get()
        self.port = int(self.entry_port.get())
        self.username = self.entry_username.get()
        threading.Thread(target = self.client_connect).start()
        threading.Thread(target = self.server_connect).start()
        self.insert_username()

    
    def waiting(self):
        try:
            if self.label_wait['text'] == "Waiting On Opponent." or self.label_wait['text'] == "Waiting On Opponent..":
                self.label_wait['text'] += '.'
            else:
                self.label_wait['text'] = "Waiting On Opponent."
            self.after(500, self.waiting)
        except Exception as e:
            print(e)
            self.update_idletasks()


    def stop_connection(self):
        self.server.close()
        self.client.close()
        self.after_cancel(self.waiting_id)
        self.window_connect.destroy()


    def server_connect(self):
        self.server.bind(('', self.port))        
        self.server.listen(2)
        while True:
            c, addr = self.server.accept()
            print("SERVER CONNECTED!!!")


    def client_connect(self):
        while True:
            try:
                self.client.connect((self.opponent_ip, self.port))
                print("CLIENT CONNECTED!!!")
            except Exception as e:
                print(e)
                if e.__str__() == '[WinError 10038] An operation was attempted on something that is not a socket':
                    break
                sleep(1)

    
    def resize_online(self, e):
        font_size = int( (e.height + (e.width/3) )/40)
        self.label_ip.configure( font = ('Helvetica', font_size))
        self.label_host.configure( font = ('Helvetica', font_size))
        self.entry_host.configure( font = ('Helvetica', font_size))
        self.label_port.configure( font = ('Helvetica', font_size))
        self.entry_port.configure( font = ('Helvetica', font_size))
        self.label_username.configure( font = ('Helvetica', font_size))
        self.entry_username.configure( font = ('Helvetica', font_size))
        self.button_connect.configure( font = ('Helvetica', font_size))
        self.button_back.configure( font = ('Helvetica', font_size))


    def resize_main_menu(self, e):
        font_size = int( (e.height + (e.width/3) )/60 )
        self.canvas_menu.configure( width = int(e.width/1.4), height = int(e.height/1.5) )
        self.image_menu = Image.open( resource_path("dev/tic-tac-toe main menu.png") )
        wpercent = (int(e.width/1.4)/float(self.image_menu.size[0]))
        hsize = int((float(self.image_menu.size[1])*float(wpercent)))
        self.image_menu = self.image_menu.resize((int(e.width/1.4),hsize), Image.ANTIALIAS)
        self.image_menu = ImageTk.PhotoImage( self.image_menu )
        self.canvas_menu.create_image( 0, 0, image = self.image_menu, anchor = 'nw' )
        self.canvas_menu.configure( height = hsize)
        self.button_bot.configure( font = ('Helvetica',font_size) )
        self.button_local.configure( font = ('Helvetica',font_size) )
        self.button_online.configure( font = ('Helvetica',font_size) )
        self.button_lan.configure( font = ('Helvetica',font_size) )


    def choose_symbol(self, gamemode):
        self.frame_menu.pack_forget()
        self.frame_symbol = Frame(self, bg = '#616E7C' )
        self.frame_symbol.pack( expand = True, fill = 'both' )
        for i in range(2):
            Grid.rowconfigure(self.frame_symbol, i, weight = 1)
            Grid.columnconfigure(self.frame_symbol, i, weight = 1)
        self.label_choose_symbol = Label(self.frame_symbol, text = 'Choose Symbol\nFor Player 1', bg = '#616E7C' )
        self.label_choose_symbol.grid( row = 0, columnspan = 2 )
        self.button_x = Button(self.frame_symbol, text = 'X', command = lambda: self.switch_play(0,'X',gamemode), fg = '#dc342e',
            activeforeground = '#dc344e')
        self.button_x.grid( row = 1, column = 0 )
        self.button_o = Button(self.frame_symbol, text = 'O', command = lambda: self.switch_play(1,'O',gamemode), fg = '#376cb6',
            activeforeground = '#376cD6')
        self.button_o.grid( row = 1, column = 1 )
        self.frame_symbol.bind('<Configure>', self.resize_choose_symbol)


    def resize_choose_symbol(self, e):
        font_size = int( (e.height + (e.width/3) )/40 )
        self.label_choose_symbol.configure( font = ('Helvetica',2*font_size) )
        self.button_x.configure( font = ('Arial Bold',4*font_size), bd = 4 )
        self.button_o.configure( font = ('Arial Bold',4*font_size), bd = 4 )


    def switch_play(self, increment, choice, gamemode ):
        self.clicks = increment
        self.player1_choice = choice
        self.frame_symbol.pack_forget()
        self.play(gamemode)


    def retrieve_data(self):
        while True:
            num = self.client.recv(1024).decode()
            print("RECEIVED num is : ", num)
            if num.isdigit():
                self.shared_algorithm(self.playground_buttons[int(num)])
                self.update()
                for btn in self.playground_buttons:
                    if btn['text'] == '' and self.winner == '':
                        btn['state'] = NORMAL
            elif num == 'retry' and self.player_retry:
                self.play_retry('LAN')
                self.opponent_retry = False
                self.player_retry = False
                self.button_retry['text'] = 'Retry'
                self.button_retry['state'] = NORMAL
            elif num == 'retry' and not self.player_retry:
                self.opponent_retry = True



    def send_click(self, button_tic, i):
        self.shared_algorithm(button_tic)
        self.sender.send(str(i-1).encode())
        for btn in self.playground_buttons:
            btn['state'] = DISABLED

    
    def decide_first_bot(self):
        while True:
            my_random = random.random()
            their_random = random.random()
            if my_random > their_random:
                self.turn = self.turn_start = 'you'
                break
            else:
                self.turn = self.turn_start = 'opponent'
                break


    def decide_first_LAN(self):
        while True:
            my_random = random.random()
            if self.server_port == 50001:
                self.sender.send(str(my_random).encode())
                their_random = float(self.client.recv(1024).decode())
            else:
                their_random = float(self.client.recv(1024).decode())
                self.sender.send(str(my_random).encode())
            if my_random > their_random:
                self.turn = self.turn_start = 'you'
                self.player1_choice = 'X'
                self.player_color = '#dc342e'
                break
            else:
                self.turn = self.turn_start = 'opponent'
                self.player1_choice = 'O'
                self.player_color = '#376cb6'
                break


    def who_first(self, gamemode):
        self.window_first = Toplevel()
        self.window_first.app_width = 4
        self.window_first.app_height = 5
        frame = Frame(self.window_first, bg = '#616E7C')
        frame.pack(expand = True, fill = 'both')
        if gamemode == 'online' or gamemode == 'LAN':
            decider_thread = threading.Thread(target=self.decide_first_LAN)
            decider_thread.start()
        elif gamemode == 'bot' or gamemode == 'player':
            decider_thread = threading.Thread(target=self.decide_first_bot)
            decider_thread.start()
        label_username = Label(frame, text = f"WHO GOES FIRST?", bg = '#616E7C', font = ('Helvetica', 19))
        label_username.pack(expand = TRUE, fill = 'both', padx = (30,5), pady = 20)
        self.center(self.window_first)
        decider_thread.join()
        if self.turn == 'you':
            if gamemode == 'online' or gamemode == 'LAN':
                label_username['text'] = f"{self.username} GOES FIRST!"
            elif gamemode == 'bot':
                label_username['text'] = f"YOU GO FIRST!"
            elif gamemode == 'player':
                label_username['text'] = f"PLAYER 1 GOES FIRST!"
        else:
            if gamemode == 'online' or gamemode == 'LAN':
                label_username['text'] = f"{self.opponent_username} GOES FIRST!"
            elif gamemode == 'bot':
                label_username['text'] = f"BOT GOES FIRST!"
            elif gamemode == 'player':
                label_username['text'] = f"PLAYER 2 GOES FIRST!"
        self.after(2000, self.window_first.destroy)


    def play(self, gamemode):
        self.who_first(gamemode)
        if self.player1_choice == 'X':
            self.opponent_choice = 'O'
            self.opponent_color = '#376cb6'
        else:
            self.opponent_choice = 'X'
            self.opponent_color = '#dc342e'
        for child in self.winfo_children():
            try:
                child.pack_forget()
            except:
                pass
        self.frame_play = Frame(self, bg = '#616E7C' )
        self.frame_play.pack( expand = True, fill = 'both' )
        for i in range(2):
            Grid.columnconfigure(self.frame_play, i, weight = 1)
        for i in range(3):
            Grid.rowconfigure(self.frame_play, i, weight = 1)
        self.frame_playground = Frame(self.frame_play, highlightbackground="white", highlightthickness = 2 )
        self.frame_playground.grid( row = 0, columnspan = 2, pady = 20 )
        self.frame_playground.grid_propagate(0)
        for i in range(3):
            Grid.rowconfigure(self.frame_playground, i, weight = 1)
            Grid.columnconfigure(self.frame_playground, i, weight = 1)
        j = k = 0
        self.playground_buttons.clear()
        for i in range(1,10):
            button_tic = Button(self.frame_playground )
            if gamemode == 'player':
                button_tic.configure( command = lambda button_tic = button_tic: self.shared_algorithm(button_tic))
            elif gamemode == 'online' or gamemode == 'LAN':
                button_tic.configure( command = lambda button_tic = button_tic, i = i: self.send_click(button_tic, i))
            elif gamemode == 'bot':
                button_tic.configure( command = lambda button_tic = button_tic: self.play_against_bot_algorithm(button_tic))
            if self.turn == 'opponent' and gamemode != 'bot' and gamemode != 'player':
                button_tic.configure( state = DISABLED )
            button_tic.grid( row = j, column = k )
            if i % 2 == 1:
                button_tic.configure(bg = '#29384d', activebackground = '#29385f')
            else:
                button_tic.configure( bg = '#e6eded', activebackground = '#e6edff')
            self.playground_buttons.append( button_tic )
            k += 1
            if i % 3 == 0:
                j += 1
                k = 0
        self.frame_score = Frame(self.frame_play, bg = '#616E7C' )
        self.frame_score.grid( row = 1, columnspan = 2, sticky = 'NSEW' )
        for i in range(3):
            Grid.columnconfigure(self.frame_score, i, weight = 1)
        for i in range(2):
            Grid.rowconfigure(self.frame_score, i, weight = 1)
        score_label = Label(self.frame_score, text = 'Score', bg = '#616E7C')
        score_label.grid( row = 0, columnspan = 3 )
        self.player1_label = Label(self.frame_score, text = 'Player 1:\t0', bg = '#616E7C')
        if gamemode == 'online' or gamemode == 'LAN':
            self.player1_label.configure( text = f'{self.username}:\t0' )
        self.player1_label.grid( row = 1, column = 0 )
        self.draw_label = Label(self.frame_score, text = 'Draw:\t0', bg = '#616E7C')
        self.draw_label.grid( row = 1, column = 1 )
        self.player2_label = Label(self.frame_score, bg = '#616E7C')
        self.player2_label.grid( row = 1, column = 2 )
        if gamemode == 'player':
            self.player2_label.configure( text = 'Player 2:\t0' )
        elif gamemode == 'online' or gamemode == 'LAN':
            self.player2_label.configure( text = f'{self.opponent_username}:\t0' )
        else:
            self.player2_label.configure( text = 'Bot:\t0' )
        self.button_retry = Button(self.frame_play, text = "Retry", bg = '#7B8794', command = lambda: self.play_retry(gamemode), activebackground = '#7B87B4')
        self.button_retry.grid( row = 2, column = 0, sticky = 'EW', padx = 20, pady = 20 )
        self.button_back = Button(self.frame_play, text = "Back", bg = '#7B8794', command = self.back, activebackground = '#7B87B4')
        if gamemode == 'online' or gamemode == 'LAN':
            self.button_back['command'] = self.back_online
            self.button_retry['command'] = self.retry_online
        self.button_back.grid( row = 2, column = 1, sticky = 'EW', padx = 20, pady = 20 )
        #self.update()
        #self.update_idletasks()
        self.frame_play.bind('<Configure>', self.resize_play )
        self.event_generate("<Configure>", when='now')
        if gamemode == 'online' or gamemode == 'LAN':
            threading.Thread( target = self.retrieve_data).start()
        elif gamemode == 'bot' and self.turn == 'opponent':
                self.play_against_bot_algorithm(None)


    def resize_play(self,e):
        font_size = int( (e.height + (e.width/3) )/40 )
        self.frame_playground.configure( width = int(e.width/1.2), height = int(e.height/1.3) )
        self.frame_playground.grid_propagate(0)
        for button in self.playground_buttons:
            button.configure( width = int( e.width/(1.2*3) ), height = int(e.height/(1.3*3) ), font = ('Arial Bold',4*font_size) )
        for child in self.frame_score.winfo_children():
            child.configure( font = ('Helvetica',font_size//2) )
        self.button_retry.configure( font = ('Helvetica',font_size) )
        self.button_back.configure( font = ('Helvetica',font_size) )


    def back_online(self):
        self.back()
        self.server.close()
        self.client.close()

    def back(self):
        for child in self.winfo_children():
            child.pack_forget()
        self.frame_menu.pack( expand = True, fill = 'both' )


    def play_retry(self, gamemode):
        self.winner = ''
        if self.turn_start == 'opponent':
            self.turn = self.turn_start = 'you'
        else:
            self.turn = self.turn_start = 'opponent'
        for button in self.playground_buttons:
            button.configure( text = '')
            if self.turn == 'you' or gamemode == 'bot' or gamemode == 'player':
                button.configure(state = NORMAL)
            elif self.turn == 'opponent' and gamemode != 'bot':
                button.configure(state = DISABLED)
        if gamemode == 'bot' and self.turn == 'opponent':
                self.play_against_bot_algorithm(None)


    def retry_online(self):
        if self.opponent_retry == False:
            self.button_retry['text'] = 'Waiting...'
            self.button_retry['state'] = DISABLED
            self.sender.send('retry'.encode())
            self.player_retry = True
        else:
            self.sender.send('retry'.encode())
            self.opponent_retry = False
            self.player_retry = False
            self.play_retry('LAN')


    def play_against_bot_algorithm(self, button_tic ):
        self.enabled_buttons.clear()
        game_done = self.shared_algorithm(button_tic)
        if game_done == 0:
            for i in range( len(self.playground_buttons) ):
                if self.playground_buttons[i].cget('text') == '' :
                    self.enabled_buttons.append( self.playground_buttons[i] )
            self.shared_algorithm( self.enabled_buttons[ random.randint(0, len(self.enabled_buttons) - 1) ] )

    
    def shared_algorithm(self, button_tic):
        if not button_tic:
            return 0
        if self.turn == 'you':
            button_tic.configure( text = f'{self.player1_choice}', disabledforeground = '#dc342e', state = DISABLED )
            self.turn = 'opponent'
        else:
            button_tic.configure( text = f'{self.opponent_choice}', disabledforeground = '#376cb6', state = DISABLED )
            self.turn = 'you'
        draw = True
        for button in self.playground_buttons:
            if not button.cget('text'):
                draw = False
        if ( self.playground_buttons[0].cget('text') == self.playground_buttons[1].cget('text') == self.playground_buttons[2].cget('text') 
        and self.playground_buttons[0].cget('text') != ''):
            self.score_update( self.playground_buttons[0].cget('text') )
        elif ( self.playground_buttons[3].cget('text') == self.playground_buttons[4].cget('text') == self.playground_buttons[5].cget('text')
        and self.playground_buttons[3].cget('text') != ''):
            self.score_update( self.playground_buttons[3].cget('text') )
        elif ( self.playground_buttons[6].cget('text') == self.playground_buttons[7].cget('text') == self.playground_buttons[8].cget('text')
        and self.playground_buttons[6].cget('text') != '') :
            self.score_update( self.playground_buttons[6].cget('text') )
        elif ( self.playground_buttons[0].cget('text') == self.playground_buttons[3].cget('text') == self.playground_buttons[6].cget('text')
        and self.playground_buttons[0].cget('text') != ''):
            self.score_update( self.playground_buttons[0].cget('text') )
        elif ( self.playground_buttons[1].cget('text') == self.playground_buttons[4].cget('text') == self.playground_buttons[7].cget('text')
        and self.playground_buttons[1].cget('text') != '') :
            self.score_update( self.playground_buttons[1].cget('text') )
        elif ( self.playground_buttons[2].cget('text') == self.playground_buttons[5].cget('text') == self.playground_buttons[8].cget('text')
        and self.playground_buttons[2].cget('text') != '') :
            self.score_update( self.playground_buttons[2].cget('text') )
        elif ( self.playground_buttons[0].cget('text') == self.playground_buttons[4].cget('text') == self.playground_buttons[8].cget('text')
        and self.playground_buttons[0].cget('text') != '') :
            self.score_update( self.playground_buttons[0].cget('text') )
        elif ( self.playground_buttons[2].cget('text') == self.playground_buttons[4].cget('text') == self.playground_buttons[6].cget('text')
        and self.playground_buttons[2].cget('text') != ''):
            self.score_update( self.playground_buttons[2].cget('text') )
        elif draw:
            self.score_update('draw')
        else:
            return 0
        return 1


    def score_update(self, winner):
        if winner == 'draw':
            self.winner = 'draw'
            draw_text = self.draw_label.cget('text')
            draw_text = draw_text.split('\t')
            self.draw_label.configure( text = draw_text[0] + '\t' + str( int(draw_text[1]) + 1) )
        elif winner == self.player1_choice:
            self.winner = 'player1'
            player1_text = self.player1_label.cget('text')
            player1_text = player1_text.split('\t')
            self.player1_label.configure( text = player1_text[0] + '\t' + str( int(player1_text[1]) + 1) )
        else:
            self.winner = 'player2'
            player2_text = self.player2_label.cget('text')
            player2_text = player2_text.split('\t')
            self.player2_label.configure( text = player2_text[0] + '\t' + str( int(player2_text[1]) + 1) )
        for button in self.playground_buttons:
            button.configure( state = DISABLED, disabledforeground = 'gray' )

if __name__ == "__main__":
    App()