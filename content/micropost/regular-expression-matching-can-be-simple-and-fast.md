Title: Regular Expression Matching Can Be Simple And Fast
Date: 2012-06-21 18:21
Author: Nacho Cano
Slug: regular-expression-matching-can-be-simple-and-fast

> Historically, regular expressions are one of computer science’s
> shining examples of how using good theory leads to good programs. They
> were originally developed by theorists as a simple computational
> model, but Ken Thompson introduced them to programmers in his
> implementation of the text editor QED for CTSS. Dennis Ritchie
> followed suit in his own implementation of QED, for GE-TSS. Thompson
> and Ritchie would go on to create Unix, and they brought regular
> expressions with them. By the late 1970s, regular expressions were a
> key feature of the Unix landscape, in tools such as ed, sed, grep,
> egrep, awk, and lex.
>
> Today, regular expressions have also become a shining example of how
> ignoring good theory leads to bad programs. The regular expression
> implementations used by today’s popular tools are significantly slower
> than the ones used in many of those thirty-year-old Unix tools.
>
> This article reviews the good theory: regular expressions, finite
> automata, and a regular expression search algorithm invented by Ken
> Thompson in the mid-1960s. It also puts the theory into practice,
> describing a simple implementation of Thompson’s algorithm. That
> implementation, less than 400 lines of C, is the one that went head to
> head with Perl above. It outperforms the more complex real-world
> implementations used by Perl, Python, PCRE, and others. The article
> concludes with a discussion of how theory might yet be converted into
> practice in the real-world implementations.

- Russ Cox | [swtch.com/\~rsc][]

  [swtch.com/\~rsc]: http://swtch.com/~rsc/regexp/regexp1.html
    "Regular Expression Matching Can Be Simple And Fast"
