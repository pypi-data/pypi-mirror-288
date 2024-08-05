# Locksys

Locksys is a Python library by Lifsys, Inc. for securely retrieving API keys from 1Password vaults using the 1Password Connect SDK.

## Installation

You can install Locksys using pip:

```
pip install locksys
```

## Usage

Here's a quick example of how to use Locksys:

```python
from locksys import Locksys

# Initialize Locksys with a vault name (default is "API")
lock = Locksys("MyVault")

# Retrieve an API key
api_key = lock.item("MyItem").key("API_KEY").results()

print(f"Retrieved API key: {api_key}")
```

## Features

- Secure retrieval of API keys from 1Password vaults
- Caching of 1Password client for improved performance
- Simple and intuitive API

## Requirements

- Python 3.6+
- 1Password Connect SDK

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.
