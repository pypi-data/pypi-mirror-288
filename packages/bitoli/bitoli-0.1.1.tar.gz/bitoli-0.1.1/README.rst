bitoli
======

bitoli is a Python package for adaptive compression and encryption of data. It offers simple methods to securely encode and decode data using AES encryption in CFB mode and adaptive compression techniques.

Features
--------

- Adaptive compression using zlib
- AES encryption with CFB mode
- Base85 encoding for non-compressed data
- Simple API for encoding and decoding data

Installation
------------

You can install bitoli using pip:

.. code:: bash

    pip install bitoli

Usage
-----

Here is a simple example of how to use bitoli:

.. code:: python

    from bitoli import encode, decode

    key = "your_password"
    data = "This is some data to encrypt and compress."

    # Encode data
    encoded_data = encode(data, key)
    print("Encoded data:", encoded_data)

    # Decode data
    decoded_data = decode(encoded_data, key)
    print("Decoded data:", decoded_data)

API
---

- `encode(data, key)`: Encrypts and compresses the data using the provided key.
- `decode(data, key)`: Decompresses and decrypts the data using the provided key.

License
-------

This project is licensed under the MIT License.
