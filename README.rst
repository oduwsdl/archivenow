Archive Now (archivenow)
=============================
A Tool To Push Web Resources Into Web Archives
----------------------------------------------

Archive Now (**archivenow**) currently is configured to push resources into four public web archives. You can easily add more archives by writing a new archive handler (e.g., myarchive_handler.py) and place it inside the folder "handlers". 

Update January 2021
~~~~~~~~~
Originally, **archivenow** was configured to push to 6 different public web archives. The two removed web archives are `WebCite <https://www.webcitation.org/>`_ and `archive.st <http://archive.st/>`_. WebCite was removed from **archivenow** as they are no longer accepting archiving requests. Archive.st was removed from **archivenow** due to encountering a Captcha when attempting to push to the archive. In addition to removing those 2 archives, the method for pushing to `archive.today <https://archive.vn/>`_ and `megalodon.jp <https://megalodon.jp/>`_ from **archivenow** has been updated. In order to push to `archive.today <https://archive.vn/>`_ and `megalodon.jp <https://megalodon.jp/>`_, `Selenium <https://selenium-python.readthedocs.io/>`_ is used.

As explained below, this library can be used through:

- Command Line Interface (CLI)

- A Web Service

- A Docker Container

- Python


Installing
----------
The latest release of **archivenow** can be installed using pip:

.. code-block:: bash

      $ pip install archivenow

The latest development version containing changes not yet released can be installed from source:

.. code-block:: bash
      
      $ git clone git@github.com:oduwsdl/archivenow.git
      $ cd archivenow
      $ pip install -r requirements.txt
      $ pip install ./
      
In order to push to `archive.today <https://archive.vn/>`_ and `megalodon.jp <https://megalodon.jp/>`_, **archivenow** must use `Selenium <https://selenium-python.readthedocs.io/>`_, which has already been added to the requirements.txt. However, Selenium additionally needs a driver to interface with the chosen browser. It is recommended to use Selenium and **archivenow** with `Firefox <https://www.mozilla.org/en-US/firefox/releases/>`_ and Firefox's corresponding `GeckoDriver <https://github.com/mozilla/geckodriver/releases>`_.

You can download the latest versions of `Firefox <https://www.mozilla.org/en-US/firefox/releases/>`_ and the `GeckoDriver <https://github.com/mozilla/geckodriver/releases>`_ to use with **archivenow**.

After installing the driver, you can push to `archive.today <https://archive.vn/>`_ and `megalodon.jp <https://megalodon.jp/>`_ from **archivenow**.

CLI USAGE 
---------
Usage of sub-commands in **archivenow** can be accessed through providing the `-h` or `--help` flag, like any of the below.

.. code-block:: bash

      $ archivenow -h
      usage: archivenow.py [-h] [--mg] [--cc] [--cc_api_key [CC_API_KEY]]
                           [--is] [--ia] [--warc [WARC]] [-v] [--all]
                           [--server] [--host [HOST]] [--agent [AGENT]]
                           [--port [PORT]]
                           [URI]

      positional arguments:
        URI                   URI of a web resource

      optional arguments:
        -h, --help            show this help message and exit
        --mg                  Use Megalodon.jp
        --cc                  Use The Perma.cc Archive
        --cc_api_key [CC_API_KEY]
                              An API KEY is required by The Perma.cc Archive
        --is                  Use The Archive.is
        --ia                  Use The Internet Archive
        --warc [WARC]         Generate WARC file
        -v, --version         Report the version of archivenow
        --all                 Use all possible archives
        --server              Run archiveNow as a Web Service
        --host [HOST]         A server address
        --agent [AGENT]       Use "wget" or "squidwarc" for WARC generation
        --port [PORT]         A port number to run a Web Service

Examples
--------


Example 1
~~~~~~~~~

To save the web page (www.foxnews.com) in the Internet Archive:

