import tkinter as tk
from tkinter import messagebox

"""The Model manages the data and defines rules and behaviors, it represents 
    the business logic of the application"""

class Memory:
    def __init__(self, memory):
        """Constructer call to initialize attributes of the memory class"""
        self.memory = memory

    def checkMemory(self, memory):
        """Checks if memory input is valid.  returns 1 if valid, 0 if not"""

        check = 1
        index = 0
        while index < len(memory):
            number = memory[index]
            if len(number) != 5:  # Checks if length of instruction is correct
                messagebox.showinfo("!", f"{number} is not a valid word")
                check = 0
                return check
            elif number[0] not in (
                "+",
                "-",
            ):  # Checks if instruction contain a + or -
                messagebox.showinfo("!", f"{number} is not a valid word")
                check = 0
                return check
            else:
                check = 1
            index += 1
        return check

    def clean_memory(self, memory):
        """Clears all memory locations that have be alocated a word"""
        index = 0
        while index < len(memory):
            number = memory[index]
            memory[index] = str(number)
            index += 1
        return memory
        