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

.. code-block:: bash
      
      $ on_demand www.foxnews.com --ia 

The output

.. code-block:: bash
      
      https://web.archive.org/web/20170202064016/http://www.foxnews.com







This will save the web page (www.foxnews.com) in the Internet Archive. The link to the archived version is (https://web.archive.org/web/20170202064016/http://www.foxnews.com).

### Example 2
```bash
%python on_demand.py www.foxnews.com --archive_is
```
###### The output
```
http://archive.is/Z7eVp
```
This will save the web page (www.foxnews.com) in the Archive Today. The link to the archived version is (http://archive.is/hxpuZ).

### Example 3
```bash
%python on_demand.py www.foxnews.com --webcite
```
###### The output
```
http://www.webcitation.org/6nyAzDqC1
```
This will save the web page (www.foxnews.com) in the WebCite archive. The link to the archived version is (http://www.webcitation.org/6nyAzDqC1).

### Example 4
```bash
%python on_demand.py www.foxnews.com --webcite --ia
```
###### The output
```
https://web.archive.org/web/20170202064527/http://www.foxnews.com
http://www.webcitation.org/6nyB5z4Iz
```
This will save the web page (www.foxnews.com) in both the WebCite archive and the Archive Today. The links to the archived versions are (http://www.webcitation.org/6nyB5z4Iz) and (https://web.archive.org/web/20170202064527/http://www.foxnews.com).


### Example 5
```bash
%python on_demand.py www.foxnews.com --all
```
###### The output
```
https://web.archive.org/web/20170202065542/http://www.foxnews.com
http://archive.is/c0vrF
http://www.webcitation.org/6nyBlk1Ri
```
This will save the web page (www.foxnews.com) in all archives listed in the file "archives.conf".

License
---------
MIT
