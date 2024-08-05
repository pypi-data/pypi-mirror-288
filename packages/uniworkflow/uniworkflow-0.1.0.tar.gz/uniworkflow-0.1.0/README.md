# UniWorkflow

UniWorkflow is a Python library that provides a unified interface for integrating with various workflow providers such as Make.com, Dify, and Zapier.

## Installation

You can install UniWorkflow using pip:

```
pip install uniworkflow
```

## Quick Start

Here's a simple example of how to use UniWorkflow:

```python
from uniworkflow import UniwWorkflow
from uniworkflow.providers import MakeProvider

# Initialize the UniwWorkflow
uw = UniwWorkflow()

# Add a provider
make_provider = MakeProvider(api_key="your_api_key")
uw.add_provider("make", make_provider)

# Execute a workflow
result = uw.execute_workflow("make", "workflow_id", data={"key": "value"})
print(result)
```

## Documentation

For more detailed information, please refer to our [documentation](docs/index.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

3. `LICENSE` (MIT License as an example)

```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
