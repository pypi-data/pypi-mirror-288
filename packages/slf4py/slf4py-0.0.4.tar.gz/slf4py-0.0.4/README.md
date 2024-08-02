# slf4py
Simple Logging Facade for Python.

## How to use
```bash
# at Terminal

$ pip install slf4py
```

```python
# at example.py

from slf4py import set_logger


@set_logger
class Example:
    def hi(self):
        self.log.info("Hello World")

        
e = Example()
e.hi()
# [INFO] [2024-06-04 23:50:41,355] [example.py:9] Hello World


from slf4py import create_logger


def main():
    logger = create_logger()
    logger.info("Hello World")


main()
# [INFO] [2024-06-04 23:50:41,355] [example.py:21] Hello World
```