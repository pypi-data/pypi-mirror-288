# jsonyx

[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)

**jsonyx** is a robust [JSON](http://json.org) encoder and decoder for Python
3.10+. It is written in pure Python with an optional C extension for better
performance and no dependencies

Key Features:

- Dedicated functions for reading and writing files
- Detailed error messages:
    ```none
      File "C:\Users\wanne\Downloads\broken.json", line 2, column 15-19
         "path": "c:\users"
                      ^^^^
    jsonyx._decoder.JSONSyntaxError: Expecting 4 hex digits
    ```
- Optionally supports these JSON deviations:
    ```json
    {
        /* Block */ // and line comments
        "Decimal numbers": [1.0000000000000001, 1e400],
        "Duplicate keys": {"key": "value 1", "key": "value 2"},
        "Missing comma's": [1 2 3],
        "NaN and infinity": [NaN, Infinity, -Infinity],
        "Trailing comma": [0,],
        "Surrogates": "\ud800"
    }
    ```

The latest documentation for jsonyx is available online at:
https://jsonyx.readthedocs.io/en/stable/usage.html
