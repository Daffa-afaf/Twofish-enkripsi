import math

# Operasi dalam finite field GF(256)

def GF256multiply(A, B): # Perkalian dalam finite field GF(256)
    p = 0
    # V is the primitve polynomial
    V = 283
    for counter in range(8):
        if (B & 1) == 1:
            p ^= A
        A = A << 1 # geser a ke kiri

        if A >= 256:
            A = A ^ V
        B = B >> 1 # geser B satu ke kiri

    return p

def GF256matrixmultiply(A, B): # Perkalian matriks dalam GF(256)
    C = []
    for i in range(len(A)):
        C.append([])
        for l in range(len(B[0])):
            a = 0
            for j in range(len(A[i])):
                a = a ^ (GF256multiply(A[i][j], B[j][l]))
            C[i].append(a)

    return C

def matrixmultiply(A, B): # Perkalian matriks biasa
    C = []
    for i in range(len(A)):
        C.append([])
        for l in range(len(B[0])):
            a = 0
            for j in range(len(A[i])):
                a = a + (A[i][j] * B[j][l])
            C[i].append(a)

    return C

def transpose_matrix(A): # Transposisi matriks
    T = []
    for i, element in enumerate(A[0]):
        T.append([])
        for l, line in enumerate(A):
            T[i].append(line[i])

    return T

# mengonversi daftar nilai ke dalam format vektor/matriks
def transpose_vector(A):
    T = []
    for i, M in enumerate(A):
        T.append([int(M, 2)])

    return T

def ROL(number, rotdist, bit_length):
    a = pad_number(number, bit_length)
    for i in range(rotdist):
        b = ''
        for l in range(bit_length - 1):
            b = b + a[l + 1]
        b = b + a[0]
        a = b

    # print a
    return int(a, 2)

def ROR(number, rotdist, bit_length):
    a = pad_number(number, bit_length)
    for i in range(rotdist):
        b = ''
        b = b + a[bit_length - 1]
        for l in range(bit_length - 1):
            b = b + a[l]
        a = b

    # print a
    return int(a, 2)

# melakukan transformasi pseudo-hamilton
def PHT(a, b):
    a = int(a, 2)
    b = int(b, 2)

    A = (a + b) % pow(2, 32)
    B = (a + (2 * b)) % pow(2, 32)

    return [A, B]

# mengubah string ke angka
def pwdtokey(password):
    numbers = []

    for letter in password:
        numbers.append(ord(letter))

    pwdsum = 1
    for i in numbers:
        pwdsum *= i

    return pwdsum

# mengubah angka kembali menjadi teks
def num2text(number):
    binnumberlist = pad_number(number, 8)
    text = ''

    for i, binnumber in enumerate(binnumberlist):
        number = int(binnumber, 2)
        letter = chr(number)
        text = text + letter

    return text

# mengubah teks menjadi angka
def text2num(text):
    result = ''

    for lett in text:
        number = ord(lett)

        result = result + pad_number(number, 8)

    return int(result, 2)

# memasukkan angka ke sejumlah bit tertentu dan mengubahnya menjadi biner
def pad_number(number, pad_val):
# jika angka input kurang dari 32 bit
# kode mengembalikan string biner 32 bit
# jika angka lebih dari 32 bit, maka
# mengembalikan daftar bilangan bulat 32 bit
    number = bin(number)[2:]
    startlen = len(number)

    if startlen < pad_val:
        padinglen = pad_val - startlen
        padstring = '0' * padinglen
        number = padstring + number

    elif startlen > pad_val:
        units = int(startlen / pad_val)
        extrabit = pad_val - (startlen % pad_val)
        pading = '0' * extrabit
        binnumber = pading + number
        number = []        
        for i in range(units + 1):
            number.append(binnumber[0:pad_val])
            binnumber = binnumber[pad_val:]

    return number


################################
##### fungsi utama twofish #####
################################

