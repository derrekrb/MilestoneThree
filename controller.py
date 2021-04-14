import tkinter as tk
from tkinter import simpledialog
from model import Memory
from tkinter import messagebox


class Controller:
    """accepts user’s inputs and delegates data representation to a View and data handling to a Model."""

    def __init__(
        self,
        memory,
        instruction_counter,
        instruction_register,
        operation_code,
        operand,
        accumulator,
        big_storage
    ):
        """Constructor call to initialize attributes of the Controller class"""
        self.memory = memory
        self.instruction_counter = instruction_counter
        self.instruction_register = instruction_register
        self.operation_code = operation_code
        self.operand = operand
        self.accumulator = accumulator
        self.big_storage = big_storage

        self.output = []

        m = Memory(self.memory)
        m.clean_memory(self.memory)

    def add(self, memory_location):
        """Adds a number from a specific location in memory to the number in the accumulator."""
        memory_value = int(self.memory[memory_location])
        
        if (memory_value == 9999 or memory_value == -9999):
            memory_value = self.big_storage[memory_location]

        self.accumulator += memory_value
        self.accumulator = int(self.accumulator)
        if self.accumulator > 999999 or self.accumulator < -999999:
            if self.accumulator > 999999:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed max value of 999999. 999999 is loaded into the accumulator",
                )
                self.accumulator = 999999
            else:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed min value of -999999. -999999 is loaded into the accumulator",
                )
                self.accumulator = -999999

        return int(self.accumulator)

    def subtract(self, memory_location):
        """Subtracts a number from a specific location in memory from the number in the accumulator."""
        memory_value = int(self.memory[memory_location])
        
        if (memory_value == 9999 or memory_value == -9999):
            memory_value = self.big_storage[memory_location]
        
        self.accumulator -= memory_value
        self.accumulator = int(self.accumulator)
        if self.accumulator > 999999 or self.accumulator < -999999:
            if self.accumulator > 999999:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed max value of 999999. 999999 is loaded into the accumulator",
                )
                self.accumulator = 999999
            else:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed min value of -999999. -999999 is loaded into the accumulator",
                )
                self.accumulator = -999999

        return int(self.accumulator)

    def multiply(self, memory_location):
        """Multiplies a number from a specific memory location to the number in the accumulator
        and returns the accumulator"""

        memory_value = int(self.memory[memory_location])
        
        if (memory_value == 9999 or memory_value == -9999):
            memory_value = self.big_storage[memory_location]
        
        self.accumulator *= memory_value
        self.accumulator = int(self.accumulator)
        if self.accumulator > 999999 or self.accumulator < -999999:
            if self.accumulator > 999999:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed max value of 999999. 999999 is loaded into the accumulator",
                )
                self.accumulator = 999999
            else:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed min value of -9999. -9999 is loaded into the accumulator",
                )
                self.accumulator = -999999

        return int(self.accumulator)

    def divide(self, memory_location):
        """Divides the number in the accumulator by a number from a specific location in memory
        and returns the accumulator."""

        memory_value = int(self.memory[memory_location])
        
        if (memory_value == 9999 or memory_value == -9999):
            memory_value = self.big_storage[memory_location]
        
        self.accumulator /= memory_value
        self.accumulator = int(self.accumulator)
        if self.accumulator > 999999 or self.accumulator < -999999:
            if self.accumulator > 999999:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed max value of 999999. 999999 is loaded into the accumulator",
                )
                self.accumulator = 999999
            else:
                messagebox.showinfo(
                    "!",
                    "Accumulator exceed min value of -9999. -9999 is loaded into the accumulator",
                )
                self.accumulator = -999999

        return int(self.accumulator)

    def read(self, memory_location):
        """Asks the user for an integer and puts it into a specific location in memory"""

        valid = False
        while not valid:
            user_input = simpledialog.askstring(
                "Input",
                "Enter an integer between -9999 and +9999\n(Format must be +0000)",
            )
            try:
                user_input = int(user_input)
            except ValueError:
                messagebox.showinfo(
                    "!", "Input must be a integer between -9999 and +9999"
                )
            except TypeError:
                messagebox.showinfo(
                    "!", "Input must be a integer between -9999 and +9999"
                )
            else:
                if user_input > 9999 or user_input < -9999:
                    messagebox.showinfo(
                        "!", "Input must be a integer between -9999 and +9999"
                    )

                else:
                    user_input = str(user_input)
                    user_input = "+" + user_input.zfill(
                        4
                    )  # Formats input to be the same as memory format
                    self.memory[memory_location] = user_input
                    valid = True
        return user_input

    def write(self, memory_location):
        """Prints the contents of the given memory location to the screen"""

        if (self.memory[memory_location] == "+9999" or self.memory[memory_location] == "-9999"):
            self.output.append(self.big_storage[memory_location])
            return self.big_storage[memory_location]
        else:
            self.output.append(self.memory[memory_location])
            return self.memory[memory_location]


    def load(self, memory_location):
        """ Will take a memory location and load what ever is there into the accumulator  """
        if (self.memory[memory_location] == "+9999" or self.memory[memory_location] == "-9999"):
            self.accumulator = self.big_storage[memory_location]
        else:
            self.accumulator = int(self.memory[memory_location])
        return

    def store(self, memory_location):
        """ Will take whatever is in the accumulator and will store it in the given location """
        if self.accumulator > 9999:
            self.big_storage[memory_location] = self.accumulator
            self.memory[memory_location] = "+9999"
        elif self.accumulator < -9999:
            self.big_storage[memory_location] = self.accumulator
            self.memory[memory_location] = "-9999"
        else:
            self.memory[memory_location] = self.accumulator
        return

    def branch_neg(self):
        """Will return True if the accumulator is less than zero, otherwise will return False"""

        if self.accumulator < 0:
            return True
        else:
            return False

    def branch_zero(self):
        """Will return True if the accumulator is equal to zero, otherwise will return False"""

        if self.accumulator == 0:
            return True
        else:
            return False

    def run_instructions(self):
        """Runs the program written into the memory"""

        self.instruction_counter = 0
        self.accumulator = 0

        index = 0
        while index < (len(self.memory) - 1):

            op = int(self.memory[index][1:3])
            memory_location = int(self.memory[index][3:5])

            if op == 10:
                self.read(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 11:
                self.write(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 20:
                self.load(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 21:
                self.store(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 30:
                self.add(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 31:
                self.subtract(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 32:
                self.divide(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 33:
                self.multiply(memory_location)
                index += 1
                self.instruction_counter += 1
            elif op == 40:
                index = memory_location
                self.instruction_counter += 1
            elif op == 41:
                if self.branch_neg() is True:
                    index = memory_location
                    self.instruction_counter += 1
                else:
                    index += 1
            elif op == 42:
                if self.branch_zero() is True:
                    index = memory_location
                    self.instruction_counter += 1
                else:
                    index += 1
            elif op == 43:  # Halt the program
                self.instruction_counter += 1
                self.operation_code = op
                self.operand = memory_location
                break

            else:
                self.instruction_counter += 1
                self.instruction_register = self.memory[index]
                self.operation_code = op
                self.operand = memory_location
                index += 1

            self.instruction_register = self.memory[index]
            self.operation_code = op
            self.operand = memory_location

