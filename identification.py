# Important vars
CHARS = "A1234567890BCDEFGHIJKLMNOPQRSTUVWXYZ"  #All digits + all uppercase characters. A is the first character to avoid having trailing 0s (CUSIP, SEDOL, and ISIN codes all end in check digits)
CHARS2 = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# utility functions
def str2int(s, chars):
    i = 0
    for c in reversed(s):
        i *= len(chars)
        i += chars.index(c)
    return i

def int2str(i, chars):
    s = ""
    while i:
        s += chars[i % len(chars)]
        i //= len(chars)
    return s

def encode(id):
    encoded = int2str(str2int(id, CHARS), CHARS2)
    padded = encoded.ljust(11, "0")
    if len(padded) != 11:
        raise Exception("compression algorithm has failed")
    return padded

def decode(id):
    depadded = id.strip("0")
    decoded = int2str(str2int(depadded, CHARS2), CHARS)
    return decoded


# Sqid Item class
class ID:
    def __init__ (
            self,
            id = None,
            cusip = None,
            sedol = None,
            isin = None,
            other=None,
    ):
        '''
        Create object by initiating with a CUSIP, SEDOL, ISIN, or ID
        If initiated with a CUSIP, SEDOL, or ISIN: 
            - Object will generate the corresponding ID under the "ID" variable
        If iniated with an ID:
            - Object will generate the correspondins CUSIP, SEDOL, or ISIN under the designated variable, determined by decoded length
        - IDs are generated by:
            1. Converting the CUSIP, SEDOL, or ISIN into the decimal value of its base 36 (alphabet upper + decimals) representation
                - The encoding process flips each tag (which must end in a check digit int) and then starts its alphabet with an A to avoid having trailing 0s which will cause the math to break down
            2. Compressing the decimal representation into a base 61 representation (alphabet lower + alphabet upper + decimals excluding 0)
            3. Padding the output value with 0s until the length of 11 is reached. The number 11 is the greatest possible length that the output could be. 
            - In doing so, we create IDs that are not only shorter than ISINs, but can also be decoded into their original representation in case of emergency
        '''

        # Sets sqid identifiers
        self.cusip = cusip
        self.sedol = sedol
        self.isin = isin
        # 
        self.other = other
        
        # If the input is in the form of a sqid id, decodes the sqid id to get identifiers
        if id:
            # Sets sqids self var
            self.id = id

            # Decodes sqid
            decoded = decode(id)

            # Determines identifier type based on length of decoded output
            if len(decoded) == 7:
                self.sedol = decoded
            elif len(decoded) == 9:
                self.cusip = decoded
            elif len(decoded) == 12:
                self.isin = decoded
            elif len(decoded) == 11:
                self.other = decoded
            else:
                raise Exception("Unable to decode")

        # If the input is in the form of cusip, sedol, isin, encodes the identifiers to get sqid
        elif cusip or isin or sedol:
            # Encodes identifiers
            # If multiple identifiers inputted, the first one that exists in the order you see is used to generate the ID. 
            # Cusip, Isin, Sedol (AKA alphabetical order)
            self.id = encode(cusip or isin or sedol)


        elif other:
            pass


        # Raises error if nothing is inputted
        else:
            raise Exception("At least one parameter must exist to create ID")


def inquire():
    input_string = input("Please input ID (11 chars), CUSIP (9 chars), ISIN (12 chars) or SEDOL (7 chars): ")
    if len(input_string) == 11:
        identifier = ID(id=input_string)
    else:
        identifier = ID(cusip=input_string) # doesnt matter whether you set it to cusip, sedol, or isin
    for key, value in vars(identifier).items():
        print(f"{key}: {value}")

#inquire()

###############################################################
if __name__ == "__main__":
    inquire()
