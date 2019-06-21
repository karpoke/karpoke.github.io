Title: Comprobar la firma de Xposed
Date: 2016-11-25 22:26
Author: Ignacio Cano
Tags: xposed, gpg, comprobación de firma, cyanogenmod
Slug: comprobar-la-firma-de-xposed

Ayer mismo, se subió una [nueva versión][] del _framework_ [Xposed][], el
cual tengo instalado en un Samsung S4.

Si queremos descargarla y comprobar mediante la firma que lo que nos hemos
bajado no ha sido alterado, no tenemos más que hacer uso de `gpg`.

Descargamos los archivos:

```bash
$ wget http://dl-xda.xposed.info/framework/sdk23/arm/xposed-v87-sdk23-arm.zip
$ wget http://dl-xda.xposed.info/framework/sdk23/arm/xposed-v87-sdk23-arm.zip.asc
```

Y comprobamos la firma:
```bash
$ gpg --verify xposed-v87-sdk23-arm.zip.asc
gpg: Signature made jue 24 nov 2016 22:26:15 CET using RSA key ID 852109AA
gpg: Can’t check signature: public key not found
```

En este caso, la firma no está certificada por una autoridad de confianza, y
tampoco la tenemos importada en nuestro sistema. Vamos a buscarla y, si nos
fiamos de esa cuenta de correo, tenemos la opción de importarla:

```bash
$ gpg --search-keys 852109AA
gpg: searching for "852109AA" from hkp server keys.gnupg.net
(1)     rovo89 <android@robv.de>
        rovo89 <rovo89@xposed.info>
          4096 bit RSA key 7235F333, created: 2016-03-12
Keys 1-1 of 1 for "852109AA".  Enter number(s), N)ext, or Q)uit > 1
gpg: requesting key 7235F333 from hkp server keys.gnupg.net
gpg: key 7235F333: public key "rovo89 <android@robv.de>" imported
gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
```

Ahora ya podemos verificar el fichero descargado:

```bash
$ gpg --verify xposed-v87-sdk23-arm.zip.asc
gpg: Signature made jue 24 nov 2016 22:26:15 CET using RSA key ID 852109AA
gpg: Good signature from "rovo89 <android@robv.de>"
gpg:                 aka "rovo89 <rovo89@xposed.info>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 0DC8 2B3E B1C4 6D48 33B4  C434 E82F 0871 7235 F333
     Subkey fingerprint: EA94 3952 EB4E 66EB 8115  1B3E 865B 714E 8521 09AA
```

  [nueva versión]: http://dl-xda.xposed.info/framework/sdk23/arm/
    "Xposed v87 SDK23 ARM"
  [Xposed]: http://repo.xposed.info/
    "Xposed framework"
