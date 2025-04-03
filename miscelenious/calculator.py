import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Scientific Calculator")
        self.master.geometry("400x500")
        self.master.resizable(False, False)
        self.master.configure(bg="#2d2d2d")  # Dark background
        
        # Display frame
        self.display_frame = tk.Frame(master, bg="#2d2d2d")  # Dark background
        self.display_frame.pack(padx=10, pady=10, fill=tk.BOTH)
        
        # Result display
        self.equation = tk.StringVar()
        self.equation.set("0")
        
        self.display = tk.Entry(
            self.display_frame, 
            textvariable=self.equation, 
            font=("Arial", 24), 
            bd=10, 
            relief=tk.FLAT,
            justify=tk.RIGHT,
            bg="#3d3d3d",  # Darker gray for display
            fg="#ffffff",  # White text
            insertbackground="#ffffff"  # White cursor
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        self.buttons_frame = tk.Frame(master, bg="#2d2d2d")  # Dark background
        self.buttons_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Define buttons
        self.create_buttons()
        
        # Initialize variables
        self.current_input = ""
        self.memory = 0
        self.error_state = False
    
    def create_buttons(self):
        # Button configurations (text, row, column, function, color)
        buttons = [
            # Row 0 - Memory and Clear
            ("MC", 0, 0, lambda: self.memory_clear(), "#444444"),
            ("MR", 0, 1, lambda: self.memory_recall(), "#444444"),
            ("M+", 0, 2, lambda: self.memory_add(), "#444444"),
            ("M-", 0, 3, lambda: self.memory_subtract(), "#444444"),
            ("C", 0, 4, lambda: self.clear(), "#d9534f"),
            
            # Row 1 - Functions
            ("sin", 1, 0, lambda: self.calculate_function("sin"), "#333333"),
            ("cos", 1, 1, lambda: self.calculate_function("cos"), "#333333"),
            ("tan", 1, 2, lambda: self.calculate_function("tan"), "#333333"),
            ("√", 1, 3, lambda: self.calculate_function("sqrt"), "#333333"),
            ("DEL", 1, 4, lambda: self.delete_last(), "#d9534f"),
            
            # Row 2 - More Functions
            ("log", 2, 0, lambda: self.calculate_function("log"), "#333333"),
            ("ln", 2, 1, lambda: self.calculate_function("ln"), "#333333"),
            ("x²", 2, 2, lambda: self.calculate_function("square"), "#333333"),
            ("x³", 2, 3, lambda: self.calculate_function("cube"), "#333333"),
            ("÷", 2, 4, lambda: self.add_operator("/"), "#ff9800"),
            
            # Row 3 - Numbers and operators
            ("7", 3, 0, lambda: self.add_digit("7"), "#4a4a4a"),
            ("8", 3, 1, lambda: self.add_digit("8"), "#4a4a4a"),
            ("9", 3, 2, lambda: self.add_digit("9"), "#4a4a4a"),
            ("(", 3, 3, lambda: self.add_parenthesis("("), "#333333"),
            ("×", 3, 4, lambda: self.add_operator("*"), "#ff9800"),
            
            # Row 4
            ("4", 4, 0, lambda: self.add_digit("4"), "#4a4a4a"),
            ("5", 4, 1, lambda: self.add_digit("5"), "#4a4a4a"),
            ("6", 4, 2, lambda: self.add_digit("6"), "#4a4a4a"),
            (")", 4, 3, lambda: self.add_parenthesis(")"), "#333333"),
            ("-", 4, 4, lambda: self.add_operator("-"), "#ff9800"),
            
            # Row 5
            ("1", 5, 0, lambda: self.add_digit("1"), "#4a4a4a"),
            ("2", 5, 1, lambda: self.add_digit("2"), "#4a4a4a"),
            ("3", 5, 2, lambda: self.add_digit("3"), "#4a4a4a"),
            ("π", 5, 3, lambda: self.add_constant("pi"), "#333333"),
            ("+", 5, 4, lambda: self.add_operator("+"), "#ff9800"),
            
            # Row 6
            ("±", 6, 0, lambda: self.toggle_sign(), "#333333"),
            ("0", 6, 1, lambda: self.add_digit("0"), "#4a4a4a"),
            (".", 6, 2, lambda: self.add_decimal(), "#4a4a4a"),
            ("e", 6, 3, lambda: self.add_constant("e"), "#333333"),
            ("=", 6, 4, lambda: self.calculate(), "#5bc0de"),
        ]
        
        # Configure grid for equal column widths
        for i in range(5):
            self.buttons_frame.columnconfigure(i, weight=1)
        for i in range(7):
            self.buttons_frame.rowconfigure(i, weight=1)
        
        # Create and place buttons
        for (text, row, col, command, color) in buttons:
            button = tk.Button(
                self.buttons_frame, 
                text=text, 
                font=("Arial", 12, "bold"), 
                bg=color,
                fg="#ffffff",  # White text for all buttons
                relief=tk.RAISED,
                bd=3,
                command=command,
                activebackground="#666666",  # Darker when pressed
                activeforeground="#ffffff"
            )
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    def add_digit(self, digit):
        if self.error_state:
            self.clear()
        
        current = self.equation.get()
        if current == "0":
            self.equation.set(digit)
        else:
            self.equation.set(current + digit)
    
    def add_operator(self, operator):
        if self.error_state:
            self.clear()
            
        current = self.equation.get()
        # Prevent starting with operators except minus
        if current == "0" and operator != "-":
            return
        
        # Replace the last operator if the last character is an operator
        if current and current[-1] in "+-*/":
            self.equation.set(current[:-1] + operator)
        else:
            self.equation.set(current + operator)
    
    def add_decimal(self):
        if self.error_state:
            self.clear()
            
        current = self.equation.get()
        # Check if the last number already has a decimal point
        parts = "".join([c if c.isdigit() or c == "." else " " for c in current]).split()
        if not parts or "." not in parts[-1]:
            self.equation.set(current + ".")
    
    def add_parenthesis(self, parenthesis):
        if self.error_state:
            self.clear()
            
        current = self.equation.get()
        if current == "0" and parenthesis == "(":
            self.equation.set(parenthesis)
        else:
            self.equation.set(current + parenthesis)
    
    def add_constant(self, constant):
        if self.error_state:
            self.clear()
            
        current = self.equation.get()
        if constant == "pi":
            value = str(math.pi)
        elif constant == "e":
            value = str(math.e)
        
        if current == "0":
            self.equation.set(value)
        else:
            self.equation.set(current + value)
    
    def calculate_function(self, function):
        if self.error_state:
            self.clear()
            
        try:
            current = self.equation.get()
            if current == "0":
                current = ""
                
            if function == "sin":
                self.equation.set(current + "math.sin(")
            elif function == "cos":
                self.equation.set(current + "math.cos(")
            elif function == "tan":
                self.equation.set(current + "math.tan(")
            elif function == "sqrt":
                self.equation.set(current + "math.sqrt(")
            elif function == "log":
                self.equation.set(current + "math.log10(")
            elif function == "ln":
                self.equation.set(current + "math.log(")
            elif function == "square":
                if current and current[-1].isdigit() or current[-1] == ")":
                    self.equation.set(current + "**2")
                else:
                    self.equation.set(current + "**2")
            elif function == "cube":
                if current and current[-1].isdigit() or current[-1] == ")":
                    self.equation.set(current + "**3")
                else:
                    self.equation.set(current + "**3")
        except:
            self.error_state = True
            self.equation.set("Error")
    
    def toggle_sign(self):
        if self.error_state:
            self.clear()
            
        current = self.equation.get()
        if current and current != "0":
            if current.startswith("-"):
                self.equation.set(current[1:])
            else:
                self.equation.set("-" + current)
    
    def calculate(self):
        if self.error_state:
            self.clear()
            return
            
        try:
            expression = self.equation.get()
            # Replace display symbols with actual operators
            expression = expression.replace("×", "*").replace("÷", "/")
            
            # Prepare expression for evaluation
            expression = expression.replace("^", "**")
            
            # Evaluate and display result
            result = eval(expression)
            self.equation.set(str(result))
        except Exception as e:
            self.error_state = True
            self.equation.set("Error")
    
    def clear(self):
        self.equation.set("0")
        self.error_state = False
    
    def delete_last(self):
        if self.error_state:
            self.clear()
            return
            
        current = self.equation.get()
        if len(current) == 1 or current == "Error":
            self.equation.set("0")
        else:
            self.equation.set(current[:-1])
    
    def memory_clear(self):
        self.memory = 0
    
    def memory_recall(self):
        if self.error_state:
            self.clear()
        
        current = self.equation.get()
        if current == "0":
            self.equation.set(str(self.memory))
        else:
            self.equation.set(current + str(self.memory))
    
    def memory_add(self):
        try:
            current = self.equation.get()
            self.memory += float(eval(current))
        except:
            pass
    
    def memory_subtract(self):
        try:
            current = self.equation.get()
            self.memory -= float(eval(current))
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
