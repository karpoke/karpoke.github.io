Title: Bash One-Liners Explained, Part III: All about redirections
Date: 2012-10-09 19:54
Author: Nacho Cano
Slug: bash-one-liners-explained-part-iii-all-about-redirections

> Working with redirections in bash is really easy once you realize that
> it’s all about manipulating file descriptors. When bash starts it
> opens the three standard file descriptors: stdin (file descriptor 0),
> stdout (file descriptor 1), and stderr (file descriptor 2). You can
> open more file descriptors (such as 3, 4, 5, ...), and you can close
> them. You can also copy file descriptors. And you can write to them
> and read from them.
>
> File descriptors always point to some file (unless they’re closed).
> Usually when bash starts all three file descriptors, stdin, stdout,
> and stderr, point to your terminal. The input is read from what you
> type in the terminal and both outputs are sent to the terminal.

- Peteris Krumins | [catonmat.net][]

  [catonmat.net]: http://www.catonmat.net/blog/bash-one-liners-explained-part-three/
    "Bash One-Liners Explained, Part III: All about redirections"
