import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import axelrod as axl

class StrategyListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Axelrod Strategy Lists")

        # Create widgets
        self.label = ttk.Label(root, text="Select Strategy List:")
        self.label.grid(row=0, column=0, padx=5, pady=10)

        # Strategy list selection box
        self.strategy_list_var = tk.StringVar(root)
        self.strategy_list_var.set("Demo Strategies")
        self.strategy_list_menu = ttk.OptionMenu(root, self.strategy_list_var, "Demo Strategies", "Basic Strategies", "Long Run Time Strategies", "Cheating Strategies", command=self.show_strategy_list)
        self.strategy_list_menu.grid(row=0, column=1, padx=5, pady=10)

        # Strategy list text widget
        self.strategy_list_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
        self.strategy_list_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Right-click menu
        self.popup_menu = tk.Menu(root, tearoff=0)
        self.popup_menu.add_command(label="Copy", command=self.copy_text)

        # Bind right-click event
        self.strategy_list_text.bind("<Button-3>", self.popup)

        # Export button
        self.export_button = ttk.Button(root, text="Export", command=self.export_text)
        self.export_button.grid(row=2, column=0, columnspan=2, pady=5)

    def show_strategy_list(self, selected_list):
        strategies = []

        if selected_list == "Demo Strategies":
            strategies = axl.demo_strategies
        elif selected_list == "Basic Strategies":
            strategies = axl.basic_strategies
        elif selected_list == "Long Run Time Strategies":
            strategies = axl.long_run_time_strategies
        elif selected_list == "Cheating Strategies":
            strategies = axl.cheating_strategies

        self.strategy_list_text.delete(1.0, tk.END)
        self.strategy_list_text.insert(tk.END, "\n".join(str(strat).split('.')[-1][:-2] for strat in strategies))

    def popup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        selected_text = self.strategy_list_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

    def export_text(self):
        text_to_export = self.strategy_list_text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(text_to_export)
                messagebox.showinfo("Export Successful", f"Text successfully exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    app = StrategyListGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
