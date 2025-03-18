from pwn import *
import random
import time
target= "verbal-sleep.picoctf.net"
targetport = 53554
# target = "localhost"
# targetport = 5555


def get_randomtimeanc(length,offset,time):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(time-offset)  # seeding with current time  old funct: int(time.time() * 1000)
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s

token_length = 20  # the token length
blocks = 50
maxattempts = 100
attempted = -90


for x in range(maxattempts):

    con = remote(target,targetport)    
    anchor = int((time.time() * 1000))
    print("New Offset:", attempted)
    print(anchor)
    if con.connected():
        for i in range(blocks):
            token = get_randomtimeanc(token_length,i,anchor-attempted)
            x = con.recvuntil(b'):')
            con.sendline(token)
            print(token)

            
            returnline = con.recvline()
            if returnline != b'Sorry, your token does not match. Try again!\n' or returnline == b"You exhausted your attempts, Bye!\n":
                print(token)
                print(returnline)
                con.close()
                con.interactive()
                break
            sleep(.01)
        attempted -= 1
    else:
        sleep(1)
    con.close()


#print(bytes.fromhex(token)) 
#con.sendline(token)
#con.close()
#con.interactive()
