NetAuth for Python
==================

A `NetAuth <https://netauth.org>`_ client library for Python.

.. currentmodule:: netauth

.. autoclass:: NetAuth
   :members:

Data Types
~~~~~~~~~~

.. autoclass:: EntityMeta
   :members:

.. autoclass:: Entity
   :members:

.. autoclass:: Group
   :members:

.. currentmodule:: netauth.v2

.. autoclass:: SubSystemStatus
   :members:

.. autoclass:: ServerStatus
   :members:

Enumerations
~~~~~~~~~~~~

.. currentmodule:: netauth

.. autoenum:: Capability

.. autoenum:: ExpansionMode

.. currentmodule:: netauth.v2

.. autoenum:: Action

.. autoenum:: RuleAction

Token Cache
~~~~~~~~~~~

.. currentmodule:: netauth.cache

.. autoclass:: TokenCache
   :members:

.. autoclass:: FSTokenCache
   :members:

.. autoclass:: MemoryTokenCache
   :members:


Exceptions
~~~~~~~~~~

.. currentmodule:: netauth.error

.. autoclass:: NetAuthException
   :members:

.. autoclass:: NetAuthRpcError
   :members:

.. autoclass:: RequestorUnqualifiedError
   :members:

.. autoclass:: MalformedRequestError
   :members:

.. autoclass:: InternalError
   :members:

.. autoclass:: UnauthenticatedError
   :members:

.. autoclass:: ReadOnlyError
   :members:

.. autoclass:: ExistsError
   :members:

.. autoclass:: DoesNotExistError
   :members:
