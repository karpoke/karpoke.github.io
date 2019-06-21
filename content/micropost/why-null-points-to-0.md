Title: Why NULL points to 0?
Date: 2012-06-26 02:40
Author: Ignacio Cano
Slug: why-null-points-to-0

> A few years ago I would answer the above question with ”because NULL
> is defined as a void pointer to 0”, which is only half correct (and
> close to being wrong). The answer to this question is much more
> complicated and thus much more interesting.
>
> Let’s start with checking what the C standards (or actually drafts of
> the standards) say about the (in)famous NULL ptr. The
> green/yellow/orange colors mark the part that caught my attention.
> I’ll leave the C++0x case for another time (C++0x introduces the
> nullptr of std::nullptr_t type btw). For TL;DR scroll down, I
> summarize the points anyway.

- [gynvael.coldwind.pl][]

  [gynvael.coldwind.pl]: http://gynvael.coldwind.pl/
    "Why NULL points to 0?"
