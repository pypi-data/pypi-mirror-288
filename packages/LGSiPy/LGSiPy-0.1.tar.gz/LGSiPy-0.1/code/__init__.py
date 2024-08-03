print(f"""
 @@@\           @@@@@@@@        @@@@@@@@      @@@@@@@@@@@@\    @@@@@@@@@@@
 @@@ \         @@@@@@@@@@      @@@@@@@@@@     @@@@@@@@@@@@ \  @@@@@@@@@@@@@\ 
 @@@ |        @@@   ___@@@\   @@@  _______\   \___@@@@  ___|  @@@   ____@@@ \ 
 @@@ |        @@@  /   @@@ \  @@@ | @@@@@@\       @@@@ |      @@@  |    \___|
 @@@ |        @@@ |    @@@ |  @@@ | @@@@@@ \      @@@@ |      @@@  |
 @@@ |        @@@ |    @@@ |  @@@ |    @@@ |      @@@@ |      @@@  |        
 @@@ |        @@@ |    @@@ |  @@@ |    @@@ |      @@@@ |      @@@  |    @@@\ 
 @@@@@@@@@\    @@@@@@@@@@  /   @@@@@@@@@@  /  @@@@@@@@@@@@\   @@@@@@@@@@@@@ \ 
 @@@@@@@@@ \    @@@@@@@@  /     @@@@@@@@  /   @@@@@@@@@@@@ \   @@@@@@@@@@@  |
 \_________|     \_______/       \_______/    \____________|    \___________/
 
 logic gates simulator in Python
 
 LGSiPy@Python:3.11.4

""")
gate = int(input('''the available gates:
1. wire
2. OR
3. XOR
4. NOR
5. NXOR
6. AND
7. NAND
8. NOT

what do you want?
~ '''))


class DataBase:
    def wire(x):
        if x == 0:
            print('$',x)
        elif x == 1:
            print('$',x)
        elif x != 0 or 1:
            print('error')
    def OR(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',0)
            print('')
        elif x == 1 and y == 0:
            print('$',x + y)
            print('')
        elif x == 0 and y == 1:
            print('$',x + y)
            print('')
        elif x == 1 and y == 1:
            print('$',1)
            print('')
            
    def XOR(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',0)
            print('')
        elif x == 1 and y == 0:
            print('$',x + y)
            print('')
        elif x == 0 and y == 1:
            print('$',x + y)
            print('')
        elif x == 1 and y == 1:
            print('$',0)
            print('')
            
    def NOR(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',1)
            print('')
        elif x == 1 and y == 0:
            print('$',0)
            print('')
        elif x == 0 and y == 1:
            print('$',0)
            print('')
        elif x == 1 and y == 1:
            print('$',0)
            print('')
            
    def NXOR(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',1)
            print('')
        elif x == 1 and y == 0:
            print('$',0)
            print('')
        elif x == 0 and y == 1:
            print('$',0)
            print('')
        elif x == 1 and y == 1:
            print('$',1)
            print('')
            
    def AND(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',0)
            print('')
        elif x == 1 and y == 0:
            print('$',0)
            print('')
        elif x == 0 and y == 1:
            print('$',0)
            print('')
        elif x == 1 and y == 1:
            print('$',1)
            print('')
            
    def NAND(x, y):
        if (x < 0 or x > 1) and (y < 0 or y >1):
            print('')
            print('error')
            print('')
        if x == 0 and y == 0:
            print('$',1)
            print('')
        elif x == 1 and y == 0:
            print('$',1)
            print('')
        elif x == 0 and y == 1:
            print('$',1)
            print('')
        elif x == 1 and y == 1:
            print('$',0)
            print('')
    
    def NOT(x):
        if (x < 0 or x > 1):
            print('')
            print('error')
            print('')
        if x == 0:
            print('$',1)
        if x == 1:
            print('$',0)
#close DataBase





if (gate == 1):
    print('')
    print('wire')
    print('')
    while True:
        print('input: 0 / 1 only')
        x = int(input('~ '))
        
        DataBase.wire(x)
            
elif (gate == 2):
    print('')
    print('OR')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.OR(x, y)
elif (gate == 3):
    print('')
    print('XOR')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.XOR(x, y)
elif (gate == 4):
    print('')
    print('NOR')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.NOR(x, y)
elif (gate == 5):
    print('')
    print('NXOR')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.NXOR(x, y)
elif (gate == 6):
    print('')
    print('AND')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.AND(x, y)
elif (gate == 7):
    print('')
    print('NAND')
    print('')
    while True:
        print('input@x: 0 / 1 only')
        x = int(input('~ '))
        print('input@y: 0 / 1 only')
        y = int(input('~ '))
        
        DataBase.NAND(x, y)
elif (gate == 8):
    print('')
    print('NOT')
    print('')
    while True:
        print('input: 0 / 1 only')
        x = int(input('~ '))
        
        DataBase.NOT(x)
else:
    print('ERROR: Invalid Operation!!')