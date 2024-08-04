# logic_gates

print("""
  @@@\           @@@@@@@@        @@@@@@@@      @@@@@@@@@@@@\    @@@@@@@@@@@
  @@@ \         @@@@@@@@@@      @@@@@@@@@@     @@@@@@@@@@@@ \  @@@@@@@@@@@@@\ 
  @@@ |        @@@   ___@@@\   @@@  _______\   \___@@@@  ___|  @@@   ____@@@ \ 
  @@@ |        @@@  /   @@@ \  @@@ | @@@@@@\       @@@@ |      @@@  |    \___|
  @@@ |        @@@ |    @@@ |  @@@ | @@@@@@ \      @@@@ |      @@@  |
  @@@ |        @@@ |    @@@ |  @@@ | \__@@@ |      @@@@ |      @@@  |        
  @@@ |        @@@ |    @@@ |  @@@ |    @@@ |      @@@@ |      @@@  |    @@@\ 
  @@@@@@@@@\    @@@@@@@@@@  /   @@@@@@@@@@  /  @@@@@@@@@@@@\   @@@@@@@@@@@@@ \ 
  @@@@@@@@@ \    @@@@@@@@  /     @@@@@@@@  /   @@@@@@@@@@@@ \   @@@@@@@@@@@  /
  \_________|     \_______/       \_______/    \____________|    \__________/
     
    logic gates simulator in Python
     
    LGSiPy@Python:3.11.4
  
  
  
  you can use the library like this:
  1) don't write " import LGSIPY ",
  @1) you should write " from LGSIPY import DataBase ".
  2) after make any operator (a, b, c ,…):
  @2) {{ THE OPERATOR SHOULD BE LIKE THIS: (operator) = int(input('your text'))}}
    """)

class DataBase:
    @staticmethod
    def wire(x):
        if x == 0:
            return f"${x}"
        elif x == 1:
            return f"${x}"
        else:
            return 'error'
    
    @staticmethod
    def OR(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${1 if x + y > 0 else 0}"
    
    @staticmethod
    def XOR(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${x ^ y}"
    
    @staticmethod
    def NOR(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${0 if x + y > 0 else 1}"
    
    @staticmethod
    def NXOR(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${1 if x == y else 0}"
    
    @staticmethod
    def AND(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${x & y}"
    
    @staticmethod
    def NAND(x, y):
        if (x < 0 or x > 1) or (y < 0 or y > 1):
            return 'error'
        return f"${0 if x & y == 1 else 1}"
    
    @staticmethod
    def NOT(x):
        if (x < 0 or x > 1):
            return 'error'
        return f"${0 if x == 1 else 1}"