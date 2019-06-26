Title: LaTeX en Wordpress
Date: 2011-03-29 18:54
Author: Nacho Cano
Tags: ecuaciones de segundo grado, latex, plugin, wordpress
Slug: latex-en-wordpress

Descarga el [plugin de LaTeX para Wordpress][]. Luego,
escribe:

```latex
\large\begin{align*}
ax^2+bx+c &= 0 \\
x^2+\frac{b}{a}x+\frac{c}{a} &= 0 \\
x^2+\frac{b}{a}x &= -\frac{c}{a} \\
x^2+\frac{b}{a}x+\frac{b^2}{4a^2} &= \frac{b^2}{4a^2} - \frac{c}{a} \\
(x+\frac{b}{2a})^2 &= \frac{b^2}{4a^2} - \frac{4ac}{4a^2} \\
x+\frac{b}{2a} &= \pm\sqrt{\frac{b^2-4ac}{4a^2}} \\
x+\frac{b}{2a} &= \frac{\pm\sqrt{b^2-4ac}}{2a} \\
x &= \frac{-b\pm\sqrt{b^2-4ac}}{2a}
\end{align*}
```

El resultado será parecido a éste:

$$
\large\begin{align*}
ax^2+bx+c &= 0 \\
x^2+\frac{b}{a}x+\frac{c}{a} &= 0 \\
x^2+\frac{b}{a}x &= -\frac{c}{a} \\
x^2+\frac{b}{a}x+\frac{b^2}{4a^2} &= \frac{b^2}{4a^2} - \frac{c}{a} \\
(x+\frac{b}{2a})^2 &= \frac{b^2}{4a^2} - \frac{4ac}{4a^2} \\
x+\frac{b}{2a} &= \pm\sqrt{\frac{b^2-4ac}{4a^2}} \\
x+\frac{b}{2a} &= \frac{\pm\sqrt{b^2-4ac}}{2a} \\
x &= \frac{-b\pm\sqrt{b^2-4ac}}{2a}
\end{align*}
$$

  [plugin de LaTeX para Wordpress]: http://wordpress.org/extend/plugins/latex/
    "plugin de LaTeX para Wordpress"
