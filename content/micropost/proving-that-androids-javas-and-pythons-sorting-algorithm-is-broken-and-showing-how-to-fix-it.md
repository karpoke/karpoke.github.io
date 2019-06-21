Title: Proving that Android’s, Java’s and Python’s sorting algorithm is broken (and showing how to fix it)
Date: 2015-02-28 14:31
Author: Nacho Cano
Slug: proving-that-androids-javas-and-pythons-sorting-algorithm-is-broken-and-showing-how-to-fix-it

> Tim Peters developed the Timsort hybrid sorting algorithm in 2002. It
> is a clever combination of ideas from merge sort and insertion sort,
> and designed to perform well on real world data. TimSort was first
> developed for Python, but later ported to Java (where it appears as
> java.util.Collections.sort and java.util.Arrays.sort) by Joshua Bloch
> (the designer of Java Collections who also pointed out that most
> binary search algorithms were broken). TimSort is today used as the
> default sorting algorithm for Android SDK, Sun’s JDK and OpenJDK.
> Given the popularity of these platforms this means that the number of
> computers, cloud services and mobile phones that use TimSort for
> sorting is well into the billions. Fast forward to 2015. After we had
> successfully verified Counting and Radix sort implementations in Java
> (J. Autom. Reasoning 53(2), 129-139) with a formal verification tool
> called KeY, we were looking for a new challenge. TimSort seemed to fit
> the bill, as it is rather complex and widely used. Unfortunately, we
> weren’t able to prove its correctness. A closer analysis showed that
> this was, quite simply, because TimSort was broken and our theoretical
> considerations finally led us to a path towards finding the bug
> (interestingly, that bug appears already in the Python
> implementation). This blog post shows how we did it.

- Stijn de Gouw | [envisage-project.eu][]

  [envisage-project.eu]: http://envisage-project.eu/proving-android-java-and-python-sorting-algorithm-is-broken-and-how-to-fix-it/
    "Proving that Android’s, Java’s and Python’s sorting algorithm is broken (and showing how to fix it)"
