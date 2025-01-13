import pandas as pd
import torch
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def format_tensor_output(tensor):
    """Format tensor output with proper indentation and spacing"""
    lines = ['queries = torch.tensor([']
    
    # Format each row
    for row in tensor:
        # Format each value with 4 decimal places
        formatted_row = [f"{val:.4f}" for val in row]
        line = f"    [{', '.join(formatted_row)}],"
        lines.append(line)
    
    lines[-1] = lines[-1][:-1]  # Remove last comma
    lines.append('    ])')
    
    # Add CUDA check
    lines.append('if torch.cuda.is_available():')
    lines.append('    queries = queries.cuda()')
    
    return '\n'.join(lines)

def csv_to_tensor(csv_path):
    """
    Convert CSV file with exactly 10 points (r00-r09) to tensor.
    Returns:
        torch.Tensor with shape (10, 3) where each row is [frame_num, x, y]
    """
    try:
        # Read the CSV file as plain text
        with open(csv_path, 'r') as file:
            lines = file.readlines()
            
        # Get the data line (4th line, index 3)
        data_line = lines[3].strip().split(',')
        
        # Extract filename from the correct position
        filename = data_line[2]  # img052.png is in the third column
        frame_num = float(filename.replace('img', '').replace('.png', ''))
        
        # Initialize tensor data
        tensor_data = []
        
        # Process exactly 10 points (r00-r09), starting from index 3
        for i in range(10):
            x_idx = 3 + (i * 2)
            y_idx = 4 + (i * 2)
            
            x = float(data_line[x_idx])
            y = float(data_line[y_idx])
            
            tensor_data.append([frame_num, x, y])
        
        return torch.tensor(tensor_data)

    except Exception as e:
        messagebox.showerror("Error", f"Error processing CSV file: {str(e)}")
        return None

class CSVConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV to Tensor Converter")
        
        # Set window size and position
        window_width = 500
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create and pack widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Title label
        title_label = tk.Label(main_frame, 
                             text="CSV to Tensor Converter", 
                             font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Select file button
        select_button = tk.Button(main_frame, 
                                text="Select CSV File",
                                command=self.select_file,
                                width=20,
                                height=2)
        select_button.pack(pady=10)
        
        # Create a frame for the results with scrollbar
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill='both', expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status text with scrollbar
        self.status_text = tk.Text(result_frame, 
                                 wrap=tk.NONE,  # Changed to NONE for proper code formatting
                                 height=15,
                                 font=('Courier', 10),  # Monospace font for code
                                 yscrollcommand=scrollbar.set)
        self.status_text.pack(fill='both', expand=True)
        scrollbar.config(command=self.status_text.yview)
        
        # Add horizontal scrollbar
        h_scrollbar = tk.Scrollbar(result_frame, orient='horizontal')
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_text.config(xscrollcommand=h_scrollbar.set)
        h_scrollbar.config(command=self.status_text.xview)
        
        # Initial status message
        self.status_text.insert(tk.END, "No file selected")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.status_text.delete('1.0', tk.END)
            self.status_text.insert(tk.END, f"Processing: {file_path}\n")
            self.root.update()
            
            tensor = csv_to_tensor(file_path)
            if tensor is not None:
                self.status_text.delete('1.0', tk.END)
                formatted_output = format_tensor_output(tensor)
                self.status_text.insert(tk.END, formatted_output)
                print("\nFormatted tensor code:")
                print(formatted_output)

def main():
    root = tk.Tk()
    app = CSVConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()