.. code-block:: bash

      $ archivenow --ia www.foxnews.com
      https://web.archive.org/web/20170209135625/http://www.foxnews.com

Example 2
~~~~~~~~~

By default, the web page (e.g., www.foxnews.com) will be saved in the Internet Archive if no optional arguments are provided:

.. code-block:: bash

      $ archivenow www.foxnews.com
      https://web.archive.org/web/20170215164835/http://www.foxnews.com

Example 3
~~~~~~~~~

To save the web page (www.foxnews.com) in the Internet Archive (archive.org) and Archive.is:

.. code-block:: bash
      
      $ archivenow --ia --is www.foxnews.com
      https://web.archive.org/web/20170209140345/http://www.foxnews.com
      http://archive.is/fPVyc


Example 4
~~~~~~~~~

To save the web page (https://nypost.com/) in all configured web archives. In addition to preserving the page in all configured archives, this command will also locally create a WARC file:

.. code-block:: bash
      
      $ archivenow --all https://nypost.com/ --cc_api_key $Your-Perma-CC-API-Key
      http://archive.is/dcnan
      https://perma.cc/53CC-5ST8
      https://web.archive.org/web/20181002081445/https://nypost.com/
      https://megalodon.jp/2018-1002-1714-24/https://nypost.com:443/
      https_nypost.com__96ec2300.warc

Example 5
~~~~~~~~~

To download the web page (https://nypost.com/) and create a WARC file:

.. code-block:: bash
      
      $ archivenow --warc=mypage --agent=wget https://nypost.com/
      mypage.warc
      
Server
------

You can run **archivenow** as a web service. You can specify the server address and/or the port number (e.g., --host localhost  --port 12345)

.. code-block:: bash
      
      $ archivenow --server
      
      Running on http://0.0.0.0:12345/ (Press CTRL+C to quit)


Example 6
~~~~~~~~~

To save the web page (www.foxnews.com) in The Internet Archive through the web service:

.. code-block:: bash

      $ curl -i http://0.0.0.0:12345/ia/www.foxnews.com
      
          HTTP/1.0 200 OK
          Content-Type: application/json
          Content-Length: 95
          Server: Werkzeug/0.11.15 Python/2.7.10
          Date: Tue, 02 Oct 2018 08:20:18 GMT

          {
            "results": [
              "https://web.archive.org/web/20181002082007/http://www.foxnews.com"
            ]
          }
      
Example 7
~~~~~~~~~

To save the web page (www.foxnews.com) in all configured archives though the web service:

.. code-block:: bash
      
      $ curl -i http://0.0.0.0:12345/all/www.foxnews.com

          HTTP/1.0 200 OK
          Content-Type: application/json
          Content-Length: 385
          Server: Werkzeug/0.11.15 Python/2.7.10
          Date: Tue, 02 Oct 2018 08:23:53 GMT

          {
            "results": [
              "Error (The Perma.cc Archive): An API Key is required ", 
              "http://archive.is/ukads", 
              "https://web.archive.org/web/20181002082007/http://www.foxnews.com", 
              "Error (Megalodon.jp): We can not obtain this page because the time limit has been reached or for technical ... ", 
              "http://www.webcitation.org/72rbKsX8B"
            ]
          }

Example 8
~~~~~~~~~

Because an API Key is required by Perma.cc, the HTTP request should be as follows:
        
.. code-block:: bash
      
      $ curl -i http://127.0.0.1:12345/all/https://nypost.com/?cc_api_key=$Your-Perma-CC-API-Key

Or use only Perma.cc:

.. code-block:: bash

      $ curl -i http://127.0.0.1:12345/cc/https://nypost.com/?cc_api_key=$Your-Perma-CC-API-Key

Running as a Docker Container
-----------------------------

.. code-block:: bash

    $ docker image pull oduwsdl/archivenow

Different ways to run archivenow    

.. code-block:: bash

    $ docker container run -it --rm oduwsdl/archivenow -h

Accessible at 127.0.0.1:12345:

.. code-block:: bash

    $ docker container run -p 12345:12345 -it --rm oduwsdl/archivenow --server --host 0.0.0.0

Accessible at 127.0.0.1:22222:

.. code-block:: bash

    $ docker container run -p 22222:11111 -it --rm oduwsdl/archivenow --server --port 11111 --host 0.0.0.0

.. image:: http://www.cs.odu.edu/~maturban/archivenow-6-archives.gif
   :width: 10pt


To save the web page (http://www.cnn.com) in The Internet Archive

.. code-block:: bash

    $ docker container run -it --rm oduwsdl/archivenow --ia http://www.cnn.com
    

Python Usage
------------

.. code-block:: bash
   
    >>> from archivenow import archivenow

Example 9
~~~~~~~~~~

To save the web page (www.foxnews.com) in all configured archives:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","all")
      ['https://web.archive.org/web/20170209145930/http://www.foxnews.com','http://archive.is/oAjuM','http://www.webcitation.org/6o9LcQoVV','Error (The Perma.cc Archive): An API KEY is required]

Example 10
~~~~~~~~~~

To save the web page (www.foxnews.com) in The Perma.cc:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","cc",{"cc_api_key":"$YOUR-Perma-cc-API-KEY"})
      ['https://perma.cc/8YYC-C7RM']
      
Example 11
~~~~~~~~~~

To start the server from Python do the following. The server/port number can be passed (e.g, start(port=1111, host='localhost')):

.. code-block:: bash

      >>> archivenow.start()
      
          2017-02-09 15:02:37
          Running on http://127.0.0.1:12345
          (Press CTRL+C to quit)


Configuring a new archive or removing existing one
--------------------------------------------------
Additional archives may be added by creating a handler file in the "handlers" directory.

For example, if I want to add a new archive named "My Archive", I would create a file "ma_handler.py" and store it in the folder "handlers". The "ma" will be the archive identifier, so to push a web page (e.g., www.cnn.com) to this archive through the Python code, I should write:


.. code-block:: python

      archivenow.push("www.cnn.com","ma")
      

In the file "ma_handler.py", the name of the class must be "MA_handler". This class must have at least one function called "push" which has one argument. See the existing `handler files`_ for examples on how to organized a newly configured archive handler.

Removing an archive can be done by one of the following options:

- Removing the archive handler file from the folder "handlers"

- Renaming the archive handler file to other name that does not end with "_handler.py"

- Setting the variable "enabled" to "False" inside the handler file


Notes
-----
The Internet Archive (IA) sets a time gap of at least two minutes between creating different copies of the "same" resource. 

For example, if you send a request to IA to capture (www.cnn.com) at 10:00pm, IA will create a new copy (*C*) of this URI. IA will then return *C* for all requests to the archive for this URI received until 10:02pm. Using this same submission procedure for Archive.is requires a time gap of five minutes.  

.. _handler files: https://github.com/oduwsdl/archivenow/tree/master/archivenow/handlers


Citing Project
--------------

.. code-block:: latex

      @INPROCEEDINGS{archivenow-jcdl2018,
        AUTHOR    = {Mohamed Aturban and
                     Mat Kelly and
                     Sawood Alam and
                     John A. Berlin and
                     Michael L. Nelson and
                     Michele C. Weigle},
        TITLE     = {{ArchiveNow}: Simplified, Extensible, Multi-Archive Preservation},
        BOOKTITLE = {Proceedings of the 18th {ACM/IEEE-CS} Joint Conference on Digital Libraries},
        SERIES    = {{JCDL} '18},
        PAGES     = {321--322},
        MONTH     = {June},
        YEAR      = {2018},
        ADDRESS   = {Fort Worth, Texas, USA},
        URL       = {https://doi.org/10.1145/3197026.3203880},
        DOI       = {10.1145/3197026.3203880}
      }
