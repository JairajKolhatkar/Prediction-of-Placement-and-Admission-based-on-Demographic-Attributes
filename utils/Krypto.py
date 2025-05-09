import hashlib


def generate_sum(key):
    num_lst = []
    for i in key:
        if i.isnumeric():
            num_lst.append(int(i))
    return sum(num_lst)


def replace_letters(key, A, B):
    c = A+B
    c_hash = list(hashlib.sha512(str(c).encode()).hexdigest())
    replacable_letter = []
    for i in key:
        if i in c_hash:
            replacable_letter.append(str(ord(i)))
    return "".join(replacable_letter), generate_sum(c_hash)


def hash_generator(key):
    result = hashlib.sha512(key.encode())
    hashed = result.hexdigest()
    sha_num_sum = ""
    num_sum = generate_sum(hashed)
    if num_sum % 2 == 0:
        sha_num_sum = hashlib.sha512(
            (str(num_sum)).encode()).hexdigest()
    else:
        sha_num_sum = hashlib.sha256(
            (str(num_sum)).encode()).hexdigest()

    num_sum_two = generate_sum(sha_num_sum)

    if num_sum_two % len(str(sha_num_sum)) == 0:
        added_hash = hashed+sha_num_sum
    else:
        added_hash = sha_num_sum+hashed

    replace_letters_op_string, D = replace_letters(
        added_hash, num_sum, num_sum_two)

    replace_letters_hash = hashlib.sha512(
        (str(replace_letters_op_string)).encode()).hexdigest()

    divisor = len(replace_letters_hash)+num_sum+num_sum_two
    divisor_hash = hashlib.sha512(str(divisor).encode()).hexdigest()

    divisor_division = len(str(divisor))

    if D % divisor_division == 0:
        return added_hash+replace_letters_hash+divisor_hash
    if D % divisor_division == 3:
        return replace_letters_hash+divisor_hash+added_hash
    if D % divisor_division == 5:
        return added_hash+divisor_hash+replace_letters_hash
    return divisor_hash+replace_letters_hash+added_hash
