Title: pci_add_option_rom: failed to find romfile "pxe-rtl8139.bin"
Date: 2011-01-14 22:07
Author: Nacho Cano
Tags: dsl, pxe-rtl8139.bin, qemu, romfile
Slug: pci_add_option_rom-failed-to-find-romfile-pxe-rtl8139-bin

Trasteando con `qemu` y `Damn Small Linux`, creamos una imagen de disco
de 500 MB:

```bash
$ qemu-img create -f qcow hd-500m.img 500M
```

Y lanzamos el programa:

```bash
$ qemu -hda hd-500m.img -cdrom dsl-4.4.10.iso -boot d -m 128 -localtime
```

En seguida nos aparece el siguiente mensaje:

```bash
pci_add_option_rom: failed to find romfile "pxe-rtl8139.bin"
```

El error que aparece, aunque no evita que la distribución arranque, se
debe a que en Ubuntu, por defecto, [no están instalados los binarios][]
para permitir que el sistema operativo emulado arranque por red.

La [solución][] es instalar el paquete `kvm-pxe`:

```bash
$ sudo aptitude install kvm-pxe
```

  [no están instalados los binarios]: http://wiki.tudos.org/QEmu
    "no están instalados los binarios"
  [solución]: http://answers.launchpad.net/ubuntu/+source/qemu-kvm/+question/110660
    "solución"
