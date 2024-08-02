# pysqlcipher3static

This is a fork of [pysqlcipher3](https://github.com/rigglemania/pysqlcipher3) that includes statically
linked binary wheel distributions to make it easier to install.

Install with:
```bash
pip install pysqlcipher3static
```

**Note: this project is no longer being actively maintained. Security vulnerabilities may exist in this code. Use at your own risk.**

This library is a fork of pysqlcipher targeted for use with Python 3.
It is still in the beta state, although this library contains minimal
new code and instead heavily pulls from the core Python sqlite source
code while linking against libsqlcipher.

- Small modifications for static build (c) 2024 Chris Arderne
- Python 3 packaging for SQLCipher (c) 2015 David Riggleman
- Packaging for SQLCipher (c) 2013-2014 Kali Kaneko
- Original code (c) 2004-2007 Gerhard Häring

## Usage
You have to pass the ``PRAGMA key`` before doing any operations::

```python
from pysqlcipher3 import dbapi2 as sqlite
conn = sqlite.connect('test.db')
c = conn.cursor()
c.execute("PRAGMA key='password'")
c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
conn.commit()
c.close()
```

## Windows build
Follow the same instructions as above except for the following:
1. Make sure that you are using OpenSSL-Win64
2. Set the PATH to the Win64 environment
3. Copy the OpenSSL folder
4. Build the amalgamation and install with the latest Python x64

## SQLCipher compatibility issues
The encryption has default compatibility with the SQLCipher version installed on your machine.
You have to execute ``PRAGMA cipher_compatibility = 3`` before doing any operations on a database encrypted with SQLCipher version 3 when a newer version is installed.
Keep in mind, you have to add ``PRAGMA cipher_compatibility`` after ``PRAGMA key``::

```python
from pysqlcipher3 import dbapi2 as sqlite
conn = sqlite.connect('test.db')
c = conn.cursor()
c.execute("PRAGMA key='password'")
c.execute("PRAGMA cipher_compatibility = 3")
c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
conn.commit()
c.close()
```
