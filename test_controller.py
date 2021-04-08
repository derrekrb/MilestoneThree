import unittest
from controller import Controller

class testController(unittest.TestCase):
    
    def test_add(self):
        memory = [0000] * 100
        memory[5] = 5
        con = Controller(memory,0,0,0,0,0)
        self.assertEqual(con.add(5), 5)
        self.assertEqual(con.add(5), 10)
        
    def test_subtract(self):
        memory = [0000] * 100
        memory[5] = 5
        con = Controller(memory,0,0,0,0,0)
        self.assertEqual(con.subtract(5), -5)
        self.assertEqual(con.subtract(5), -10)
        
    def test_multiply(self):
        memory = [0000] * 100
        memory[5] = 5
        con = Controller(memory,0,0,0,0,0)
        self.assertEqual(con.multiply(5), 0)
        con.accumulator = 6
        self.assertEqual(con.multiply(5), 30)
        
    def test_divide(self):
        memory = [0000] * 100
        memory[10] = 2
        con = Controller(memory,0,0,0,0,0)
        self.assertEqual(con.divide(10), 0)
        con.accumulator = 10
        self.assertEqual(con.divide(10), 5)
        
    def test_read(self):
        pass
    
    def test_write(self):
        pass
    
    def test_load(self):
        memory = [0000] * 100
        con = Controller(memory,0,0,0,0,0)
        con.memory[23] = 50
        con.load(23)
        self.assertEqual(con.accumulator, 50)
        con.memory[40] = 99
        con.load(40)
        self.assertEqual(con.memory[40], 99)
    
    def test_store(self):
        memory = [0000] * 100
        con = Controller(memory,0,0,0,0,0)
        con.accumulator = 23
        con.store(30)
        self.assertEqual(con.memory[30], 23)
        con.accumulator = 40
        con.store(30)
        self.assertEqual(con.memory[30], 40)
        
    def test_branch_neg(self):
        memory = [0000] * 100
        con = Controller(memory,0,0,0,0,0)
        self.accumulator = 5
        self.assertEqual(con.branch_neg(), False)
        con.accumulator = 10
        self.assertEqual(con.branch_neg(), False)
        con.accumulator = -10
        self.assertEqual(con.branch_neg(), True)
        
    def test_branch_zero(self):
        memory = [0000] * 100
        con = Controller(memory,0,0,0,0,0)
        self.assertEqual(con.branch_zero(), True)
        con.accumulator = 10
        self.assertEqual(con.branch_zero(), False)
        con.accumulator = -10
        self.assertEqual(con.branch_zero(), False)
        
    def test_run_instructions(self):
        memory = [0000] * 100
        memory[0] = 1007
        memory[1] = 1008
        memory[2] = 2007
        memory[3] = 3008
        memory[4] = 2109
        memory[5] = 4300
        con = Controller(memory,0,0,0,0,0)
        self.assertIsInstance(con.accumulator, int)
        self.assertIsInstance(con.operation_code, int)
        self.assertIsInstance(con.memory, list)
        self.assertIsInstance(con.instruction_counter, int)
        
if __name__ == "__main__":
    unittest.main()