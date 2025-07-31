# Bookcart API Automated Tests

This repository contains automated API tests for the Bookcart application.  
You can find the live application [here](https://bookcart.azurewebsites.net/) and the API documentation [here](https://bookcart.azurewebsites.net/swagger/index.html).

---

## Getting Started

Follow these steps to set up and run the tests locally.

### Prerequisites

- Python 3.8 or higher installed
- Git installed
- Internet connection to access the API

### Setup

1. Clone the repository:

```bash
git clone https://github.com/farisbeqa/bookcart-api-tests.git
cd bookcart-api-tests

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

pytest tests/ -v

pytest tests/test_wishlist_api.py -v
