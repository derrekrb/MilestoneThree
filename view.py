import tkinter as tk
from tkinter import filedialog
from model import Memory
from controller import Controller
from tkinter import messagebox


class View:
    """The View class presents all the data to the user"""

    def __init__(
        self,
        master,
        memory,
        instruction_counter,
        instruction_register,
        operation_code,
        operand,
        accumulator,
        big_storage,
    ):
        # Initialize variables from main
        # and initialize main window
        self.main_frame = tk.Frame(master)
        self.memory = memory
        self.instruction_counter = instruction_counter
        self.instruction_register = instruction_register
        self.operation_code = operation_code
        self.operand = operand
        self.accumulator = accumulator
        self.big_storage = big_storage

        # Initialize Memory Class from model
        self.M = Memory(self.memory)

        self.createWindow()

    def createWindow(self):
        """Creates the GUI for UVSim"""
        # Begin creating widgets
        self.main_frame.grid(sticky="news", pady=50, padx=50)

        # Displays the greeting to the UVsim
        greeting = tk.Label(
            self.main_frame,
            text="---- Instructions given in the UVsim must be in the format of +0000.  Ex. +1001 is a valid instruction ----",
        )
        greeting.grid(row=0, column=1, pady=10, padx=10)

        # Begin creating input box and scroll bar
        frame_canvas = tk.Frame(self.main_frame)
        frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky="nw")
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_propagate(False)
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, sticky="news")
        vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=vsb.set)

        # Create frame for export and import buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=0, column=0)

        button_explore = tk.Button(
            button_frame, text="Import File", command=self.browseFiles
        )
        button_explore.grid(row=0, column=0, padx=5)
        button_save = tk.Button(button_frame, text="Export File", command=self.saveFile)
        button_save.grid(row=0, column=1, padx=5)

        # Create a frame for the help button
        help_button = tk.Button(self.main_frame, text="Help", command=self.helpButton)
        help_button.grid(row=0, column=2)

        # Create frame for input and initialize input boxes
        frame_input = tk.Frame(canvas)
        frame_input.grid(row=1, column=0)
        canvas.create_window((0, 0), window=frame_input, anchor="nw")
        self.text_input = tk.Text(frame_input, height=400, width=200)
        self.text_input.grid(row=0, column=0)

        frame_input.update_idletasks()
        frame_canvas.config(width=200, height=400, padx=10, pady=10)
        canvas.config(scrollregion=canvas.bbox("all"))

        # Initialize memory frame
        self.memory_frame = tk.Frame(self.main_frame)

        # Load memory into frame
        memory_location = 0
        self.retreive_mem_contents = []
        for i in range(10):
            for j in range(10):
                mem_content = tk.Label(
                    self.memory_frame, text=self.memory[memory_location]
                )
                mem_content.grid(row=i + 1, column=j, padx=5, pady=5)
                self.retreive_mem_contents.append(mem_content)
                memory_location += 1
        self.memory_frame.grid(column=1, row=1)

        # Create the Load Memory Button
        self.load_memory_btn = tk.Button(
            self.main_frame, text="Load Memory", command=self.loadMemory
        )
        self.load_memory_btn.grid(row=2, columnspan=1, pady=10)

        # Create the Run Program Button
        self.run_program_btn = tk.Button(self.main_frame, text="Run Program")
        self.run_program_btn.grid(row=3, columnspan=1, pady=5)

        # Initialize Output Frame
        output_frame = tk.Frame(self.main_frame)
        tk.Label(output_frame, text="OUTPUT").grid(row=0, column=0)
        self.prog_output = tk.Label(output_frame, text="")
        self.prog_output.grid(row=1, column=0)
        output_frame.grid(row=2, column=1, rowspan=2)

        # Initialize all Register Frames
        register_frame = tk.Frame(self.main_frame)

        ir_frame = tk.Frame(register_frame)
        tk.Label(ir_frame, text="Instruction Register").grid(row=0)
        self.ir_label = tk.Label(ir_frame, text=self.instruction_register)
        self.ir_label.grid(row=1)
        ir_frame.grid(row=0, pady=10)

        ic_frame = tk.Frame(register_frame)
        tk.Label(ic_frame, text="Instruction Counter").grid(row=0)
        self.ic_label = tk.Label(ic_frame, text=self.instruction_counter)
        self.ic_label.grid(row=1)
        ic_frame.grid(row=1, pady=10)

        ac_frame = tk.Frame(register_frame)
        tk.Label(ac_frame, text="Accumulator").grid(row=0)
        self.ac_label = tk.Label(ac_frame, text=self.accumulator)
        self.ac_label.grid(row=1)
        ac_frame.grid(row=2, pady=10)

        opcode_frame = tk.Frame(register_frame)
        tk.Label(opcode_frame, text="Op Code").grid(row=0)
        self.opcode_label = tk.Label(opcode_frame, text=self.operation_code)
        self.opcode_label.grid(row=1)
        opcode_frame.grid(row=3, pady=10)

        operand_frame = tk.Frame(register_frame)
        tk.Label(operand_frame, text="Operand").grid(row=0)
        self.operand_label = tk.Label(operand_frame, text=self.operand)
        self.operand_label.grid(row=1)
        operand_frame.grid(row=4, pady=10)

        register_frame.grid(row=1, column=2, padx=10, pady=10)

        clear_all = tk.Button(
            self.main_frame, text="CLEAR ALL", command=self.clear_contents
        )
        clear_all.grid(row=2, column=2)

        # # Update memory when load Memory button is pressed
        # self.load_memory_btn.bind("<Button-1>", self.loadMemory)

        # Run the loaded Program when Run Program button is pressed
        self.run_program_btn.bind("<Button-1>", self.runProgram)

    def loadMemory(self):
        """When load memory button is pressed, the memory is updated with new values in the entry and loaded into the memory frame"""

        # Checks if inputs are valid words in BASIC ml
        new_memory = ["+0000"] * 100
        entry_list = self.text_input.get("1.0", "end").split("\n")
        entry_list.pop()
        for i in range(len(entry_list)):
            mem_input = entry_list[i]
            if mem_input != "":
                new_memory[i] = mem_input

        if self.M.checkMemory(new_memory) == 1:

            self.memory = new_memory

            self.M.clean_memory(self.memory)

            # Creates new memory frame with new memory values
            self.memory_frame.destroy()
            self.memory_frame = tk.Frame(self.main_frame)
            memory_location = 0
            self.retreive_mem_contents = []
            for i in range(10):
                for j in range(10):
                    mem_content = tk.Label(
                        self.memory_frame, text=self.memory[memory_location]
                    )
                    mem_content.grid(row=i + 1, column=j, padx=5, pady=5)
                    self.retreive_mem_contents.append(mem_content)
                    memory_location += 1
            self.memory_frame.grid(column=1, row=1)

    def runProgram(self, event):
        """When the run program button is pressed, the memory is ran as the program"""

        C = Controller(
            self.memory,
            self.instruction_counter,
            self.instruction_register,
            self.operation_code,
            self.operand,
            self.accumulator,
            self.big_storage,
        )

        # Return an array of updated values from the Controller
        C.run_instructions()

        # Update registers with new values
        self.memory = C.memory
        self.instruction_counter = C.instruction_counter
        self.instruction_register = C.instruction_register
        self.operation_code = C.operation_code
        self.operand = C.operand
        self.accumulator = C.accumulator
        self.big_storage = C.big_storage

        # Prints the output array to the output field
        self.updateWindow(C.output)

    def browseFiles(self):
        """ Allows user to browse files and select .txt file"""

        MsgBox = tk.messagebox.askquestion(
            "Clear Input",
            "Opening a new file will delete the current written contents:\nAre you sure you want to continue?",
        )
        if MsgBox == "yes":
            # Clear contents of text for new content
            self.text_input.delete("1.0", "end")

            # Opens file explorer to select file
            filename = filedialog.askopenfilename(
                initialdir="/",
                title="Select a File",
                filetypes=(("Text files", "*.txt*"), ("all files", "*.*")),
            )

            # Reads the file and writes the content to the text entry frame
            with open(filename, "r") as f:
                input_file = f.read()
                self.text_input.insert("1.0", input_file)

    def saveFile(self):
        """ Saves the contents of the input text area to a .txt file"""

        export = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt*"), ("all files", "*.*")),
        )
        with open(export, "w") as f:
            f.write(self.text_input.get("1.0", "end"))

    def helpButton(self):
        """ Suplies an overview of the UVsim"""
        messagebox.showinfo(
            "?",
            f"""Overview: -The UVSim is a Graphical User Interface software simulator created by us over at IED (Innovative EDucation). Universities typically have a course where computer science students learn to work with registers and very low level coding, so this simulator allows for a simple and effective machine language environment. UVSIM works with a language called BasicML, which consists of instructions written in a signed four-digit decimal number, such as +1050, -5768, etc. UVSim has a 100-word memory, which are referenced by the last two digits of whatever command is entered. The BasicML program must be loaded into main memory starting at location 00 before running the program. The UVSim contains a CPU, register, and main memory. There is also an accumulator, which is what we will use to do different arithmetic or move around numbers in various ways. Each instruction (signed four-digit decimal number) occupies one word of the 100 word UVSim memory. Each slot may contain one of these instructions, or a data value that is placed inside one of the memory slots to be worked with.

            The first two digits of each instruction are the operation code specifying the operation to be performed, which will be explained in the Features section.

            The last two digits of each instruction are the operand, the address of the memory location containing the word we will be operating with.

            Features: Here is a list of the operations that can be performed (Based on the first two digits of the signed four digit instruction). I/O operation:

            READ = 10 Read a word from the keyboard into a specific location in memory. WRITE = 11 Write a word from a specific location in memory to screen. Load/store operations: LOAD = 20 Load a word from a specific location in memory into the accumulator. STORE = 21 Store a word from the accumulator into a specific location in memory. Arithmetic operation: Add = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator) SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator) DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator). MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator). Control operation: BRANCH = 40 Branch to a specific location in memory BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative. BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero. HALT = 43 Pause the program Ending the Program / Output: Along with all of these operations that can be performed, the UVSim will complete once it has either ran through all 100-word memory slots, or if the command -99999 is entered. Use -99999 if you can to end the program at a quicker speed. Once the input is done being read, it will be checked for validity to make sure there are no commands that are invalid and dont follow the signed four digit decimal number format. The program will be ran to completion and output the following: Registers:

            Accumulator Instruction Counter (Counts the number of instructions ran in your program) Instruction Register (Contains the last instruction read by your program before completion) Operation Code (Contains the last operation code read by your program before completion) Operand (Contains the last operand read by your program before completion) Memory:

            When you are storing an integer into a memory slot in the data range of 0-99, you are able to store an integer of size -9999 to 9999. When you are performing arithmetic, there is a higher range available of -999999 to 999999. Whenever an integer in a memory location is lower than -9999 or higher than 9999, the respective -9999 or +9999 are shown in the memory. However, when you pull the integer from those locations, it will contain the respective integer that is higher or lower than those values that had previously been stored. This is done to maintain simplicity in the formatting of the 100 slots of memory, along with hinting to the user that the memory location contains a number that is greater than 4 digits:

            Memory will be printed out in a table format, with each of the instructions in the correct memory locations that they were assigned. If there was an integer number stored in a memory-word location, then it will be converted to the format that the instructions are. If the integer is negative, it will have a '-' sign in front, and if it is a positive integer it will have a '+' sign like the other instructions. Conclusion:

            For testing perposes the input value that is required to run the read function for the user input is +0005.

            All of this will be presented in a GUI type environment. We hope this provides a solid work environment for each of your students at your university/college and that it will help them come to a stronger understanding of how to work with registers, along with how to work with a low-level language like BasicML.""",
        )

    def updateWindow(self, lyst):
        """Takes the array of outputs from the controller class and
        loads it into the Output array"""

        # Updates registers and output field
        self.prog_output.config(text=lyst)
        self.ir_label.config(text=self.instruction_register)
        self.ic_label.config(text=self.instruction_counter)
        self.ac_label.config(text=self.accumulator)
        self.opcode_label.config(text=self.operation_code)
        self.operand_label.config(text=self.operand)

        # Updates memory frame with new values after run program is pressed
        self.memory_frame.destroy()
        self.memory_frame = tk.Frame(self.main_frame)
        memory_location = 0
        self.retreive_mem_contents = []
        for i in range(10):
            for j in range(10):
                mem_content = tk.Label(
                    self.memory_frame, text=self.memory[memory_location]
                )
                mem_content.grid(row=i + 1, column=j, padx=5, pady=5)
                self.retreive_mem_contents.append(mem_content)
                memory_location += 1
        self.memory_frame.grid(column=1, row=1)

    def clear_contents(self):
        """ Clears contents of input and memory"""

        MsgBox = tk.messagebox.askquestion(
            "Clear all",
            "This will clear the contents of all input and memory:\nAre you sure you want to continue?",
        )
        if MsgBox == "yes":
            # Clear contents of text for new content
            self.text_input.delete("1.0", "end")

            self.loadMemory()
