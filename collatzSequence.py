#callatzSequence.py
def callatz_sequenceProg(n):
    if n<=00:
        return None
    sequence = [n]

    while n > 1:
        if n% 2 == 0:
            n = n//2 
        else  :
            n = n*3 +1
        sequence.append(n) 
    return sequence
tt = int(input("Start_Number:"))

result =callatz_sequenceProg(tt)
print(f"Callatz_Sequence for {tt}:{result}")

            

    