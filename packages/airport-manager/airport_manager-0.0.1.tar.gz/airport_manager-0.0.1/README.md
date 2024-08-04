# PyPI Publisher Template

This repository is a template for publishing Python packages to PyPI and TestPyPI using GitHub Actions and shell scripts.

## Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/yourusername/pypi-publisher-template.git
   cd pypi-publisher-template
   ```

2. **Run the setup script**:

   ```sh
   ./setup.sh
   ```

3. **Update your .env file** with your PyPI and TestPyPI tokens:

   ```env
   TEST_PYPI_API_TOKEN=your_test_pypi_token_here
   PYPI_API_TOKEN=your_pypi_token_here

   BASE_URL=your_base_url_here
   ```

## Publishing

### To TestPyPI

Run the following command to publish to TestPyPI:

```sh
./publish_test.sh
```

### To PyPI

Run the following command to publish to PyPI:

```sh
./publish_pypi.sh
```

## Workflow

The GitHub Actions workflow is configured to publish to PyPI on tag creation and push to the main branch. Make sure to configure your repository secrets with the required tokens.

## License

This project is licensed under the MIT License.
