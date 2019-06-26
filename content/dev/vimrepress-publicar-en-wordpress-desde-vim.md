Title: vimrepress, publicar en WordPress desde vim
Date: 2012-05-20 13:54
Author: Nacho Cano
Tags: markdown, python, vim, wordpress
Slug: vimrepress-publicar-en-wordpress-desde-vim

[vimrepress][] es un complemento para trabajar con WordPress. Esta mañana
he leído sobre él en el blog de CyberHades y me han entrado ganas de
probarlo.

Instalación
-----------

Para que funcione, además de instalar el complemento deberemos activar el
servicio XML-RPC en WordPress para publicar de forma remota. Para
activarlo vamos a Ajustes > Escritura y marcamos la casilla XML-RCP.

Ahora vamos a instalar el complemento. Descargamos la última versión
estable, en estos momentos la 2.1.5, y la descomprimimos en el
directorio `~/.vim`:

```bash
$ wget "www.vim.org/scripts/download_script.php?src_id=16490" -O vimpress-stable_2.1.5.zip
$ unzip vimpress-stable_2.1.5.zip -d ~/.vim
```

Añadimos al fichero de configuración de `vim`, `~/.vimrc`:

```bash
let VIMPRESS = [{'username': 'user',
                 'password': 'pass',
                 'blog_url': 'http://your-first-blog.com/'
                },
                {'username': 'user',
                 'blog_url': 'http://your-second-blog.com/'
                }]
```

Uso
---

Algunos comandos que muestran cómo utilizar el complemento:

```bash
    :BlogList             -  Los 30 últimos artículos.
    :BlogList post 100    -  100 últimos artículos.
    :BlogList page        -  Las 30 últimas páginas.

    :BlogNew post         -  Añadir un artículo.
    :BlogNew page         -  Añadir una página.

    :BlogSave             -  Guardar (por defecto, como publicado).
    :BlogSave draft       -  Guardar como borrador.

    :BlogPreview local    -  Vista previa en local.
    :BlogPreview publish  -  Publicar y vista previa.

    :BlogOpen 679
    :BlogOpen http://your-first-blog.com/archives/679
    :BlogOpen http://your-second-blog.com/?p=679
    :BlogOpen http://your-third-blog.com/with-your-custom-permalink
```

Para que funcione, además de instalar el complemento deberemos activar el
servicio XML-RPC para publicar de forma remota. Para activarlo vamos a
Ajustes > Escritura y

Markdown
--------

Con vimpress podemos utilizar [Markdown][] para escribir los artículos
en lugar de hacerlo en HTML. Tendremos que tener instalado el paquete
`python-markdown`.

Un pequeño ejemplo de su sintaxis:

`# Título H1`
=============

`## Título H2`
--------------

### `### Título H3`

_`_cursiva_`_

__`**negrita**`__

__*`***negrita y cursiva***`*__

[texto del enlace][] = `[texto del enlace](http://www.example.com)`

![texto alternativo de la imagen][] =
`![texto alternativo de la imagen](http://www.example.com/image.png "Título de la imagen")`

[enlace referenciado][] = `[enlace referenciado][id]` y en otra parte
añadimos `[id]: http://example.com/  "Title"`

Listado sin orden:

-   `"- foo"`
-   `"- bar"`

Listado ordenado:

1.  `"1. primero"`
2.  `"2. segundo"`

> `> cita`

> > `> > cita anidada`

``` ``code`` ```

Referencias
-----------

- [Vim, Markdown y WordPress][]
- [vimrepress][1]
- [Markdown syntax][Markdown]
- [Markdown web dingus][]

  [vimrepress]: http://www.vim.org/scripts/download_script.php?src_id=16490
    "vimrepress"
  [Markdown]: http://daringfireball.net/projects/markdown/syntax
    "Markdown"
  [texto del enlace]: http://example.com
    "texto del enlace"
  [texto alternativo de la imagen]: http://example.com/image.png
    "texto alternativo de la imagen"
  [enlace referenciado]: http://www.example.com
    "enlace referenciado"
  [Vim, Markdown y WordPress]: http://www.cyberhades.com/2012/05/11/vim-markdown-y-wordpress/
    "Vim, Markdown y WordPress"
  [1]: http://www.vim.org/scripts/script.php?script_id=3510
    "1"
  [Markdown web dingus]: http://daringfireball.net/projects/markdown/dingus
    "Markdown web dingus"
