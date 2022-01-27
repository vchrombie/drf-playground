from django.db import models

from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    title = models.CharField(
        verbose_name="Snippet Title",
        max_length=100,
        blank=True,
        default=''
    )
    created = models.DateTimeField(
        verbose_name="Created Time",
        auto_now_add=True
    )
    code = models.TextField(
        verbose_name="Code"
    )
    linenos = models.BooleanField(
        verbose_name='Linenos',
        default=False,
    )
    language = models.CharField(
        verbose_name="Programming Language",
        max_length=40,
        choices=LANGUAGE_CHOICES,
        default='text',
    )
    style = models.CharField(
        verbose_name='Style',
        max_length=40,
        choices=STYLE_CHOICES,
        default='friendly'
    )
    owner = models.ForeignKey(
        'auth.User',
        verbose_name='Owner of the Snippet',
        related_name='snippets',
        on_delete=models.CASCADE
    )
    highlight = models.TextField()

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style,
            linenos=linenos,
            full=True,
            **options
        )

        self.highlight = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)
