.. _query:

Query syntax
============
Queries can be defined by the following components (for more details, see :ref:`grammar`).

Atoms
-----

Atoms represent the basic components of each query (and can be queries on their own).

+---------------------+---------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| Type                | Syntax                          | Description                                                                                                           |
+=====================+=================================+=======================================================================================================================+
| Simple words        |  word without spaces            |  A normal word without special characters. Evaluated to :code:`true` if the word is present in the `search scope`_.   |
+---------------------+---------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| Word with wildcards |  See Wildcards_ syntax          |  See Wildcards_ descriptions.                                                                                         |
+---------------------+---------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| Expression          |  "first second third ..."       |  A list of words separated by white spaces (words cannot contain wildcards). Evaluated to :code:`true` if the exact   |
|                     |                                 |  expression if found the `search scope`_.                                                                             |
+---------------------+---------------------------------+-----------------------------------------------------------------------------------------------------------------------+
| Proximity           |  expression ~ distance          |  Expression ~ distance (e.g. "hello world" ~ 2). Evaluated to :code:`true` if all                                     |
|                     |                                 |  the words are present in the `search scope`_ (in the same order) separated by at most *distance* words.              |
+---------------------+---------------------------------+-----------------------------------------------------------------------------------------------------------------------+


.. warning::
    Note that all atoms are **case insensitive** and that's intended.

Logical operators
-----------------

+----------+---------------------------+--------------------------------------------------------------------------------------------------+
| Operator | Syntax                    | Description                                                                                      |
+==========+===========================+==================================================================================================+
| AND      |  *left* **AND** *right*   |  Logical **and** operator. **Both** conditions must be satisfied.                                |
+----------+---------------------------+--------------------------------------------------------------------------------------------------+
| OR       |  *left* **OR** *right*    |  Logical **or** operator. **At least one** condition must be satisfied.                          |
+----------+---------------------------+--------------------------------------------------------------------------------------------------+
| NOT      |  *left* **NOT** *right*   |  Exclusion operator. Equivalent to boolean (*left* **AND NOT** *right*).                         |
|          |                           |  To be evaluated to :code:`true`, *left* must be :code:`true` **and** *right* to :code:`false`.  |
+----------+---------------------------+--------------------------------------------------------------------------------------------------+

.. _search scope:

Search scopes
-------------

+--------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| Search Scope | Keyword    | Syntax                      | Description                                                                                                    |
+==============+============+=============================+================================================================================================================+
| Title        | intitle    |  **intitle:** *subquery*    |  Subquery will be searched **only in title.**                                                                  |
+--------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| Content      | incontent  |  **incontent:** *subquery*  |  Subquery will be searched **only in document content.**                                                       |
+--------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+
| Global       |            |  *subquery*                 |  **Default scope**. If nothing is specified, the subquery will be searched in **both content and title.**      |
+--------------+------------+-----------------------------+----------------------------------------------------------------------------------------------------------------+

.. note::
    Search scope keywords are case insensitive (i.e. "INTITLE:", "Intitle:", and "intitle:" are equivalent).

.. note::
    Another search scope (:code:`begin`) will be implemented soon and will look up for keyword only in the beginning of document content.

.. _Wildcards:

Wildcards
---------

Currently, there's only two wildcards implemented, and their behaviors are very different from their equivalent in Regex.

+------------+---------------------------+---------------------------------------------------------------------------------------------------------------+
| Wildcard   | Syntax                    | Description                                                                                                   |
+============+===========================+===============================================================================================================+
| :code:`*`  |  *word* *                 |  Will match everything or nothing. E.g. hell* would match hell, hello, helloo, and hellfires.                 |
+------------+---------------------------+---------------------------------------------------------------------------------------------------------------+
| :code:`?`  |  *word* ?                 |  Will match one character or nothing. E.g. hell? would match hell, hello **but not** helloo neither hellfires |
+------------+---------------------------+---------------------------------------------------------------------------------------------------------------+


Priorities
----------
Priorities are defined in this order (from highest to lower):

* Parenthesis
* Expressions & Proximities
* Scoped queries
* Logical operators

Examples:

- :code:`intitle:hello AND world` is equivalent to :code:`(intitle:(hello) AND world)`
- :code:`hello OR short AND fake` is equivalent to :code:`((hello OR short) AND fake)`
