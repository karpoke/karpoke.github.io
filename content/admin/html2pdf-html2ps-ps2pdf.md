Title: html2pdf = html2ps + ps2pdf
Date: 2011-02-28 13:47
Author: Nacho Cano
Tags: alias, html, html2ps, libro, pdf, ps, ps2pdf
Slug: html2pdf-html2ps-ps2pdf

Un buen comando para [convertir una web a PDF][], idóneo para sitios con
documentación pero que ésta sólo está disponible _online_. Por ejemplo:

```bash
$ html2ps -W b http://www.vala-project.org/doc/vala/ | ps2pdf - out.pdf
```

Con la opción `-W b` le decimos a `html2ps` que siga sólo los enlaces
que están en el mismo directorio, o a partir de él,
respecto a la ruta proporcionada.

![Cool HTML Codes]({static}/images/cool-html-codes-300x225.jpg)

<small>_Fuente: [techpin.com][]_</small>

Podemos crear un alias que reciba dos parámetros, la URL y el nombre que
queremos ponerle al PDF:

```bash
$ alias html2pdf='fhtml2pdf() { html2ps -W a "$1" | ps2pdf - "$2"; }; fhtml2pdf'
$ html2pdf http://www.vala-project.org/doc/vala/ vala-doc.pdf
```

  [convertir una web a PDF]: http://www.atareao.es/ubuntu/conociendo-ubuntu/convetir-un-sitio-web-a-pdf-en-ubuntu/
    "convertir una web a PDF"
  [techpin.com]: http://www.techpin.com/
    "www.techpin.com"
