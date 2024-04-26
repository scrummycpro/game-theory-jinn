import tkinter as tk
from tkinter import ttk
import axelrod as axl
import tkinter.messagebox as msgbox
import sqlite3
from datetime import datetime

class MoranProcessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Moran Process Simulation")

        # Get all player names
        self.player_names = [strategy.name for strategy in axl.strategies]

        # Create widgets
        self.label = ttk.Label(root, text="Select Players:")
        self.label.grid(row=0, column=0, padx=5, pady=10)

        # Selection box for player 1
        self.player1_label = ttk.Label(root, text="Player 1:")
        self.player1_label.grid(row=1, column=0, padx=5, pady=5)
        self.player1_var = tk.StringVar(root)
        self.player1_var.set(self.player_names[0])
        self.player1_menu = ttk.OptionMenu(root, self.player1_var, *self.player_names)
        self.player1_menu.grid(row=1, column=1, padx=5, pady=5)

        # Selection box for player 2
        self.player2_label = ttk.Label(root, text="Player 2:")
        self.player2_label.grid(row=2, column=0, padx=5, pady=5)
        self.player2_var = tk.StringVar(root)
        self.player2_var.set(self.player_names[1])
        self.player2_menu = ttk.OptionMenu(root, self.player2_var, *self.player_names)
        self.player2_menu.grid(row=2, column=1, padx=5, pady=5)

        # Button to start the simulation
        self.start_button = ttk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=3, columnspan=2, padx=5, pady=10)

        # Create SQLite connection and cursor
        self.conn = sqlite3.connect("results.db")
        self.cur = self.conn.cursor()

        # Create table if not exists
        self.cur.execute('''CREATE TABLE IF NOT EXISTS results
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             player1 TEXT,
                             player2 TEXT,
                             winner TEXT,
                             seed INTEGER,
                             timestamp TEXT)''')
        self.conn.commit()

    def start_simulation(self):
        # Get selected players
        player1_name = self.player1_var.get()
        player2_name = self.player2_var.get()

        # Find strategy objects corresponding to the selected names
        player1_strategy = next(strategy for strategy in axl.strategies if strategy.name == player1_name)
        player2_strategy = next(strategy for strategy in axl.strategies if strategy.name == player2_name)

        # Set seed and timestamp
        seed = 10000  # Change this to your desired seed
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Run the Moran Process
        mp = axl.MoranProcess([player1_strategy(), player2_strategy()], seed=seed)
        populations = mp.play()

        # Get the final population distribution
        final_distribution = populations[-1]

        # Determine the winner
        player1_count = final_distribution[player1_name]
        player2_count = final_distribution[player2_name]

        if player1_count == player2_count:
            winner = "Tie"
        else:
            winner = player1_name if player1_count > player2_count else player2_name

        # Display the winner
        msgbox.showinfo("Winner", f"The winner is: {winner}")

        # Insert results into the database
        self.cur.execute('''INSERT INTO results (player1, player2, winner, seed, timestamp)
                            VALUES (?, ?, ?, ?, ?)''', (player1_name, player2_name, winner, seed, timestamp))
        self.conn.commit()

    def __del__(self):
        # Close SQLite connection
        self.conn.close()

def main():
    root = tk.Tk()
    app = MoranProcessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
