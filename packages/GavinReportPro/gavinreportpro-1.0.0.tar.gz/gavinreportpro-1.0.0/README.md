![](https://img.shields.io/badge/Version-1.0.0-green.svg)
![](https://img.shields.io/badge/License-MIT-orange.svg)
![](https://img.shields.io/badge/Python-3-green.svg)

# Introduction
```text
Modified based on unittestreport
Added automatic screenshot and picture display for assertion failure
Added the lark Robot api
```

# Install
```text
pip install TheRuffianReportPro
```

# Author
```text
name:TheRuffian
email:bugpz2779@gmail.com
email:theruffian@163.com
```

# Instructions for use
### Case

```python
import unittest
from selenium import webdriver
from GavinReportPro.common import failure_monitor


class Test_demo(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome()
        self.failureException = failure_monitor(self, 'images')
        self.driver.get("url")

    def test_example(self):
        self.driver.find_element(By, Element).send_keys(keyword)
        self.driver.find_element(By, Element).click()
        self.assertEqual(first, second)  # Take a screenshot if the first assertion fails 

```
### Run

```python
import unittest
from GavinReportPro.core.testRunner import TestRunner
from case.xxx import Test_demo

runner = TestRunner(unittest.TestLoader().loadTestsFromTestCase(Test_demo),
                    filename='report.html',
                    report_dir='./Report',
                    templates=3)
runner.run()
```