.. _iftglobal-reference:

ift_global API
==============

Public API
----------


In python, the distinction between public and private API implementations are not always directly enforceable within the code base.
Accordingly, within this section we will clarify what the user of this API can safely use as classes, functions or methods without being affected by further releases.

In general,

- Methods, functions or classes starting with an underscore ```_``` should be considered as **private**.
- A module that starts with an ```_``` should be considered as **private**.





.. toctree::
    :maxdepth: 1
    :hidden:
    :titlesonly:

    ift_global <main_namespace>
    ift_global.email <email_functionality>