Title: Copiar un directorio excluyendo los archivos de una clase
Date: 2011-05-11 21:09
Author: Nacho Cano
Tags: dropbox, rsync, svn
Slug: copiar-un-directorio-excluyendo-los-archivos-de-una-clase

Si queremos copiar un directorio pero no queremos que se copien los
archivos `.svn`, o `.dropbox`, podemos ejecutar:

    $ rsync -r --exclude=.dropbox /path/source/dir /path/destination
