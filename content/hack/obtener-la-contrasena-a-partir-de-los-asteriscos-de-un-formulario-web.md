Title: Obtener la contraseña a partir de los asteriscos de un formulario web
Date: 2011-09-11 17:48
Author: Nacho Cano
Tags: chromium, contraseña, firebug, firefox, javascript, noscript
Slug: obtener-la-contrasena-a-partir-de-los-asteriscos-de-un-formulario-web

Si nos encontramos un formulario web lleno de asteriscos, podemos
obtener lo que hay realmente escrito pegando lo siguiente en la barra de
direcciones:

    javascript:(function(){var s,F,j,f,i; s = ""; F = document.forms; for(j=0; j < f.length; ++j) { f = F[j]; for (i=0; i < f.length; ++i) { if (f[i].type.toLowerCase() == "password") s += f[i].value + " "; } } if (s) alert("Passwords in forms on this page: " + s); else alert("There are no passwords in forms on this page.");})();