# Fungsi H mengambil kata 32 bit dan daftar kata 32 bit
# dan menghasilkan satu kata 32 bit. Jumlah putaran
# bergantung pada panjang daftar. Ada 2=>4 langkah q box/L XOR
# di mana kata dibagi menjadi 4 kata 8 bit yang masing-masing dilewatkan
# melalui kotak q0 atau q1 tergantung pada putarannya. Kata-kata tersebut kemudian
# digabungkan kembali menjadi kata 32 bit dan di-XOR dengan elemen L.
# Langkah terakhir adalah set akhir kotak q0/q1 dan kemudian kata 8 bit yang dihasilkan
# diubah menjadi vektor dan matriks dikalikan dengan
# matriks MDS di bidang GF(2^8)
def H_function(W, L, MDS):
    # jika ada empat kata dalam L, lakukan putaran pertama h
    # dengan L3. Putaran 1
    if len(L) > 3:
        w1 = int(W[0:8], 2)
        w2 = int(W[8:16], 2)
        w3 = int(W[16:24], 2)
        w4 = int(W[24:32], 2)

        w1 = q1(w1)
        w2 = q0(w2)
        w3 = q0(w3)
        w4 = q1(w4)

        w1 = pad_number(w1, 8)
        w2 = pad_number(w2, 8)
        w3 = pad_number(w3, 8)
        w4 = pad_number(w4, 8)

        W = w1 + w2 + w3 + w4

        W = int(W, 2) ^ int(L[3], 2)

        W = pad_number(W, 32)

    # jika ada tiga kata atau lebih dalam L, lakukan putaran pertama h
    # dengan L2. Putaran 2
    if len(L) > 2:
        w1 = int(W[0:8], 2)
        w2 = int(W[8:16], 2)
        w3 = int(W[16:24], 2)
        w4 = int(W[24:32], 2)

        w1 = q0(w1)
        w2 = q0(w2)
        w3 = q1(w3)
        w4 = q1(w4)

        w1 = pad_number(w1, 8)
        w2 = pad_number(w2, 8)
        w3 = pad_number(w3, 8)
        w4 = pad_number(w4, 8)

        W = w1 + w2 + w3 + w4

        W = int(W, 2) ^ int(L[2], 2)

        W = pad_number(W, 32)

    # Harus ada setidaknya 2 elemen di L karena panjang kunci minimum adalah 128 bit. Putaran 3

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    W = w1 + w2 + w3 + w4

    W = int(W, 2) ^ int(L[1], 2)

    W = pad_number(W, 32)
    # putaran terakhir dengan langkah XOR. XOR dengan L0

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    W = w1 + w2 + w3 + w4

    W = int(W, 2) ^ int(L[0], 2)

    W = pad_number(W, 32)
    # putaran akhir q-box sebelum perkalian matriks

    w1 = int(W[0:8], 2)
    w2 = int(W[8:16], 2)
    w3 = int(W[16:24], 2)
    w4 = int(W[24:32], 2)

    w1 = q1(w1)
    w2 = q0(w2)
    w3 = q1(w3)
    w4 = q0(w4)

    w1 = pad_number(w1, 8)
    w2 = pad_number(w2, 8)
    w3 = pad_number(w3, 8)
    w4 = pad_number(w4, 8)

    # mengalikannya dengan matriks MDS sehingga kita mengubahnya ke vektor menggunakan notasi yang telah kita buat
    Word_vector = [[int(w1, 2)], [int(w2, 2)], [int(w3, 2)], [int(w4, 2)]]
    
    C = GF256matrixmultiply(MDS, Word_vector)
    Z = ''

    for i, c in enumerate(C):
        Z = Z + pad_number(c[0], 8)

    return Z

# S-box function
def q0(number):

    t = [[8, 1, 7, 13, 6, 15, 3, 2, 0, 11, 5, 9, 14, 12, 10, 4],
         [14, 12, 11, 8, 1, 2, 3, 5, 15, 4, 10, 6, 7, 0, 9, 13],
         [11, 10, 5, 14, 6, 13, 9, 0, 12, 8, 15, 3, 2, 4, 7, 1],
         [13, 7, 15, 4, 1, 2, 6, 14, 9, 11, 3, 0, 8, 5, 12, 10]]

    X = number

    a0 = int(X / 16)
    b0 = int(X % 16)

    # XOR nibble a0 dan nibble b0 untuk mendapatkan a1

    a1 = a0 ^ b0
    b1 = ((a0 ^ ROR(b0, 1, 4)) ^ (8 * a0)) % 16

    # pindahkan a1 dan b1 melalui kotak substitusi
    [a2, b2] = [t[0][a1], t[1][b1]]

    # XOR nibble a2 and nibble b2 to get a3
    a3 = a2 ^ b2
    b3 = ((a2 ^ ROR(b2, 1, 4)) ^ (8 * a2)) % 16

    # pindahkan a3 dan b3 melalui kotak substitusi
    [a4, b4] = [t[2][a1], t[3][b1]]

    # menggabungkan kembali nibble menjadi byte
    y = (16 * b4) + a4

    return y

