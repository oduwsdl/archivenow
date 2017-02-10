Archive Now (archivenow)
=============================
A Tool To Push Web Resources Into Web Archives
----------------------------------------------

Archive Now (**archivenow**) currently is configured to push resources into three public web archives. You can easily add more archives by writing a new archive handler (e.g., ia_handler.py) and place it inside the folder "handlers".

As explained below, this library can be used through:

- CLI

- Web Service

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
      usage: archivenow [-h] [--ia] [--is] [--wc] [--all] [--server]
                     [--host [HOST]] [--port [PORT]]
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
        --host [HOST]  The server address
        --port [PORT]  The port number to run a Web Service
  
Examples
--------

- **Example 1**

To save the web page (www.foxnews.com) in the Internet Archive:

.. code-block:: bash

      $ archivenow --ia www.foxnews.com
      ['https://web.archive.org/web/20170209135625/http://www.foxnews.com']


- **Example 2**

To save the web page (www.foxnews.com) in the Internet Archive (archive.org) and The Archive Today (archive.is):

.. code-block:: bash
      
      $ archivenow --ia --is www.foxnews.com
      ['https://web.archive.org/web/20170209140345/http://www.foxnews.com', 'http://archive.is/fPVyc']


- **Example 3**

To save the web page (www.foxnews.com) in all configured web archives:

.. code-block:: bash
      
      $ archivenow --all www.foxnews.com
      ['https://web.archive.org/web/20170209140913/http://www.foxnews.com','http://archive.is/w6coU','http://www.webcitation.org/6o9IKD9FP']


Server
------

You can run **archivenow** as a web service. You can specify the server address and/or the port number (e.g., --host localhost  --port 11111)

.. code-block:: bash
      
      $ archivenow --server
 
         2017-02-09 14:20:33
         Running on http://0.0.0.0:12345
         (Press CTRL+C to quit) 

- **Example 4**

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
      
- **Example 5**

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
              "http://www.webcitation.org/6o9Jubykh"
            ]
          }    
      
Python Usage
------------

.. code-block:: bash
   
    >>> from archivenow import archivenow
    
- **Example 6**

To save the web page (www.foxnews.com) in The WebCite Archive:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","wc")
      ['http://www.webcitation.org/6o9LTiDz3']

- **Example 7**

To save the web page (www.foxnews.com) in all configured archives:

.. code-block:: bash

      >>> archivenow.push("www.foxnews.com","all")
      ['https://web.archive.org/web/20170209145930/http://www.foxnews.com','http://archive.is/oAjuM','http://www.webcitation.org/6o9LcQoVV']
      
- **Example 8**

To start the server from Python do the following. The server/port number can be passed (e.g, start(1111, 'localhost')):

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
The Internet Archive (IA) sets a time gap of al least two minutes between creating different copies of the 'same' resource. For example, if you send a request to the IA to capture (www.cnn.com) at 10:00pm. The IA will create a new copy (lets call it C1) of this CNN homepage. The IA will return (C1) for all requests to archive the CNN homepage recived before 10:02pm. The Archive Today sets this time gap to five minutes.  
