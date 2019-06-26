Title: Instalación automática de las fuentes para web de Google
Date: 2011-08-07 00:21
Author: Nacho Cano
Tags: fc-cache, fontconfig, fuentes, google web fonts, hg, mercurial, script, software libre
Slug: instalacion-automatica-de-las-fuentes-para-web-de-google

En [webupd8.org][] han publicado un _script_ que permite [descargar las
fuentes para web de Google][], o actualizarlas si ya las habíamos
descargado.

[Google Web Fonts][] es un proyecto que consiste en crear un repositorio
de fuentes tipográficas de calidad, libres y gratuitas, para que
cualquiera pueda utilizarlas en sus proyectos web, sin ningún tipo de
barrera, mucho menos económica.

![Google Web Fonts]({static}/images/google-web-fonts-300x199.png)

<small>_Fuente: [googlewebfonts.blogspot.com][]_</small>

El _[script][]_ instala las fuentes en el directorio
`/usr/share/fonts/truetype/google-fonts/`, por lo que basta eliminar
este directorio para borrarlas.

Para descargar el _script_ e instalar las fuentes, ejecutamos:

```bash
$ wget http://webupd8.googlecode.com/files/install-google-fonts
$ chmod +x install-google-fonts
$ ./install-google-fonts
```

Éste es el contenido del _script_:

```bash
# Original author: Michalis Georgiou
# Modified by Andrew http://www.webupd8.org

sudo apt-get install mercurial

_hgroot="https://googlefontdirectory.googlecode.com/hg/"
_hgrepo="googlefontdirectory"

echo "Connecting to Mercurial server...."
if [ -d $_hgrepo ] ; then
    cd $_hgrepo
    hg pull -u || return 1
    echo "The local files have been updated."
    cd ..
else
    hg clone $_hgroot $_hgrepo || return 1
fi
echo "Mercurial checkout done or server timeout"
sudo mkdir -p /usr/share/fonts/truetype/google-fonts/
find $PWD/$_hgrepo/ -name "*.ttf" -exec sudo install -m644 {} /usr/share/fonts/truetype/google-fonts/ \; || return 1
fc-cache -f > /dev/null
echo "done."
```

El _script_ también crea el directorio `googlefontdirectory` en el
directorio desde el cual lo hayamos lanzado. Ahí se encuentra el
[respositorio de las fuentes][], así la próxima vez que lo ejecutemos se
realizará una actualización, en lugar de una descarga completa.

Una cosa que hace el _script_ y que no he visto comentada en la página
del repositorio, es ejecutar el comando `fc-cache` después de realizar
la instalación o actualización de las fuentes.

`fc-cache` busca en el directorio de fuentes del sistema,
`/usr/share/fonts/`, y crea diversos archivos caché con información de
las fuentes para las aplicaciones que usan `fontconfig` para el
tratamiento de las fuentes. Estos archivos caché se utilizan para
acelerar el inicio de la aplicación cuando utilizan la librería
`fontconfig`. `fontconfig` es una biblioteca de configuración y
personalización de tipografías, que no depende del sistema de ventanas
X. Está diseñada para localizar tipografías en el sistema y
seleccionarlas según los requerimientos especificados por las
aplicaciones.

Para utilizar las fuentes, vamos al menú
`Sistema > Preferencias > Apariencia > Tipografías`.

  [webupd8.org]: http://www.webupd8.org
    "webupd8.org"
  [descargar las fuentes para web de Google]: http://www.webupd8.org/2011/01/automatically-install-all-google-web.html
    "descargar las fuentes para web de Google"
  [Google Web Fonts]: http://www.google.com/webfonts#AboutPlace:about
    "Google Web Fonts"
  [googlewebfonts.blogspot.com]: http://googlewebfonts.blogspot.com/
    "googlewebfonts.blogspot.com"
  [script]: http://webupd8.googlecode.com/files/install-google-fonts
    "script"
  [respositorio de las fuentes]: http://code.google.com/p/googlefontdirectory/
    "respositorio de las fuentes"
