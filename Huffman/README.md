# Huffman coding

> A Huffman code is a particular type of optimal prefix code that is commonly used for lossless data compression.
>
> [Wikipedia - Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)

## Requirements

You'll have to install some requirements in order to get the Huffman coding implementation working. Just do:

```bash
pip install -r requirements.txt
```

Or, in order to works with python3:

```bash
pip3 install -r requirements.txt
```

## Tests

**pytest** is present in `requirements.txt`, so it should now be installed in your system. To launch the tests:

```bash
pytest
```

The command `pytest` will find the files begining with `test_` and test all methods, in those files, begining with `test_`.

## Limitations

The first 6 bytes of a compressed file contains the size of the the uncompressed data. So this implementation can not compress a file larger than 32 to.