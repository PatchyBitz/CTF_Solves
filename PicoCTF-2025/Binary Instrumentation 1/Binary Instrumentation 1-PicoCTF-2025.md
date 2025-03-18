
#### Hints given
1. Frida is an easy-to-install, lightweight binary instrumentation toolkit
2. Try using the CLI tools like frida-trace to auto-generate handlers

	Author: Venax
	Description:
	
	I have been learning to use the Windows API to do cool stuff! Can you wake up my program to get the flag? Download the exe [here](https://challenge-files.picoctf.net/c_verbal_sleep/c71239e2890bd0008ff9c1da986438d276e7a96ba123cb3bc7b04d5a3de27fe7/bininst1.zip). Unzip the archive with the password `picoctf`
---
>This challenge was my first interaction with Frida and binary instrumentation, so I apologize for any mistakes on that front.
>This was done in VirtualBox running Windows 10. The file kept tripping windows defender so I thought it'd be better to be safe than sorry.

The description of this challenge points in the direction of Win32 API. After installing Frida, we can use the following command to try to discover what functions are being used (In the same directory as bininst1.exe)
```
frida-trace -f bininst1.exe -I KERNEL32.DLL
```
This is a very brute force method to discover the the function being used as it tells frida-trace to generate a handler/interceptor for every single Win32 API call by the program. This will include a lot of red herrings that are just part of an exe's standard execution. A more effective one would be to look up the sleep functions in Microsoft's documentation. I found the following to be the most effective:
```
frida-trace -f bininst1.exe -i Sleep -i SleepEx
```

After frida-trace generates the handlers, going to the UI at the provided link will present:

![[Step1.png]]


A handy function of frida-trace is that each handler can easily be set to return the arguments that the function was called with. Navigating to the [SleepEx Function Documentation](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-sleepex) we can see that SleepEx has the following arguments:

	DWORD SleepEx(
	  [in] DWORD dwMilliseconds,
	  [in] BOOL  bAlertable
	);

So we can change the onEnter in KERNEL32.DLL\/SleepEx to the following.
```
defineHandler({
  onEnter(log, args, state) {
    log('SleepEx()');
    log('Time:',args[0].toUInt32());
    log('Alertable:',args[1]);

  },

  onLeave(log, retval, state) {
  }
});
```

After that we hit deploy on the top left and respawn on the bottom left.
> This might take a moment, that or my poor abused VM was struggling

After a while we should see the following: 
![[Step2.png]]

We can see that the time on this sleep is set to about ~1200 hours.
> This may not be accurate due to how we read the output.

Frida can also be used to rewrite the arguments of the function call as they're being called. We can do that with the following code:
```
defineHandler({
  onEnter(log, args, state) {
    log('SleepEx()');
    log('Time:',args[0].toUInt32());
    log('Alertable:',args[1]);
    log("Rewriting Time....");
    args[0] = ptr(1);
  },

  onLeave(log, retval, state) {
  }
});
```

After hitting deploy and respawn, we can go back to our cmd line window (where we ran the frida-trace command) and see something like this:
![[Step3.png]]
Scrolling down a bit:
![[Step4.png]]
We get a prompt:
```
Ok, I'm Up! The flag is: cGljb0NURnt3NGtlX20zX3VwX3cxdGhfZnIxZGFfZjI3YWNjMzh9
```
This looks like base64 but that should be easy enough for anyone reading to translate.


