Title: GNU Make in Detail for Beginners
Date: 2012-06-28 12:56
Author: Nacho Cano
Slug: gnu-make-in-detail-for-beginners

> Large projects can contain thousands of lines of code, distributed in
> multiple source files, written by many developers and arranged in
> several subdirectories. A project may contain several component
> divisions. These components may have complex inter-dependencies ” for
> example, in order to compile component X, you have to first compile Y;
> in order to compile Y, you have to first compile Z; and so on. For a
> large project, when a few changes are made to the source, manually
> recompiling the entire project each time is tedious, error-prone and
> time-consuming.
>
> Make is a solution to these problems. It can be used to specify
> dependencies between components, so that it will compile components in
> the order required to satisfy dependencies. An important feature is
> that when a project is recompiled after a few changes, it will
> recompile only the files which are changed, and any components that
> are dependent on it. This saves a lot of time. Make is, therefore, an
> essential tool for a large software project.
>
> Each project needs a Makefile ” a script that describes the project
> structure, namely, the source code files, the dependencies between
> them, compiler arguments, and how to produce the target output
> (normally, one or more executables). Whenever the make command is
> executed, the Makefile in the current working directory is
> interpreted, and the instructions executed to produce the target
> outputs. The Makefile contains a collection of rules, macros, variable
> assignments, etc. (’Makefile’ or ’makefile’ are both acceptable.)

- Sarath Lakshman | [linuxforu.com][]

  [linuxforu.com]: http://www.linuxforu.com/2012/06/gnu-make-in-detail-for-beginners/
    "GNU Make in Detail for Beginners"
