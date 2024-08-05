#!/usr/bin/env python3


class Token:
    """Token objects store a piece of text (in the end a single token) with additional information.

    Parameters
    ----------
    text : str
        The text that makes up the token object
    markup : bool, (default=False)
        Is the token a markup token?
    markup_class : {'start', 'end'}, optional (default=None)
        If `markup=True`, then `markup_class` must be either "start" or "end".
    markup_eos : bool, optional (default=None)
        Is the markup token a sentence boundary?
    locked : bool, (default=False)
        Mark the token as locked.
    token_class : {'URL', 'XML_entity', 'XML_tag', 'abbreviation', 'action_word', 'amount', 'date', 'email_address', 'emoticon', 'hashtag', 'measurement', 'mention', 'number', 'ordinal', 'regular', 'semester', 'symbol', 'time'}, optional (default=None)
        The class of the token, e.g. "regular", "emoticon", "URL", etc.
    space_after : bool, (default=True)
        Was there a space after the token in the original data?
    original_spelling : str, optional (default=None)
        The original spelling of the token, if it is different from the one in `text`.
    first_in_sentence : bool, (default=False)
        Is it the first token of a sentence?
    last_in_sentence : bool, (default=False)
        Is it the last token of a sentence?
    character_offset : tuple, (default=None)
        Character offset of the token in the input as tuple `(start, end)`
        such that `input[start:end] == text` (if there are no changes to
        the token text during tokenization)

    """

    token_classes = {
        "URL",
        "XML_entity",
        "XML_tag",
        "abbreviation",
        "action_word",
        "amount",
        "date",
        "email_address",
        "emoticon",
        "hashtag",
        "measurement",
        "mention",
        "number",
        "ordinal",
        "regular",
        "semester",
        "symbol",
        "time",
    }

    def __init__(
            self,
            text,
            *,
            markup=False,
            markup_class=None,
            markup_eos=None,
            locked=False,
            token_class=None,
            space_after=True,
            original_spelling=None,
            first_in_sentence=False,
            last_in_sentence=False,
            character_offset=None
    ):
        self.text = text
        if markup:
            assert markup_class is not None, "You need to specify a `markup_class` for markup tokens."
            assert markup_eos is not None, "You need to provide a value for `markup_eos` for markup tokens."
        if markup_class is not None:
            assert markup, "You can only specify a `markup_class` for markup tokens."
            assert markup_class == "start" or markup_class == "end", f"'{markup_class}' is not a recognized markup class."
        if markup_eos is not None:
            assert markup, "You can only use `markup_eos` for markup tokens."
            assert isinstance(markup_eos, bool), f"'{markup_eos}' is not a Boolean value."
        if token_class is not None:
            assert token_class in self.token_classes, f"'{token_class}' is not a recognized token class."
        self.markup = markup
        self.markup_class = markup_class
        self.markup_eos = markup_eos
        self._locked = locked
        self.token_class = token_class
        self.space_after = space_after
        self.original_spelling = original_spelling
        self.first_in_sentence = first_in_sentence
        self.last_in_sentence = last_in_sentence
        self.character_offset = character_offset

    def __str__(self):
        return self.text

    @property
    def extra_info(self):
        """String representation of extra information.

        Returns
        -------
        str
            A string representation of the `space_after` and `original_spelling` attributes.

        Examples
        --------
        >>> tok = Token(":)", token_class="regular", space_after=False, original_spelling=": )")
        >>> print(tok.text)
        :)
        >>> print(tok.extra_info)
        SpaceAfter=No, OriginalSpelling=": )"

        """
        info = []
        if not self.space_after:
            info.append("SpaceAfter=No")
        if self.original_spelling is not None:
            info.append("OriginalSpelling=\"%s\"" % self.original_spelling)
        return ", ".join(info)
