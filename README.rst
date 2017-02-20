Archive Now (archivenow)
=============================
A Tool To Push Web Resources Into Web Archives
----------------------------------------------

Archive Now (**archivenow**) currently is configured to push resources into four public web archives. You can easily add more archives by writing a new archive handler (e.g., ia_handler.py) and place it inside the folder "handlers".

As explained below, this library can be used through:

- CLI

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
      
      $ git clone git@github.com:maturban/archivenow.git
      $ cd archivenow
      $ pip install -r requirements.txt
      $ pip install ./

CLI USAGE
---------
Usage of sub-commands in **archivenow** can be accessed through providing the `-h` or `--help` flag, like any of the below.

.. code-block:: bash

      $ archivenow -h
      usage: archivenow.py [-h] [--cc] [--cc_api_key [CC_API_KEY]] [--ia] [--is]
                     [--wc] [-v] [--all] [--server] [--host [HOST]]
                     [--port [PORT]]
                     [URI]

      positional arguments:
        URI                   URI of a web resource

      optional arguments:
        -h, --help            show this help message and exit
        --cc                  Use The Perma.cc Archive
        --cc_api_key [CC_API_KEY]
                              An API KEY is required by The Perma.cc Archive
        --ia                  Use The Internet Archive
        --is                  Use The Archive Today
        --wc                  Use The WebCite Archive
        -v, --version         Report the version of archivenow
        --all                 Use all possible archives
        --server              Run archiveNow as a Web Service
        --host [HOST]         A server address
        --port [PORT]         A port number to run a Web Service
  
Examples
--------

- **Example 1**

To save the web page (www.foxnews.com) in the Internet Archive:

.. code-block:: bash

      $ archivenow --ia www.foxnews.com
      ['https://web.archive.org/web/20170209135625/http://www.foxnews.com']

- **Example 2**

By default, the web page (e.g., www.foxnews.com) will be saved in the Internet Archive if no optional arguments provided:

.. code-block:: bash

      $ archivenow www.foxnews.com
      ['https://web.archive.org/web/20170215164835/http://www.foxnews.com']

- **Example 3**

To save the web page (www.foxnews.com) in the Internet Archive (archive.org) and The Archive Today (archive.is):

.. code-block:: bash
      
      $ archivenow --ia --is www.foxnews.com
      ['https://web.archive.org/web/20170209140345/http://www.foxnews.com', 'http://archive.is/fPVyc']


- **Example 4**

To save the web page (www.foxnews.com) in all configured web archives:

.. code-block:: bash
      
      $ archivenow.py --all www.foxnews.com --cc_api_key $YOUR-Perma-cc-API-KEY
      ['https://perma.cc/8YYC-C7RM','https://web.archive.org/web/20170220074919/http://www.foxnews.com','http://archive.is/jy8B0','http://www.webcitation.org/6o9IKD9FP']

Server
------

You can run **archivenow** as a web service. You can specify the server address and/or the port number (e.g., --host localhost  --port 11111)

.. code-block:: bash
      
      $ archivenow --server
 
         2017-02-09 14:20:33
         Running on http://0.0.0.0:12345
         (Press CTRL+C to quit) 

- **Example 5**

To save the web page (www.foxnews.com) in The Internet Archive through the web service:

.. code-block:: bash
      
      $ curl -i http://0.0.0.0:12345/ia/www.foxnews.com
      
           HTTP/1.0 200 OK
           Content-Type: application/json
           Content-Length: 95
           Server: Werkzeug/0.11.15 Python/2.7.10
           Date: Thu, 09 Feb 2017 14:29:23 GMT

          {
            "results": [
              "https://web.archive.org/web/20170209142922/http://www.foxnews.com"
            ]
          }
      
- **Example 6**

To save the web page (www.foxnews.com) in all configured archives though the web service:

.. code-block:: bash
      
      $ curl -i http://0.0.0.0:12345/all/www.foxnews.com

          HTTP/1.0 200 OK
          Content-Type: application/json
          Content-Length: 172
          Server: Werkzeug/0.11.15 Python/2.7.10
          Date: Thu, 09 Feb 2017 14:33:47 GMT

          {
            "results": [
              "https://web.archive.org/web/20170209143327/http://www.foxnews.com", 
              "http://archive.is/H2Yfg", 
              "http://www.webcitation.org/6o9Jubykh",
              "Error (The Perma.cc Archive): An API KEY is required"
            ]
          }   

- **Example 7**

Because an API Key is required by Perma.cc, the HTTP request should be as following:
        
.. code-block:: bash
      
      $ curl -i http://0.0.0.0:12345/all/www.foxnews.com?cc_api_key=$YOUR-Perma-cc-API-KEY

Or use only the Perma.cc:

.. code-block:: bash

      $ curl -i http://0.0.0.0:12345/cc/www.foxnews.com?cc_api_key=$YOUR-Perma-cc-API-KEY

Running as a Docker Container
-----------------------------

.. code-block:: bash

    $ docker pull maturban/archivenow

Different ways to run archivenow    

.. code-block:: bash

    $ docker run -it --rm maturban/archivenow -h
    $ docker run -p 80:12345 -it --rm maturban/archivenow --server
    $ docker run -p 80:11111 -it --rm maturban/archivenow --server --port 11111
    $ docker run -it --rm maturban/archivenow --ia http://www.cnn.com
    

Python Usage
------------

.. code-block:: bash
   
    >>> from archivenow import archivenow
    
- **Example 8**

To save the web page (www.foxnews.com) in The WebCite Archive:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","wc")
      ['http://www.webcitation.org/6o9LTiDz3']

- **Example 9**

To save the web page (www.foxnews.com) in all configured archives:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","all")
      ['https://web.archive.org/web/20170209145930/http://www.foxnews.com','http://archive.is/oAjuM','http://www.webcitation.org/6o9LcQoVV','Error (The Perma.cc Archive): An API KEY is required]

- **Example 10**

To save the web page (www.foxnews.com) in The Perma.cc:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","cc","cc_api_key=$YOUR-Perma-cc-API-KEY")
      ['https://perma.cc/8YYC-C7RM']
      
- **Example 11**

To start the server from Python do the following. The server/port number can be passed (e.g, start(port=1111, host='localhost')):

.. code-block:: bash

      >>> archivenow.start()
      
          2017-02-09 15:02:37
          Running on http://0.0.0.0:12345
          (Press CTRL+C to quit)


Configuring a new archive or removing existing one
--------------------------------------------------
Adding a new archive is as simple as adding a handler file in the folder "handlers". For example, if I want to add a new archive named "My Archive", I would create a file "ma_handler.py" and store it in the folder "handlers". The "ma" will be the archive identifier, so to push a web page (e.g., www.cnn.com) to this archive through the Python code, I should write ">>>archivenow.push("www.cnn.com","ma")". In the file "ma_handler.py", the name of the class must be "MA_handler". This class must have at least one function called "push" which has one argument. It might be helpful to see how other "\*_handler.py" organized.

Removing an archive can be done by one of the following options:

- Removing the archive handler file from the folder "handlers"

- Rename the archive handler file to other name that does not end with "_handler.py"

- Simply, inside the handler file, set the variable "enabled" to "False"


Notes
-----
The Internet Archive (IA) sets a time gap of at least two minutes between creating different copies of the 'same' resource. For example, if you send a request to the IA to capture (www.cnn.com) at 10:00pm. The IA will create a new copy (lets call it C1) of this CNN homepage. The IA will return (C1) for all requests to archive the CNN homepage recived before 10:02pm. The Archive Today sets this time gap to five minutes.  
