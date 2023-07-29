.. _grammar:

Grammar
-------

.. _Lark: https://github.com/lark-parser/lark

The parsing tool used is Lark_. We generate a LALR(1) parser using the following grammar
(which can be found at :code:`sci_watch/assets/grammar.lark`).

.. code-block::

    query                           : factor
                                    | query AND factor -> and_clause
                                    | query OR factor -> or_clause
                                    | query NOT factor -> not_clause

    !factor                         : token -> token
                                    | INTITLE_KW COLON scoped_token -> in_title_clause
                                    | INCONTENT_KW COLON scoped_token -> in_content_clause
                                    | BEGIN_KW COLON scoped_token -> begin_clause

    token                           : word_with_wildcard
                                    | expr
                                    | LEFT_PAR query RIGHT_PAR -> parenthesis_clause

    scoped_token                    : word_with_wildcard
                                    | expr
                                    | LEFT_PAR scoped_query RIGHT_PAR -> parenthesis_clause

    scoped_query                    : scoped_token
                                    | scoped_query AND scoped_token -> and_clause
                                    | scoped_query OR scoped_token -> or_clause
                                    | scoped_query NOT scoped_token -> not_clause

    expr                            : QUOTE /[A-Za-z0-9\-]+/ ( /[A-Za-z0-9\-]+/)* QUOTE -> expression
                                    | QUOTE /[A-Za-z0-9\-]+/ ( /[A-Za-z0-9\-]+/)* QUOTE TILDE distance -> proximity

    word_with_wildcard              : /[A-Za-z0-9\-\*\?]+/
                                    | /([A-Za-z0-9\-]*\??[A-Za-z0-9\-]*)+\*/
    distance                        : /[1-9][0-9]*/

    QUOTE                           : "\""
    AND                             : "AND"
    OR                              : "OR"
    NOT                             : "NOT"
    LEFT_PAR                        : "("
    RIGHT_PAR                       : ")"
    TILDE                           : "~"
    COLON                           : ":"
    SPACE                           : /\s+/

    INTITLE_KW                      : "intitle"i
    INCONTENT_KW                    : "incontent"i
    BEGIN_KW                        : "begin"i

    %ignore SPACE

The entry point is **query**.