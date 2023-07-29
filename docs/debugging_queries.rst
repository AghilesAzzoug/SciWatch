.. _debugging_queries:

Debugging queries
-----------------

For debugging queries, i.e. knowing which parts of the query matched (evaluated to true) versus which parts didn't match, you can
use the script :code:`scripts/01_visualize_query_evaluation.py`, as follows:

.. code-block:: sh

    python scripts/01_visualize_query_evaluation.py --query "hello AND (world OR title)" --content "hello content" --title "a title" --print-tree --show-graph

You will get (because of :code:`--show-graph` argument) the following graph on your **browser**:

.. image:: _static/sample_query_evaluation_image.png
    :width: 800
    :alt: Evaluation tree
    :align: center

.. warning::
    For very long queries, the graph might be unreadable. Prefer the :code:`--print-tree` option alone.

You will also get (because of :code:`--print-tree` argument) the following graph on your **terminal**:

.. image:: _static/sample_query_evaluation_cmd.png
    :width: 800
    :alt: Evaluation tree
    :align: center



.. note::
    Content (i.e. the argument :code:`--content`) can be a path to a long file containing the content