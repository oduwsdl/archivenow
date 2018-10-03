Archive Now (archivenow)
=============================
A Tool To Push Web Resources Into Web Archives
----------------------------------------------

Archive Now (**archivenow**) currently is configured to push resources into six public web archives. You can easily add more archives by writing a new archive handler (e.g., myarchive_handler.py) and place it inside the folder "handlers".

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

CLI USAGE
---------
Usage of sub-commands in **archivenow** can be accessed through providing the `-h` or `--help` flag, like any of the below.

.. code-block:: bash

      $ archivenow -h
      usage: archivenow.py [-h] [--mg] [--wc] [--cc] [--cc_api_key [CC_API_KEY]]
                           [--is] [--st] [--ia] [--warc [WARC]] [-v] [--all]
                           [--server] [--host [HOST]] [--agent [AGENT]]
                           [--port [PORT]]
                           [URI]

      positional arguments:
        URI                   URI of a web resource

      optional arguments:
        -h, --help            show this help message and exit
        --mg                  Use Megalodon.jp
        --wc                  Use The WebCite Archive
        --cc                  Use The Perma.cc Archive
        --cc_api_key [CC_API_KEY]
                              An API KEY is required by The Perma.cc Archive
        --is                  Use The Archive.is
        --st                  Use The Archive.st
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
      http://www.webcitation.org/72ramyxT2
      https://Archive.st/archive/2018/10/nypost.com/h5m1/nypost.com/index.html
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
              "http://Archive.st/ikxq", 
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
~~~~~~~~~

To save the web page (www.foxnews.com) in The WebCite Archive:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","wc")
      ['http://www.webcitation.org/6o9LTiDz3']

Example 10
~~~~~~~~~

To save the web page (www.foxnews.com) in all configured archives:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","all")
      ['https://web.archive.org/web/20170209145930/http://www.foxnews.com','http://archive.is/oAjuM','http://www.webcitation.org/6o9LcQoVV','Error (The Perma.cc Archive): An API KEY is required]

Example 11
~~~~~~~~~~

To save the web page (www.foxnews.com) in The Perma.cc:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","cc",{"cc_api_key":"$YOUR-Perma-cc-API-KEY"})
      ['https://perma.cc/8YYC-C7RM']
      
Example 12
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
