/**********************************
Pourquoi ne pas utiliser l'événement submit pour le savoir ? L'événement submit n'est pas déclenché tant que le navigateur n'a pas déterminé que tous les champs à valider sont corrects. Ainsi, il n'est pas possible de savoir si l'utilisateur a tenté de valider son formulaire, mais que le navigateur l'en a empêché.

Il serait utile de savoir quand l'utilisateur tente de soumettre un formulaire. Vous pourriez vouloir montrer à l'utilisateur une liste de messages d'erreur, changer le focus ou afficher des messages d'aide. Malheureusement, vous aurez besoin de code supplémentaire pour faire cela.

L'une des façons d'y arriver est d'ajouter au formulaire l'attribut novalidate et d'utiliser l'événement submit. Du fait de l'attribut novalidate, la soumission du formulaire ne sera pas empêchée par un champ non validé. Ensuite, ce sera au script de vérifier la validité du formulaire lors de l'événement submit et d'empêcher, si besoin, la soumission.
Voici comment pourrait s'écrire un tel script dans le cas précédent de deux champs password devant être identiques :

 Sélectionnez
******************************************/

<form id="passwordForm" novalidate>
    <fieldset>
        <legend>Changer votre mot de passe</legend>
        <ul>
            <li>
                <label for="password1">Mot de passe :</label>
                <input type="password" required id="password1" />
            </li>
            <li>
                <label for="password2">Confirmez :</label>
                <input type="password" required id="password2" />
            </li>
        </ul>
        <input type="submit" />
    </fieldset>
</form>
<script>
    var password1 = document.getElementById('password1');
    var password2 = document.getElementById('password2');
 
    var checkPasswordValidity = function() {
        if (password1.value != password2.value) {
            password1.setCustomValidity('Les mots de passe doivent être identiques.');
        } else {
            password1.setCustomValidity('');
        }        
    };
 
    password1.addEventListener('change', checkPasswordValidity, false);
    password2.addEventListener('change', checkPasswordValidity, false);
 
    var form = document.getElementById('passwordForm');
    form.addEventListener('submit', function() {
        checkPasswordValidity();
        if (!this.checkValidity()) {
            event.preventDefault();
            // Ajoutez ici la gestion de vos messages d'erreur.
            password1.focus();
        }
    }, false);
</script>


//To stop that Html5 popup/balloon in Web-kit browser use following CSS 

::-webkit-validation-bubble-message { display: none; }

//ou sous balise form ajouter 
novalidate="novalidate"


$("#form").validate({
    onfocusout: false,
    invalidHandler: function(form, validator) {
        var errors = validator.numberOfInvalids();
        if (errors) {                    
            validator.errorList[0].element.focus();
        }
    } 
});