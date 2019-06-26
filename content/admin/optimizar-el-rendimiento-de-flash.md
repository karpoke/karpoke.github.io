Title: Optimizar el rendimiento de Flash
Date: 2011-01-11 12:33
Author: Nacho Cano
Tags: adobe, flash, gpu, plugin, ubuntu
Slug: optimizar-el-rendimiento-de-flash

Leyendo el blog [Usemos Linux][], veo que podemos [optimizar el
rendimiento del uso de Flash][], configurando el complemento para que no
realice algunas comprobaciones de la GPU, con lo que se alivia el
consumo de CPU y de memoria.

Sin embargo, no en todos los casos se conseguirá esta mejora del
rendimiento. Esto [dependerá][] de:

1.  el contenido debe estar preparado para utilizar la GPU, de lo
    contrario, la reproducción hasta podría volverse más lenta.
2.  los requerimientos de hardware para la GPU en el modo GPU son
    importantes.
3.  no se puede garantizar la fidelidad de los _píxels_, ya que podrían
    cambiar de color.
4.  no importa si el _frame rate_ está por encima de 60, nunca será
    superior. De hecho, podemos esperar que sea entre 50 y 55 fps.
5.  no se debería usar, o abusar, del modo GPU para todo el contenido
    Flash que se utilice en una página, ya que degradaría bastante la
    respuesta del navegador.
6.  el rendimiento también depende de los fabricantes y sus
    controladores.

Para configurar el complemento, deberemos crear el fichero de configuración
`mms.cfg`. Ejecutamos:

```bash
$ sudo mkdir /etc/adobe
$ echo "OverrideGPUValidation=true" | sudo tee /etc/adobe/mms.cfg
```

También podemos configurarlo como preferencias de usuario:

```bash
$ mkdir ~/adobe
$ echo "OverrideGPUValidation=true" >> ~/.adobe/mms.cfg
```

  [Usemos Linux]: http://usemoslinux.blogspot.com/2011/01/como-evitar-que-flash-arruine-tu.html
    "Usemos Linux"
  [optimizar el rendimiento del uso de Flash]: http://blogs.adobe.com/penguinswf/2008/08/secrets_of_the_mmscfg_file_1.html
    "optimizar el rendimiento del uso de Flash"
  [dependerá]: http://www.kaourantin.net/2008/05/what-does-gpu-acceleration-mean.html
    "dependerá"