def q1(number):

    t = [[2, 8, 11, 13, 15, 7, 6, 14, 3, 1, 9, 4, 0, 10, 12, 5],
         [1, 14, 2, 11, 4, 12, 3, 7, 6, 13, 10, 5, 15, 9, 0, 8],
         [4, 12, 7, 5, 1, 6, 9, 10, 0, 14, 13, 8, 2, 11, 3, 15],
         [11, 9, 5, 1, 12, 3, 13, 14, 6, 4, 7, 15, 2, 0, 8, 10]]

    X = number

    a0 = int(X / 16)
    b0 = int(X % 16)

    a1 = a0 ^ b0
    b1 = ((a0 ^ ROR(b0, 1, 4)) ^ (8 * a0)) % 16

    [a2, b2] = [t[0][a1], t[1][b1]]

    a3 = a2 ^ b2
    b3 = ((a2 ^ ROR(b2, 1, 4)) ^ (8 * a2)) % 16

    [a4, b4] = [t[2][a1], t[3][b1]]

    y = (16 * b4) + a4

    return y

# Key Generation
def find_M_vectors(Key):
    bin_key = bin(Key)
    bin_key = bin_key[2:]
    
    if len(bin_key) <= 128:
        N = 128
    elif len(bin_key) > 128 or len(Key) <= 192:
        N = 192
    elif len(bin_key) <= 256:
        N = 256

    Key = pad_number(Key, N)

    N = len(Key)
    k = N / 64

    mk = []
    mij = ''
    for i, digit in enumerate(Key):

        mij = mij + digit

        if len(mij) == 8:
            mk.append(mij)
            mij = ''

    Mi = []
    mi = ''
    
    for i, word in enumerate(mk):

        mi = mi + word
        if len(mi) == 32:
            Mi.append(mi)
            mi = ''

    Mo = []
    Me = []
    for i, m in enumerate(Mi):

        if (1 + i) % 2 == 1:
            Me.append(m)
        else:
            Mo.append(m)

    return [mk, Mo, Me, Mi]

def generate_K(Me, Mo, rounds=16):
    # Matriks MDS
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    rho = pow(2, 24) + pow(2, 16) + pow(2, 8) + pow(2, 0) 

    A = []
    B = []
    K = []
    for i in range(rounds + 8):
        a = pad_number((2 * i * rho), 32)
        A = int(H_function(a, Me, MDS), 2)
        b = pad_number(((2 * i) + 2) * rho, 32)
        B = ROL(int(H_function(b, Mo, MDS), 2), 8, 32)
        K.append((A + B) % pow(2, 32))
        K.append(ROL(((A + (2 * B)) % pow(2, 32)), 9, 32))

    return K

def find_S_vector(mk):
    # Matriks RS
    RS = [[1, 164, 85, 135, 90, 88, 219, 158],
          [164, 86, 130, 243, 30, 198, 104, 229],
          [2, 161, 252, 193, 71, 174, 61, 25],
          [164, 85, 135, 90, 88, 219, 158, 3]]

    T = transpose_vector(mk)

    S_vector = [[], [], [], []]
    k = len(mk) / 8

    for i in range(int(len(mk) / 8)):

        V = T[(8 * i): (8 * i) + 8]

        si = GF256matrixmultiply(RS, V)

        for l, s in enumerate(si):
            S_vector[l].append(s)

    S = []
    for i in range(len(S_vector[0])):

        Si = ''
        for l in range(len(S_vector)):
            Si = Si + pad_number(S_vector[l][i][0], 8)

        S.append(Si)

    return S

def gen_keys(key, N=128, rounds=16):
    key_lengths = [128, 192, 256]

    m = pwdtokey(key)

    if len(bin(m)[2:]) > N:
        m = int(bin(m)[2:N + 2], 2)

    [mk, Mo, Me, Mi] = find_M_vectors(m)

    bin_key = bin(m)
    bin_key = bin_key[2:]
    paded_key = pad_number(m, 128)

    S = find_S_vector(mk)

    K = generate_K(Me, Mo, rounds)

    return [K, S]


