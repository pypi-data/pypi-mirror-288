.. _injectable:
.. role:: python(code)
   :language: python

Injectable: Dependency Injection for Humans™
============================================

`Usage Examples 🚩 <https://injectable.readthedocs.io/en/latest/usage/index.html>`_ | `Developer Reference 👩‍💻 <https://injectable.readthedocs.io/en/latest/reference/index.html>`_ | `Authors 👫 <https://injectable.readthedocs.io/en/latest/authors.html>`_

.. start-badges

.. list-table::
    :stub-columns: 1

    * - license
      - |license|
    * - docs
      - |docs|
    * - tests
      - |build| |coveralls| |reliability| |security| |black| |flake8|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |platforms| |downloads|
.. |docs| image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=plastic
    :target: https://injectable.readthedocs.io/en/latest/
    :alt: Documentation

.. |build| image:: https://github.com/roo-oliv/injectable/actions/workflows/build.yml/badge.svg
    :alt: Build Status
    :target: https://github.com/roo-oliv/injectable/actions/workflows/build.yml

.. |coveralls| image:: https://coveralls.io/repos/github/allrod5/injectable/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/allrod5/injectable?branch=master

.. |reliability| image:: https://sonarcloud.io/api/project_badges/measure?project=roo-oliv_injectable&metric=reliability_rating
    :alt: Reliability Rating
    :target: https://sonarcloud.io/dashboard?id=roo-oliv_injectable

.. |security| image:: https://sonarcloud.io/api/project_badges/measure?project=roo-oliv_injectable&metric=security_rating
    :alt: Security Rating
    :target: https://sonarcloud.io/dashboard?id=roo-oliv_injectable

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style
    :target: https://github.com/psf/black

.. |flake8| image:: https://img.shields.io/badge/standards-flake8-blue
    :alt: Standards
    :target: https://flake8.pycqa.org/en/latest/

.. |version| image:: https://img.shields.io/pypi/v/injectable.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/injectable

.. |wheel| image:: https://img.shields.io/pypi/wheel/injectable.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/injectable

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/injectable.svg
    :alt: Supported versions
    :target: https://pypi.org/project/injectable

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/injectable.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/injectable

.. |license| image:: https://img.shields.io/github/license/roo-oliv/injectable
    :alt: GitHub license
    :target: https://github.com/roo-oliv/injectable/blob/master/LICENSE

.. |platforms| image:: https://img.shields.io/badge/platforms-windows%20%7C%20macos%20%7C%20linux-lightgrey
    :alt: Supported Platforms
    :target: https://github.com/roo-oliv/injectable/blob/master/.github/workflows/build.yml#L11

.. |downloads| image:: https://pepy.tech/badge/injectable/month
    :alt: Downloads per Month
    :target: https://pepy.tech/project/injectable/month


.. end-badges

**Injectable** is an elegant and simple Dependency Injection framework built with Heart
and designed for Humans.

.. list-table::
    :header-rows: 0

    * - .. code:: python

            from typing import Annotated, List
            from injectable import Autowired, autowired
            from models import Database
            from messaging import Broker

            class Service:
                @autowired
                def __init__(
                    self,
                    database: Annotated[Database, Autowired],
                    message_brokers: Annotated[List[Broker], Autowired],
                ):
                    pending = database.get_pending_messages()
                    for broker in message_brokers:
                        broker.send_pending(pending)

        .. code:: python

            from abc import ABC

            class Broker(ABC):
                def send_pending(messages):
                    ...

      - .. code:: python

            from injectable import injectable

            @injectable
            class Database:
                ...

        .. code:: python

            from messaging import Broker
            from injectable import injectable

            @injectable
            class KafkaProducer(Broker):
                ...

        .. code:: python

            from messaging import Broker
            from injectable import injectable

            @injectable
            class SQSProducer(Broker):
                ...

Features you'll love ❤️
-----------------------

* **Autowiring**: injection is transparent to the function. Just decorate the function
  with :python:`@autowired` and annotate parameters with :python:`Autowired`, that's it.

* **Automatic dependency discovery**: just call :python:`load_injection_container()` at
  the root of your project or pass the root path as an argument. All classes decorated
  with :python:`@injectable` will be automatically discovered and ready for injection.

* **Qualifier overloading**: declare as many injectables as you like for a single
  qualifier or extending the same base class. You can inject all of them just by
  specifying a :python:`typing.List` to :python:`Autowired`:
  :python:`deps: Annotated[List["qualifier"], Autowired]`.

* **Transparent lazy initialization**: passing the argument :python:`lazy=True` for
  :python:`Autowired` will make your dependency to be initialized only when actually used, all
  in a transparent fashion.

* **Singletons**: decorate your class with :python:`@injectable(singleton=True)` and only a
  single instance will be initialized and shared for injection.

* **Namespaces**: specify different namespaces for injectables as in
  :python:`@injectable(namespace="foo")` and then just use them when annotating your
  parameters as in :python:`dep: Annotated[..., Autowired(namespace="foo")]`.

* **Linters friendly**: :python:`Autowired` is carefully designed to comply with static linter
  analysis such as PyCharm's to preserve the parameter original type hint.

These are just a few cool and carefully built features for you. Check out our `docs
<https://injectable.readthedocs.io/en/latest/>`_!
