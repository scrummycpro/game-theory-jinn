import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import axelrod as axl

class StrategyDescriptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Axelrod Strategy Descriptions")

        # Get all player names and descriptions
        self.player_info = {strategy.name: getattr(strategy, '__doc__', 'No description available') for strategy in axl.strategies}

        # Create widgets
        self.label = ttk.Label(root, text="Select Strategy:")
        self.label.grid(row=0, column=0, padx=5, pady=10)

        # Selection box for strategies
        self.strategy_var = tk.StringVar(root)
        self.strategy_var.set(list(self.player_info.keys())[0])
        self.strategy_menu = ttk.OptionMenu(root, self.strategy_var, *self.player_info.keys())
        self.strategy_menu.grid(row=0, column=1, padx=5, pady=10)

        # Button to show description
        self.show_button = ttk.Button(root, text="Show Description", command=self.show_description)
        self.show_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # Description text widget
        self.description_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.description_text.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Button to export description
        self.export_button = ttk.Button(root, text="Export Description", command=self.export_description)
        self.export_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def show_description(self):
        selected_strategy = self.strategy_var.get()
        description = self.player_info[selected_strategy]
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, description)

    def export_description(self):
        selected_strategy = self.strategy_var.get()
        description = self.player_info[selected_strategy]

        # Open file dialog to select export location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return  # User canceled the dialog

        # Write description to the selected file
        with open(file_path, "w") as file:
            file.write(f"Strategy: {selected_strategy}\n")
            file.write(f"Description: {description}")

def main():
    root = tk.Tk()
    app = StrategyDescriptionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
