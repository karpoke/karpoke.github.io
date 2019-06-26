Title: JABH - Just Another Bash Hacker
Date: 2010-07-28 14:03
Author: Nacho Cano
Tags: jabh, japh, just another bash hacker
Slug: jabh

Se le llama [JAPH][] a un programa en Perl que escribe "Just another
Perl hacker,". JABH vendría a ser algo parecido, en Bash:

```bash
$ s="Jaescunrhkso  ettBhr haa,";for y in {0..4};do for x in {0..4};do echo -n "${s:$((5*x+y)):1}";done;done
Just another Bash hacker,
```

Otra versión, algo más críptica:

```bash
$ s="Jaescunrhkso  ettBhr haa,";t=4;f(){ eval "for $1 in {0..$t};do eval $2;done;";};f x ';f y "echo -n \"'\''\${s:\$(((t+1)*y+x)):1}'\''\""'
Just another Bash hacker,
```

  [JAPH]: http://en.wikipedia.org/wiki/Just_another_Perl_hacker "JAPH"
    "JAPH"
