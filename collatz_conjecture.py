import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def collatz_sequence(n):
    """Generate the Collatz sequence for a given starting number."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

class CollatzGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Collatz Conjecture Visualizer")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_main_menu()
    
    def create_main_menu(self):
        """Create the main menu interface."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2E86AB', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title = tk.Label(title_frame, text="COLLATZ CONJECTURE", 
                        font=('Arial', 24, 'bold'), bg='#2E86AB', fg='white')
        title.pack(pady=10)
        
        subtitle = tk.Label(title_frame, text="3x+1 Problem Visualizer", 
                           font=('Arial', 12), bg='#2E86AB', fg='white')
        subtitle.pack()
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#F0F0F0')
        button_frame.pack(expand=True, fill='both', padx=40, pady=30)
        
        buttons = [
            ("📊 Single Sequence", self.single_sequence_window),
            ("📈 Multiple Sequences", self.multiple_sequences_window),
            ("⏱️ Stopping Times", self.stopping_times_window),
            ("🔝 Maximum Values", self.max_values_window),
            ("📝 View Sequence (Text)", self.text_sequence_window),
            ("ℹ️ About", self.show_about),
            ("❌ Exit", self.root.quit)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command,
                          font=('Arial', 12), width=30, height=2,
                          bg='white', relief='raised', bd=2,
                          cursor='hand2')
            btn.pack(pady=8)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#E8F4F8'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='white'))
    
    def single_sequence_window(self):
        """Window for single sequence visualization."""
        win = tk.Toplevel(self.root)
        win.title("Single Sequence Visualization")
        win.geometry("400x250")
        
        tk.Label(win, text="Single Sequence Visualization", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(win, text="Enter starting number:", 
                font=('Arial', 11)).pack(pady=5)
        
        entry = tk.Entry(win, font=('Arial', 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        def visualize():
            try:
                num = int(entry.get())
                if num <= 0:
                    messagebox.showerror("Error", "Please enter a positive number!")
                    return
                
                seq = collatz_sequence(num)
                
                # Create plot
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(range(len(seq)), seq, marker='o', markersize=5, 
                       color='#2E86AB', linewidth=2, markerfacecolor='#A23B72')
                ax.set_xlabel('Step Number', fontsize=12)
                ax.set_ylabel('Value', fontsize=12)
                ax.set_title(f'Collatz Sequence starting from {num}\n'
                           f'Length: {len(seq)} steps | Max: {max(seq)}', 
                           fontsize=13, fontweight='bold')
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Visualize", command=visualize,
                 font=('Arial', 11), bg='#2E86AB', fg='white',
                 width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", command=win.destroy,
                 font=('Arial', 11), width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: visualize())
    
    def multiple_sequences_window(self):
        """Window for multiple sequences visualization."""
        win = tk.Toplevel(self.root)
        win.title("Multiple Sequences Visualization")
        win.geometry("450x300")
        
        tk.Label(win, text="Multiple Sequences Visualization", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(win, text="Enter numbers separated by commas:", 
                font=('Arial', 11)).pack(pady=5)
        tk.Label(win, text="(e.g., 7,15,27)", 
                font=('Arial', 9), fg='gray').pack()
        
        entry = tk.Entry(win, font=('Arial', 12), width=30)
        entry.pack(pady=10)
        entry.focus()
        
        tk.Label(win, text="Scale:", font=('Arial', 11)).pack(pady=5)
        scale_var = tk.StringVar(value="normal")
        tk.Radiobutton(win, text="Normal Scale", variable=scale_var, 
                      value="normal", font=('Arial', 10)).pack()
        tk.Radiobutton(win, text="Logarithmic Scale", variable=scale_var, 
                      value="log", font=('Arial', 10)).pack()
        
        def visualize():
            try:
                numbers = [int(x.strip()) for x in entry.get().split(',')]
                if not all(n > 0 for n in numbers):
                    messagebox.showerror("Error", "All numbers must be positive!")
                    return
                
                fig, ax = plt.subplots(figsize=(12, 7))
                colors = plt.cm.tab10(range(len(numbers)))
                
                for i, num in enumerate(numbers):
                    seq = collatz_sequence(num)
                    if scale_var.get() == 'log':
                        ax.semilogy(range(len(seq)), seq, marker='o', markersize=3,
                                   label=f'Start: {num}', alpha=0.7, color=colors[i])
                    else:
                        ax.plot(range(len(seq)), seq, marker='o', markersize=4,
                               label=f'Start: {num}', alpha=0.7, linewidth=2, color=colors[i])
                
                ax.set_xlabel('Step Number', fontsize=12)
                ylabel = 'Value (log scale)' if scale_var.get() == 'log' else 'Value'
                ax.set_ylabel(ylabel, fontsize=12)
                ax.set_title('Collatz Conjecture - Multiple Sequences', 
                           fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers separated by commas!")
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Visualize", command=visualize,
                 font=('Arial', 11), bg='#2E86AB', fg='white',
                 width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", command=win.destroy,
                 font=('Arial', 11), width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: visualize())
    
    def stopping_times_window(self):
        """Window for stopping times visualization."""
        win = tk.Toplevel(self.root)
        win.title("Stopping Times Analysis")
        win.geometry("400x250")
        
        tk.Label(win, text="Stopping Times Analysis", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(win, text="Analyze numbers from 1 to:", 
                font=('Arial', 11)).pack(pady=5)
        
        entry = tk.Entry(win, font=('Arial', 12), width=20)
        entry.pack(pady=10)
        entry.insert(0, "100")
        entry.focus()
        
        def visualize():
            try:
                max_n = int(entry.get())
                if max_n <= 0:
                    messagebox.showerror("Error", "Please enter a positive number!")
                    return
                
                numbers = range(1, max_n + 1)
                stopping_times = [len(collatz_sequence(n)) - 1 for n in numbers]
                
                fig, ax = plt.subplots(figsize=(14, 6))
                ax.bar(numbers, stopping_times, color='steelblue', 
                      alpha=0.7, edgecolor='navy', linewidth=0.5)
                ax.set_xlabel('Starting Number', fontsize=12)
                ax.set_ylabel('Steps to Reach 1', fontsize=12)
                ax.set_title(f'Collatz Conjecture: Stopping Times (1 to {max_n})\n'
                           f'Longest: {max(stopping_times)} steps from number {stopping_times.index(max(stopping_times)) + 1}',
                           fontsize=13, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='y')
                plt.tight_layout()
                plt.show()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Analyze", command=visualize,
                 font=('Arial', 11), bg='#2E86AB', fg='white',
                 width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", command=win.destroy,
                 font=('Arial', 11), width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: visualize())
    
    def max_values_window(self):
        """Window for maximum values visualization."""
        win = tk.Toplevel(self.root)
        win.title("Maximum Values Analysis")
        win.geometry("400x250")
        
        tk.Label(win, text="Maximum Values Analysis", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(win, text="Analyze numbers from 1 to:", 
                font=('Arial', 11)).pack(pady=5)
        
        entry = tk.Entry(win, font=('Arial', 12), width=20)
        entry.pack(pady=10)
        entry.insert(0, "100")
        entry.focus()
        
        def visualize():
            try:
                max_n = int(entry.get())
                if max_n <= 0:
                    messagebox.showerror("Error", "Please enter a positive number!")
                    return
                
                numbers = range(1, max_n + 1)
                max_values = [max(collatz_sequence(n)) for n in numbers]
                
                fig, ax = plt.subplots(figsize=(14, 6))
                scatter = ax.scatter(numbers, max_values, c=max_values, 
                                    cmap='viridis', s=30, alpha=0.6, 
                                    edgecolors='black', linewidth=0.5)
                ax.set_xlabel('Starting Number', fontsize=12)
                ax.set_ylabel('Maximum Value Reached', fontsize=12)
                ax.set_title(f'Collatz Conjecture: Maximum Values (1 to {max_n})\n'
                           f'Highest Peak: {max(max_values)} from number {max_values.index(max(max_values)) + 1}',
                           fontsize=13, fontweight='bold')
                plt.colorbar(scatter, label='Max Value', ax=ax)
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Analyze", command=visualize,
                 font=('Arial', 11), bg='#2E86AB', fg='white',
                 width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", command=win.destroy,
                 font=('Arial', 11), width=12, height=2, cursor='hand2').pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: visualize())
    
    def text_sequence_window(self):
        """Window for text-based sequence view."""
        win = tk.Toplevel(self.root)
        win.title("View Sequence (Text)")
        win.geometry("500x500")
        
        tk.Label(win, text="View Sequence (Text)", 
                font=('Arial', 16, 'bold')).pack(pady=15)
        
        tk.Label(win, text="Enter starting number:", 
                font=('Arial', 11)).pack(pady=5)
        
        entry = tk.Entry(win, font=('Arial', 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        text_area = scrolledtext.ScrolledText(win, font=('Courier', 10), 
                                             width=55, height=20)
        text_area.pack(pady=10, padx=20)
        
        def show_sequence():
            try:
                num = int(entry.get())
                if num <= 0:
                    messagebox.showerror("Error", "Please enter a positive number!")
                    return
                
                seq = collatz_sequence(num)
                text_area.delete('1.0', tk.END)
                
                text_area.insert(tk.END, f"Sequence from {num} to 1\n")
                text_area.insert(tk.END, f"{'='*40}\n")
                text_area.insert(tk.END, f"Length: {len(seq)} steps\n")
                text_area.insert(tk.END, f"Maximum value: {max(seq)}\n")
                text_area.insert(tk.END, f"{'='*40}\n\n")
                
                for i, val in enumerate(seq):
                    text_area.insert(tk.END, f"Step {i:4d}: {val}\n")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")
        
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Show Sequence", command=show_sequence,
                 font=('Arial', 11), bg='#2E86AB', fg='white',
                 width=15, height=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", command=win.destroy,
                 font=('Arial', 11), width=15, height=2, cursor='hand2').pack(side='left', padx=5)
        
        entry.bind('<Return>', lambda e: show_sequence())
    
    def show_about(self):
        """Show about dialog."""
        about_text = """COLLATZ CONJECTURE (3x+1 Problem)

The Collatz Conjecture is an unsolved mathematical problem.

Rules:
• Start with any positive integer n
• If n is even: divide it by 2 (n/2)
• If n is odd: multiply by 3 and add 1 (3n+1)
• Repeat the process

The conjecture states that no matter what number 
you start with, you will always eventually reach 1.

Example: Starting with 7
7 → 22 → 11 → 34 → 17 → 52 → 26 → 13 
→ 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

Despite its simplicity, no one has proven 
this works for ALL numbers!"""
        
        messagebox.showinfo("About Collatz Conjecture", about_text)

def main():
    root = tk.Tk()
    app = CollatzGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()