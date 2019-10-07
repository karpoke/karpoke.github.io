Title: Conseguir la lista actualizada de medios AEDE para bloquearlos
Date: 2014-07-27 11:28
Author: Nacho Cano
Tags: aede, awk, boycott, chrome, curl, firefox, greasemonkey, hosts, lynx, plugin, script, sed, sort, uniq, wordpress
Slug: conseguir-la-lista-actualizada-de-medios-aede-para-bloquearlos
Related: hphosts-evitando-la-navegacion-por-dominios-maliciosos

La lista de medios asociados a AEDE se puede consultar en su página:
www.aede.es/publica/Periodicos_Asociados.asp. Si no queremos visitar ni
por error las páginas de dichos medios, tenemos diferentes alternativas,
desde _scripts_ de GreaseMonkey para [Firefox][] y complementos para
[Chrome][], hasta [añadir los dominios en el fichero `/etc/hosts`][añadir los dominios en el fichero /etc/hosts],
tal como haríamos si fuesen [dominios maliciosos][], o incluso
complementos para [WordPress][].

Los siguientes comandos nos facilitan descargar la lista de dominios:

```bash
$ lynx -dump http://www.aede.es/publica/Periodicos_Asociados.asp |
  \grep -Eo "http://[^/\"]+" |
  \grep -v aede.es |
  sort |
  uniq |
  awk "{gsub(/http:\/\//, \"\"); print; gsub(/www\./, \"\"); print; }" |
  sed 's/^/127.0.0.1  /'
```

Una alternativa a `lynx` sería utilizar el comando `curl`:

```bash
$ curl -so- http://www.aede.es/publica/Periodicos_Asociados.asp |
  \grep -Eo "http://[^/\"]+" |
  \grep -v aede.es |
  sort |
  uniq |
  awk "{gsub(/http:\/\//, \"\"); print; gsub(/www\./, \"\"); print; }" |
  sed 's/^/127.0.0.1  /'
```

Para que la lista sea más completa, también se podrían añadir los
dominios alternativos (.com, .es, etc) o dominios de otras páginas de
cada grupo de prensa: <http://pykiss.github.io/anti-AEDE/domains.list>.

Referencias
-----------

» [Los usuarios de Menéame se levantan contra los medios de AEDE][]

  [Firefox]: https://github.com/pykiss/anti-AEDE/blob/master/script.user.js
    "Firefox"
  [Chrome]: https://chrome.google.com/webstore/detail/aede-blocker/olfbaiingdbeoihdemklgmakblhcgpmn?hl=es
    "Chrome"
  [añadir los dominios en el fichero /etc/hosts]: http://anotacionsalmarge.wordpress.com/2014/02/17/bloquejar-pagines-web/
    "añadir los dominios en el fichero /etc/hosts"
  [dominios maliciosos]: {filename}/admin/hphosts-evitando-la-navegacion-por-dominios-maliciosos.md
    "hpHosts, evitando la navegación por dominios maliciosos"
  [WordPress]: https://wordpress.org/plugins/canon-aede/
    "WordPress"
  [Los usuarios de Menéame se levantan contra los medios de AEDE]: http://www.elconfidencial.com/tecnologia/2014-02-17/los-usuarios-de-meneame-se-levantan-contra-los-medios-de-aede_90486/
    "Los usuarios de Menéame se levantan contra los medios de AEDE"
