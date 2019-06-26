Title: La guardiana de la puerta
Date: 2010-10-22 19:37
Author: Nacho Cano
Tags: detección de intrusos, el guardián de la puerta de Zuul, inicio de sesión, mail, script
Slug: la-guardiana-de-la-puerta

¿A veces no os gustaría saber si el que se mete en vuestra casa no es el
maestro de las llaves?

![la guardiana de la puerta]({static}/images/guardiana-300x260.jpg)

En [ubuntu][], los _scripts_ que estén en el directorio `/etc/profile.d`
se ejecutan cada vez que un usuario inicia la sesión. Si nuestro
servidor sólo lo usamos nosotros, y si no también, podríamos [enviarnos
un correo cada vez que un usuario se conecta][]. Así, al menos,
podríamos saber si alguien ha entrado con nuestro usuario.

  [ubuntu]: http://serverfault.com/questions/77983/run-shell-script-each-time-any-user-logs-on
    "ubuntu"
  [enviarnos un correo cada vez que un usuario se conecta]: http://terminus.ignaciocano.com/wp-uploads/linked/user-has-logged-in.sh
    "enviarnos un correo cada vez que un usuario se conecta"
