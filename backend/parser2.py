def convert_to_format(input_str, filename, times):
    # Format the input string with single quotes
    formatted_str = "', '".join([input_str] * times)
    
    # Add the single quotes at the beginning and end
    result = f"'{formatted_str}'"
    
    # Write the result to a file
    with open(filename, 'w') as file:
        file.write(result)

# Example usage
input_str = "1"
filename = "output2.txt"
times = 2698  # Specify how many times you want the string to be repeated
convert_to_format(input_str, filename, times)

print(f"Output written to {filename}")
