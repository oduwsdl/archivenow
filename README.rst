Archive Now (archivenow)
=============================
A Tool To Push Web Resources Into Web Archives
---------------------------------------

Archive Now (archivenow) currently is configured to push resources into three public web archives. You can easily add more archives by writing a new archive handler (e.g., ia_handler.py) and place it inside the folder "handlers".

Installing
----------
The latest release of archivenow can be installed using pip:

.. code-block:: bash

      $ pip install archivenow

The latest development version containing changes not yet released can be installed from source:

.. code-block:: bash
      
      $ git clone git@github.com:maturban/archivenow.git
      $ cd ipwb
      $ pip install -r requirements.txt
      $ pip install ./

USAGE
-------------
Usage of sub-commands in archivenow can be accessed through providing the `-h` or `--help` flag, like any of the below.

.. code-block:: bash


      $ archivenow -h
      usage: archivenow [-h] [--ia] [--is] [--wc] [--all] [--server]
                     [--port [PORT]]
                     [URI]

      positional arguments:
        URI            URI of a web resource

      optional arguments:
        -h, --help     show this help message and exit
        --ia           Use The Internet Archive
        --is           Use The Archive Today
        --wc           Use The WebCite Archive
        --all          Use all possible archives
        --server       Run archiveNow as a Web Service
        --port [PORT]  port number to run a Web Service
  
Examples
--------

Example 1
--------

To save the web page (www.foxnews.com) in the Internet Archive:

.. code-block:: bash
      
      $ archivenow --ia www.foxnews.com

*The output*

.. code-block:: bash
      
      ['https://web.archive.org/web/20170209135625/http://www.foxnews.com']


Example 2
--------

To save the web page (www.foxnews.com) in the Internet Archive (archive.org) and The Archive Today (archive.is):

.. code-block:: bash
      
      $ archivenow --ia --is www.foxnews.com
      
*The output*

.. code-block:: bash

      ['https://web.archive.org/web/20170209140345/http://www.foxnews.com', 'http://archive.is/fPVyc']


Example 3
--------

To save the web page (www.foxnews.com) in all configured web archives:

.. code-block:: bash
      
      $ archivenow --all www.foxnews.com
      
*The output*

.. code-block:: bash

      ['https://web.archive.org/web/20170209140913/http://www.foxnews.com', 'http://archive.is/w6coU','http://www.webcitation.org/6o9IKD9FP']


Server
--------

You can run archivenow as a web service ( you can specify the port number using "--port #")

.. code-block:: bash
      
      $ archivenow --server
      
*The output*

.. code-block:: bash

     2017-02-09 14:20:33
     Running on http://localhost:12345
     (Press CTRL+C to quit) 

License
---------
MIT
