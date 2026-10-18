def multiplication_grid(size):
    print("   ", end = "")
    for col in range (1,size +1):
        print(f"{col:4}", end ="")
    print("\n" + "----" *(size+1))

        # print each row of  the grid
    for row in range (1,size +1):
        print(f"{row:2}|", end ="")  
        for col in range (1,size +1):
            print(f"{row*col:4}", end ="")
        print() 
mg= int(input("Multiplication Grid:"))
print(multiplication_grid(mg))              