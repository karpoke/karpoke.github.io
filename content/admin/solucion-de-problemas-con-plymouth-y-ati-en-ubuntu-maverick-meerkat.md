Title: Solución de problemas con Plymouth y ATI en Ubuntu Maverick Meerkat
Date: 2011-01-18 06:23
Author: Nacho Cano
Tags: 10.10, arranque gráfico del sistema, ati, hwinfo, lspci, plymouth, tee, ubuntu maverick meerkat, update-grub2, update-initramfs, vga=769 deprecated
Slug: solucion-de-problemas-con-plymouth-y-ati-en-ubuntu-maverick-meerkat

Se conoce que tras [actualizar a Maverick Meerkat][], incluso de Karmic
a Lucid, algo pasaba con Playmouth, de tal manera que utilizaba una
resolución inadecuada.

La solución parece depender en algunos casos de la tarjeta gráfica que
tengamos, así que describiré la que me [funcionó con una ATI Radeon][]:

```bash
$ lspci | grep vga
01:00.0 VGA compatible controller: ATI Technologies Inc M92 [Mobility Radeon HD 4500 Series]
```

Instalamos el paquete `v86d`:

```bash
$ sudo aptitude install v86d
```

Comprobamos las resoluciones que podemos poner:

```bash
$ sudo hwinfo --framebuffer
```

```bash

02: None 00.0: 11001 VESA Framebuffer
  [Created at bios.464]
  Unique ID: rdCR.QOJHFkjgnM2
  Hardware Class: framebuffer
  Model: "(C) 1988-2005, ATI Technologies Inc.  M92"
  Vendor: "(C) 1988-2005, ATI Technologies Inc. "
  Device: "M92"
  SubVendor: "ATI ATOMBIOS"
  SubDevice:
  Revision: "01.00"
  Memory Size: 16 MB
  Memory Range: 0xd0000000-0xd0ffffff (rw)
  Mode 0x0300: 640x400 (+640), 8 bits
  Mode 0x0301: 640x480 (+640), 8 bits
  Mode 0x0303: 800x600 (+832), 8 bits
  Mode 0x0305: 1024x768 (+1024), 8 bits
  Mode 0x0307: 1280x1024 (+1280), 8 bits
  Mode 0x0310: 640x480 (+1280), 15 bits
  Mode 0x0311: 640x480 (+1280), 16 bits
  Mode 0x0313: 800x600 (+1600), 15 bits
  Mode 0x0314: 800x600 (+1600), 16 bits
  Mode 0x0316: 1024x768 (+2048), 15 bits
  Mode 0x0317: 1024x768 (+2048), 16 bits
  Mode 0x0319: 1280x1024 (+2560), 15 bits
  Mode 0x031a: 1280x1024 (+2560), 16 bits
  Mode 0x030d: 320x200 (+640), 15 bits
  Mode 0x030e: 320x200 (+640), 16 bits
  Mode 0x0320: 320x200 (+1280), 24 bits
  Mode 0x0393: 320x240 (+320), 8 bits
  Mode 0x0395: 320x240 (+640), 16 bits
  Mode 0x0396: 320x240 (+1280), 24 bits
  Mode 0x03b3: 512x384 (+512), 8 bits
  Mode 0x03b5: 512x384 (+1024), 16 bits
  Mode 0x03b6: 512x384 (+2048), 24 bits
  Mode 0x03c3: 640x350 (+640), 8 bits
  Mode 0x03c5: 640x350 (+1280), 16 bits
  Mode 0x03c6: 640x350 (+2560), 24 bits
  Mode 0x0333: 720x400 (+768), 8 bits
  Mode 0x0335: 720x400 (+1472), 16 bits
  Mode 0x0336: 720x400 (+2944), 24 bits
  Mode 0x0353: 1152x864 (+1152), 8 bits
  Mode 0x0355: 1152x864 (+2304), 16 bits
  Mode 0x0356: 1152x864 (+4608), 24 bits
  Mode 0x0363: 1280x960 (+1280), 8 bits
  Mode 0x0365: 1280x960 (+2560), 16 bits
  Mode 0x0366: 1280x960 (+5120), 24 bits
  Mode 0x0321: 640x480 (+2560), 24 bits
  Mode 0x0322: 800x600 (+3200), 24 bits
  Mode 0x0323: 1024x768 (+4096), 24 bits
  Mode 0x0324: 1280x1024 (+5120), 24 bits
  Mode 0x0343: 1400x1050 (+1408), 8 bits
  Mode 0x0345: 1400x1050 (+2816), 16 bits
  Mode 0x0346: 1400x1050 (+5632), 24 bits
  Config Status: cfg=new, avail=yes, need=no, active=unknown
```

Escogemos, por ejemplo, 1280x960.

Editamos el fichero `/etc/default/grub` y modificamos la linea:

```bash
GRUB_CMDLINE_LINUX_DEFAULT
```

por

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset video=uvesafb:mode_option=1280x960-24,mtrr=3,scroll=ywrap"
```

Y añadimos, debajo de la línea comentada que comienza por
`GRUB_GFXMODE`:

```bash
GRUB_GFXMODE=1280x960
```

Ahora añadimos al fichero `/etc/initramfs-tools/modules`:

```bash
uvesafb mode_option=1280x960-24 mtrr=3 scroll=ywrap
```

Forzamos a usar el _framebuffer_ en el arranque:

```bash
$ echo FRAMEBUFFER=y | sudo tee /etc/initramfs-tools/conf.d/splash
```

Actualizamos `grub2` y `initramfs`:

```bash
$ sudo update-grub2
$ sudo update-initramfs -u
```

Y cuando reiniciemos ya estará solucionado.

vga=769 deprecated
------------------

Sin embargo, tenía otro [problema con el arranque][] y es que me
aparecía el siguiente mensaje de error:

```bash
Error "vga=769 is deprecated.
```

Para solucionarlo, editamos nuevamente el archivo `/etc/default/grub` y
modificamos la línea:

```bash
GRUB_CMDLINE_LINUX=" vga=769"
```

por

```bash
GRUB_CMDLINE_LINUX=" gfxpayload=true gfxpayload=1280x960x24"
```

Cuando reiniciemos ya estará solucionado.

  [actualizar a Maverick Meerkat]: {filename}/admin/actualizando-ubuntu-a-la-ultima-distribucion-de-forma-remota.md
    "actualizar a Maverick Meerkat"
    "actualizar a maverick meerkat de forma remota"
  [funcionó con una ATI Radeon]: http://www.nosinmiubuntu.com/2010/10/solucion-para-el-plymouth-en-ubuntu.html
    "funcionó con una ATI Radeon"
  [problema con el arranque]: http://achmadz.blogspot.com/2010/03/ubuntu-910-karmic-koala-error-is.html
    "problema con el arranque"
