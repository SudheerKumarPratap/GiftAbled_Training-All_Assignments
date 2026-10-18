class BankAccount:

    def __init__(self,owner,balance):
        self.owner = owner
        self.__balance = balance  # private  attribute
    def get_balance(self):
        return self.__balance
        
    def deposit(self,amount):
        if amount>0:
            self.__balance += amount
            print(f"Deposited ₹{amount}.\nYour A/C balance now:₹ {self.__balance:.2f}")
        else:      
            print("Invalid")
    def withdraw(self,withdrawn_amount):
        
        if withdrawn_amount<= self.__balance:
            self.__balance -= withdrawn_amount
            print(f"withdrawn ₹{withdrawn_amount}.\nYour A/C balance now:₹ {self.__balance:.2f}")           
        else:
            print("your A/c Balance can't be Negative")
            
          
ba=BankAccount("A",0)
print(f"Initial balance:{ba.get_balance():.2f}")

print(ba.owner)

#print(ba.__balance) # accessing private data directly fails
d=int(input("Enter deposit amount:"))
ba.deposit(d)
w=int(input("Enter withdrawn amount:"))
ba.withdraw(w)
#print(ba.get_balance()) 