#############################################
## Fungsi yang melakukan enkripsi dekripsi ##
#############################################


def encrypt_word(message, S, K, rounds=16):
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    m = message

    E = []
    for i in range(4):
        E.append(m[(i * 32):((i * 32) + 32)])

    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i], 32)

    e = []
    for i, ee in enumerate(E):
        e.append(int(E[i], 2))

    for r in range(rounds):
        e = [[], [], [], []]
        e[0] = H_function(E[0], S, MDS)

        e[1] = ROL(int(E[1], 2), 8, 32)
        e[1] = pad_number(e[1], 32)
        e[1] = H_function(e[1], S, MDS)

        [e[0], e[1]] = PHT(e[0], e[1])

        e[0] = (e[0] + K[(2 * r) + 8]) % pow(2, 32)
        e[1] = (e[1] + K[(2 * r) + 9]) % pow(2, 32)

        e[2] = e[0] ^ int(E[2], 2)
        e[2] = ROR(e[2], 1, 32)

        e[3] = ROL(int(E[3], 2), 1, 32)
        e[3] = e[3] ^ e[1]

        E = [pad_number(e[2], 32), pad_number(e[3], 32), E[0], E[1]]

    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i + 4], 32)

    C = E[0] + E[1] + E[2] + E[3]

    return C


def decrypt_word(Cyphertext, S, K, rounds=16):
    MDS = [[1, 239, 91, 91],
           [91, 239, 239, 1],
           [239, 91, 1, 239],
           [239, 1, 239, 91]]

    C = Cyphertext

    E = []
    for i in range(4):
        E.append(C[(i * 32):((i * 32) + 32)])

    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i + 4], 32)

    for R in range(rounds):
        r = rounds - 1 - R

        E = [E[2], E[3], E[0], E[1]]
        e = [[], [], [], []]

        e[0] = H_function(E[0], S, MDS)

        e[1] = ROL(int(E[1], 2), 8, 32)
        e[1] = pad_number(e[1], 32)
        e[1] = H_function(e[1], S, MDS)

        [e[0], e[1]] = PHT(e[0], e[1])

        e[0] = (e[0] + K[(2 * r) + 8]) % pow(2, 32)
        e[1] = (e[1] + K[(2 * r) + 9]) % pow(2, 32)


        e[2] = ROL(int(E[2], 2), 1, 32)
        e[2] = e[0] ^ e[2]

        e[3] = int(E[3], 2) ^ e[1]
        e[3] = ROR(e[3], 1, 32)

        for i, ee in enumerate(e):
            e[i] = pad_number(ee, 32)

        E = [E[0], E[1], e[2], e[3]]

    for i, e in enumerate(E):
        E[i] = pad_number(int(e, 2) ^ K[i], 32)

    p = E[0] + E[1] + E[2] + E[3]

    return p

def encrypt_message(message, S, K, rounds=16):
    message_num = text2num(message)
    to_encrypt = pad_number(message_num, 128)

    if not isinstance(to_encrypt, list):
        to_encrypt = [to_encrypt]

    cypher_text = ''
    for i, word in enumerate(to_encrypt):
        cypher_word = encrypt_word(word, S, K, rounds)

        cypher_text = cypher_text + cypher_word

    C = int(cypher_text, 2)

    number_C = C

    C = num2text(C)

    return [number_C, C]

def decrypt_message(message, S, K, rounds=16):
    to_encrypt = pad_number(message, 128)

    if not isinstance(to_encrypt, list):
        to_encrypt = [to_encrypt]

    cypher_text = ''
    for i, word in enumerate(to_encrypt):
        cypher_word = decrypt_word(word, S, K, rounds)

        cypher_text = cypher_text + cypher_word

    C = int(cypher_text, 2)

    C = num2text(C)

    return C

######################
## Akhir dari fungsi #
######################

# atur kuncinya
key = 'VkYp3s6v9y$B&E(H+MbQeThWmZq4t7w!'
N = 128
rounds = 16

def start():
    global K, S
    [K, S] = gen_keys(key, N, rounds)

test = 'Lol)'

def encrypt():
    global Cypher_text, num_C
    [num_C, Cypher_text] = encrypt_message(test, S, K)

def decrypt():
    global plain_text
    message_num = text2num(test)
    plain_text = decrypt_message(message_num, S, K, rounds=16)
