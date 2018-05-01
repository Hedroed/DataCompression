# LZW

> Lempel–Ziv–Welch (LZW) is a universal lossless data compression algorithm. The algorithm is simple to implement and has the potential for very high throughput in hardware implementations. It is the algorithm of the widely used Unix file compression utility compress and is used in the GIF image format.
>
> [Wikipedia - Lempel–Ziv–Welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch)

## Requirements

You'll have to install some requirements in order to get the LZW implementation working. Just do:

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