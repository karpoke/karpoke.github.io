Title: Linux containers in 500 lines of code
Date: 2016-11-01 15:09
Author: Nacho Cano
Tags: contenedores en linux, c, kernel, cgroups, strlimit, llamadas de sistema, puntos de montaje, recursos de sistema, configuración de red
Slug: linux-containers-in-500-lines-of-code
Relatd:

> I’ve used Linux containers directly and indirectly for years, but I wanted
> to become more familiar with them. So I wrote some code. This used to be 500
> lines of code, I swear, but I’ve revised it some since publishing; I’ve
> ended up with about 70 lines more.
>
> I wanted specifically to find a minimal set of restrictions to run untrusted
> code. This isn’t how you should approach containers on anything with any
> exposure: you should restrict everything you can. But I think it’s important
> to know which permissions are categorically unsafe!

- Lizzie Dixon | [blog.lizzie.io][]

  [blog.lizzie.io]: https://blog.lizzie.io/linux-containers-in-500-loc.html
    "Linux containers in 500 lines of code"
