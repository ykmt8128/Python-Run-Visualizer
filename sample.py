def test():
    for i in range(1, 4):
        print("LOOP", i)
    
        if i % 2 == 0:
            print("EVEN")
        else:
            print("ODD")

print("START")
test()
print("END")