def be_palindrome_simple(data):
# convert data into string so that  data can be used  for string and numbers 
    data_str = str(data)
    return data_str  ==  data_str [::-1]
print(be_palindrome_simple("radar"))
print(be_palindrome_simple("12321"))
print(be_palindrome_simple(12345432))





    