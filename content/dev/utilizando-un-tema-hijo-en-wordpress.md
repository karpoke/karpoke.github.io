Title: Utilizando un tema hijo en WordPress
Date: 2013-07-13 19:04
Author: Nacho Cano
Tags: php, tema hijo, tema nieto, wordpress
Slug: utilizando-un-tema-hijo-en-wordpress

Un [tema hijo en WordPress][] es un tema que hereda la funcionalidad de
otro, el tema padre, permitiendo modificar el estilo o añadir
funcionalidades a éste. Es la forma más sencilla y segura de modificar
un tema existente, ya sean cambios grandes o pequeños. Si utilizamos un
tema de otros, ya sea gratuito o de pago, crear un tema hijo es una
buena idea.


¿Por qué crear un tema hijo?
----------------------------

Porqué en algún momento cambiaremos algo del tema que estamos usando, y
en algún momento posterior es posible que haya una actualización de
dicho tema. En el mejor de los casos, nos deberemos preocupar de guardar
los cambios que hemos hecho en el tema y aplicarlos de nuevo tras la
actualización. En el peor, perderemos los cambios que hemos hecho.

Crear un tema hijo
------------------

Para tener un tema hijo funcionando, lo único que tenemos que hacer es:

1.  Crear un directorio con el mismo nombre, añadiendo el sufijo
    `-child`, en el mismo directorio del tema padre. Ejemplo:
    `twentytwelve-child`
2.  Añadimos el fichero `style.css` en el directorio recién creado:

    ```php
    /*
    Theme Name:     Twenty Twelve Child
    Theme URI:      http://example.com/
    Description:    Child theme for the Twenty Twelve theme
    Author:         Your name here
    Author URI:     http://example.com/about/
    Template:       twentytwelve
    Version:        0.1.0
    */
    ```

    Si sólo queremos hacer pequeñas modificaciones, podemos importar la
    hoja de estilo del tema padre y añadir los cambios a continuación:

    ```php
    @import url("../twentytwelve/style.css");
    ```

3.  Activamos el tema desde el panel de administración

Para sobreescribir un fichero, basta que tenga el mismo nombre que en el
tema padre. De ahí que necesitemos importar el fichero del tema padre si
sólo queremos añadir algunos cambios. Una excepción es el fichero
`functions.php`, el cual se carga antes que el del tema hijo, por lo que
no será necesario copiar este fichero. Para poder sobrecargar una
función del tema padre, éste debe utilizar funciones sobreescribibles,
que comprueban si han sido definidas previamente.

A partir de ahora, podemos llenar el fichero `functions.php` de nuestro
tema hijo con todas esas funciones imprescindibles de sitios como:

-   [WordPress Stack Exchange][]
-   [Cats who code][]
-   [Smashing Magazine][]
-   [WordPress Recipes][]
-   [WordPress Mix][]
-   [Dig WordPress][]
-   [WordPress Tutplus][]
-   [WordPress Code Snippets][]

¿Y si ya estoy utilizando un tema hijo?
---------------------------------------

Es posible que ya estemos utilizando un tema hijo. En este caso, podemos
crear un tema nieto, sólo que no se hace como hemos hecho para el tema
hijo, sino que debe hacerse como si fuese un complemento. Más información
en este artículo en [wp-code.com][].

Referencias
-----------

» [How to Customize Your WordPress Theme With a Child Theme][]
» [Don't edit child themes – use grandchild themes!][wp-code.com]
» [WordPress Child Themes][tema hijo en WordPress]
» [WordPress Pluggable Functions][]

  [tema hijo en WordPress]: http://codex.wordpress.org/Child_Themes
    "tema hijo en WordPress"
  [WordPress Stack Exchange]: http://wordpress.stackexchange.com
    "WordPress Stack Exchange"
  [Cats who code]: http://www.catswhocode.com
    "Cats who code"
  [Smashing Magazine]: http://wp.smashingmagazine.com
    "Smashing Magazine"
  [WordPress Recipes]: http://www.wprecipes.com
    "WordPress Recipes"
  [WordPress Mix]: http://wp-mix.com
    "WordPress Mix"
  [Dig WordPress]: http://digwp.com
    "Dig WordPress"
  [WordPress Tutplus]: http://wp.tutsplus.com/
    "WordPress Tutplus"
  [WordPress Code Snippets]: http://www.wp-code.com/
    "WordPress Code Snippets"
  [wp-code.com]: http://www.wp-code.com/wordpress-snippets/wordpress-grandchildren-themes/
    "wp-code.com"
  [How to Customize Your WordPress Theme With a Child Theme]: http://wp.tutsplus.com/wordpress-2/how-to-customize-your-wordpress-theme-with-a-child-theme/
    "How to Customize Your WordPress Theme With a Child Theme"
  [WordPress Pluggable Functions]: http://codex.wordpress.org/Pluggable_Functions
    "WordPress Pluggable Functions"
