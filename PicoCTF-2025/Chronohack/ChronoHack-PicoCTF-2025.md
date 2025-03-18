
#### Hints given
1. https://www.epochconverter.com/
2. https://learn.snyk.io/lesson/insecure-randomness/
3. Time tokens generation
4. Generate tokens for a range of seed values very close to the target time

	Author: Theoneste Byagutangaza
	#### Description
	
	Can you guess the exact token and unlock the hidden flag? Our school relies on tokens to authenticate students. Unfortunately, someone leaked an important [file for token generation](https://challenge-files.picoctf.net/c_verbal_sleep/a9a0d914f80a4b798146047d893257cbd875fa51ffeb4f2da69ae1e07e54577b/token_generator.py). Guess the token to get the flag.
	
	Additional details will be available after launching your challenge instance.
---

This challenge was relatively simple, but required the use of automation to solve effectively.

When opening a connection to the target server we are presented with:
```
Can you guess the token?

Enter your guess for the token (or exit):

```
Notably, the limit on the number of guesses is 50 per connection. We can see this in the provided file here:
```
            if n == 50:
                print("\nYou exhausted your attempts, Bye!")
```
After 50 attempts, a new token is generated with the following:
```
def get_random(length):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(int(time.time() * 1000))  # seeding with current time 
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s
```

After examining the code the program does the following:
1. Welcomes the user
2. Generates a random token
3. Takes user's input/guess
4. Exits after 50 incorrect attempts

Another piece to note in the token generator function is the random seed that is used. Because a computer can't truly be random, the seed is the deterministic start for the entire string of numbers that the function may output. As such if we can guess the right seed, which in this case is just a timestamp that we can copy, we should be able to generate the exact same token and get the flag. 

### Solution:
To go about solving this I used PWNTools, a Python library that had been introduced in one of the earlier challenges. 
>I tried going back to find this but I wasn't able to find which exact challenge introduced it as a hint, it may have been one of the challenges that were removed early on in the challenge`

The solver script does the following:
1. Connects to the target server using PWNTools Socket
2. Gets the current time at start connection as "anchor"
3. Subtracts current time from a custom "attempted" offset
4. Runs the token generator function with the modified time
5. Connects and attempts to use token
6. If failed messages are returned, iterates and loops steps 3 - 6 again for defined block size of 50 (The amount of allowed attempts)
7. Closes connection after 50 and tries till "maxoffset" is reached.

I tried this for a while with attempted set to positive numbers and iterating by 1 second each loop. I thought that I would be trying to go backwards and reach the time the target had generated the token as the token should have been generated before my script initiated. After trying various offsets up to 100 seconds, I figured that there wasn't any way that the clock could have initiated that much faster than my program. So I figured I may as well have tried the other direction. What I settled on was +90 manual offset and after going through the first loop, after ~6 attempts by my script I was able to get the flag. 

It turns out that the target server had their time slightly ahead of mine which had caused some issues with determining the right time token. I'm guessing that depending on where the competitors were during this competition, their system settings and NTP Servers, they may have had a varied experience on how easy/difficult it was to match seeds with the insecure token token generator.




