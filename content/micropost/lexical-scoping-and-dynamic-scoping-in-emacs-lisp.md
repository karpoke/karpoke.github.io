Title: lexical scoping and dynamic scoping in Emacs Lisp
Date: 2012-06-26 12:39
Author: Nacho Cano
Slug: lexical-scoping-and-dynamic-scoping-in-emacs-lisp

> In this article, I demonstrate:
>
> -   difference between dynamic scoping and lexical scoping in Emacs
>     Lisp
> -   what to watch out for with dynamic scoping
> -   what you can do with lexical scoping and lexical closures
> -   what happens when you mix lexical scoping code and dynamic scoping
>     code
>
> Emacs Lisp is always dynamically scoped in Emacs 23 and below. Support
> for lexical scoping is added to Emacs 24. Nice because many agree that
> lexical scoping makes more sense in most cases than dynamic scoping
> does. You’ll see why soon in this article. If you have an el file that
> you want to load with lexical scoping, you can add -\*-
> lexical-binding: t -\*- as the first line, then when Emacs 24 loads
> the file, it will apply lexical scoping to the code in that el file.

» [yoo2080.wordpress.com][]

  [yoo2080.wordpress.com]: http://yoo2080.wordpress.com/2011/12/31/lexical-scoping-and-dynamic-scoping-in-emacs-lisp/
    "lexical scoping and dynamic scoping in Emacs Lisp"
