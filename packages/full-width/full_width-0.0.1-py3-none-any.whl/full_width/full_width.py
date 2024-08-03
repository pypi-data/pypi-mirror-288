import sys

def full_width():
    for c in sys.stdin.read():
        if ord(c) >= ord("A") and ord(c) <= ord("Z"):
            sys.stdout.write(chr(ord(c)-ord("A")+65313))
        elif ord(c) >= ord("a") and ord(c) <= ord("z"):
            sys.stdout.write(chr(ord(c)-ord("a")+65345))
        else:
            sys.stdout.write(c)
    sys.stdout.flush()
    return 0
