import tkinter as tk
import tkinter.messagebox
import random
import os

class TicTacToe:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TicTacToe, cls).__new__(cls)
        return cls._instance

    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.game_mode = tk.IntVar(value=1)
        tk.Label(master, text="Select game mode:", font='Times 15 bold').grid(row=0, column=0, columnspan=3)
        tk.Radiobutton(master, text="Human vs Human", variable=self.game_mode, value=1, command=self.setup_game).grid(row=1, column=0)
        tk.Radiobutton(master, text="Human vs AI", variable=self.game_mode, value=2, command=self.setup_game).grid(row=1, column=1)

        self.setup_game()

    def setup_game(self):
        try:
            for row in self.buttons:
                for button in row:
                    button.destroy()
            self.reset_button.destroy()
            self.player1_label.destroy()
            self.player2_label.destroy()
            self.player1_entry.destroy()
            self.player2_entry.destroy()
        except AttributeError:
            pass

        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar(value='Computer' if self.game_mode.get() == 2 else '')

        self.player1_label = tk.Label(self.master, text="Player 1:", font='Times 20 bold')
        self.player1_label.grid(row=2, column=0)
        self.player1_entry = tk.Entry(self.master, textvariable=self.player1_name, bd=5)
        self.player1_entry.grid(row=2, column=1, columnspan=8)

        if self.game_mode.get() == 1:
            self.player2_name.set('')  # Clear default name
            self.player2_label = tk.Label(self.master, text="Player 2:", font='Times 20 bold')
            self.player2_label.grid(row=3, column=0)
            self.player2_entry = tk.Entry(self.master, textvariable=self.player2_name, bd=5)
            self.player2_entry.grid(row=3, column=1, columnspan=8)

        self.buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.create_button(i, j)

        self.bclick = True
        self.flag = 0

        self.reset_button = tk.Button(self.master, text="Reset", font='Times 20 bold', bg='white', fg='black',
                                      command=self.reset_game)
        self.reset_button.grid(row=7, column=0, columnspan=3)

        self.load_game()

    def create_button(self, row, col):
        cmd = lambda r=row, c=col: self.btn_click(r, c)
        button = tk.Button(self.master, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                           command=cmd)
        button.grid(row=row + 4, column=col)
        self.buttons[row][col] = button

    def btn_click(self, row, col):
        if self.buttons[row][col]['text'] == " ":
            if self.bclick:
                player = PlayerFactory.create_player('human', 'X')
                player.make_move(self.buttons, row, col)
                self.flag += 1
                win = self.check_for_win()
                if win:
                    self.announce_winner('X')
                elif self.flag == 9:
                    tkinter.messagebox.showinfo("Tic-Tac-Toe", "It is a Tie")
                    self.disable_buttons()
                self.bclick = False  # Switch to AI in Human vs AI mode
            else:
                if self.game_mode.get() == 1:  # Human vs Human mode
                    player = PlayerFactory.create_player('human', 'O')
                    player.make_move(self.buttons, row, col)
                    self.flag += 1
                    if self.check_for_win():
                        self.announce_winner('O')
                    self.bclick = True  # Switch turn back to first player
                    if self.flag == 9 and not self.check_for_win():
                        tkinter.messagebox.showinfo("Tic-Tac-Toe", "It is a Tie")
                        self.disable_buttons()

            if self.game_mode.get() == 2 and not self.bclick and not win:
                self.master.after(100, self.ai_move)

    def ai_move(self):
        player = PlayerFactory.create_player('ai')
        player.make_move(self.buttons)
        self.flag += 1
        if self.check_for_win():
            self.announce_winner('O')
        self.bclick = True
        if self.flag >= 9 and not self.check_for_win():
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "It is a Tie")
            self.disable_buttons()

    def check_for_win(self):
        for row in range(3):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != " ":
                return True
        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == self.buttons[2][col]['text'] != " ":
                return True
        if (self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != " ") or \
                (self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != " "):
            return True
        return False

    def announce_winner(self, player):
        winner_name = self.player1_name.get() if player == 'X' else self.player2_name.get()
        if not winner_name:
            winner_name = "Player 1" if player == 'X' else "Player 2"
        tk.messagebox.showinfo("Tic-Tac-Toe", f"{winner_name} Wins!")
        self.disable_buttons()

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def reset_game(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ", state=tk.NORMAL)
        self.bclick = True
        self.flag = 0
        self.save_game()

    def save_game(self):
        with open('game_state.txt', 'w') as f:
            for row in self.buttons:
                f.write(''.join(button['text'] for button in row) + '\n')

    def load_game(self):
        if os.path.exists('game_state.txt'):
            with open('game_state.txt', 'r') as f:
                for i, line in enumerate(f):
                    for j, char in enumerate(line.strip()):
                        self.buttons[i][j]['text'] = char


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, buttons, row=None, col=None):
        pass

class HumanPlayer(Player):
    def make_move(self, buttons, row, col):
        if buttons[row][col]['text'] == " ":
            buttons[row][col]['text'] = self.symbol

class AIPlayer(Player):
    def make_move(self, buttons, row=None, col=None):
        empty = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]['text'] == " "]
        if empty:
            row, col = random.choice(empty)
            buttons[row][col]['text'] = self.symbol

class PlayerFactory:
    @staticmethod
    def create_player(player_type, symbol='O'):
        if player_type == 'human':
            return HumanPlayer(symbol)
        elif player_type == 'ai':
            return AIPlayer(symbol)

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()


