def int_to_codeword_vec(val: int, num_bits: int) -> list[int]:
    return list(
            [(val >> i) & 1 for i in range(num_bits)]
        )

def print_stats(old: int, new: int) -> None:
    print(f"We can now represent {new} distinct values.")
    print(f"\tValues Reduced:\t{old - new}")
    print(f"\t% Reduction:\t{(1 - (new/old)) * -100:.2f}%")
    print()

def calculate_first_invariant(codeword: list[int]) -> int:
    total_sum = 0
    
    # Iterate over the codeword in reverse (starting from the LSB)
    for i in range(0, len(codeword)):
        if codeword[i] == 1:
            # Add 1 for each 1-bit
            total_sum += 1
        elif codeword[i] == 0:
            # Subtract 1 for each 0-bit
            total_sum -= 1
            
    return total_sum

def calculate_second_invariant(codeword: list[int]) -> int:
    total_sum = 0
    
    # Use range to iterate through indices from 0 to 15
    # We account for 0-based indexing inside the loop during the arithmetic
    for i in range(0, len(codeword)):
        if codeword[i] == 1:
            # If the bit is 1, add its index to the sum
            total_sum += i + 1
        elif codeword[i] == 0:
            # If the bit is 0, subtract its index from the sum
            total_sum -= i + 1
            
    return total_sum

def embedded_value(codeword: list[int]) -> int:
    return calculate_second_invariant(codeword[:len(codeword) // 2]) >> 1

def mirror_property(codeword: list[int]) -> bool:
    for i in range(0, len(codeword) // 2):
        if codeword[i] != codeword[len(codeword)-1-i]:
            return False

    return True

def complementation_property(codeword: list[int]) -> bool:
    return embedded_value(codeword) == -embedded_value([0 if b else 1 for b in codeword])

if __name__ == "__main__":
    CODEWORD_LENGTH = 16

    codewords = list(map(lambda v: int_to_codeword_vec(v, CODEWORD_LENGTH), range(1 << CODEWORD_LENGTH)))

    print(f"{CODEWORD_LENGTH} bits can represent {len(codewords)} values.")
    print("We will now apply invariants and properties to find what codewords we can really use.")
    print()
    
    old_count = len(codewords)
    codewords = list(filter(lambda c: calculate_first_invariant(c) == 0, codewords))
    new_count = len(codewords)
    print("Applied First Invariant...")
    print_stats(old_count, new_count)

    old_count = len(codewords)
    codewords = list(filter(lambda c: calculate_second_invariant(c) == 0, codewords))
    new_count = len(codewords)
    print("Applied Second Invariant...")
    print_stats(old_count, new_count)

    old_count = len(codewords)
    codewords = list(filter(mirror_property, codewords))
    new_count = len(codewords)
    print("Applied Mirror Property...")
    print_stats(old_count, new_count)

    old_count = len(codewords)
    codewords = list(filter(complementation_property, codewords))
    new_count = len(codewords)
    print("Applied Complementation Property...")
    print_stats(old_count, new_count)

    for codeword in codewords:
        complement = [0 if b else 1 for b in codeword]
        print(f"{embedded_value(codeword):2d} -> {''.join(map(str, codeword))}\t~complement~>\t{''.join(map(str, complement))} -> {embedded_value(complement):2d}")
