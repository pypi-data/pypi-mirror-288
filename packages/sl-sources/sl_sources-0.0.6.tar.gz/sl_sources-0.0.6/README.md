# Society Library Sources

This repo contains the source document collectors for the Society Library.

## Use the package directly
```bash
# with pipx
pipx sl_sources search youtube "machine learning tutorial" --num_results 3 --output results.json

# other sources will require you to set your environment variables
# for local development, copy .env.template to .env
# for cli, export the variables directly
export GOOGLE_API_KEY=<your api key>
pip sl_sources search google_scholar "artificial intelligence" --num_results 5

export SEMANTIC_SCHOLAR_API_KEY=<your api key>
python -m sl_sources download semantic_scholar <paper id>
```

## Library
```bash
pip install sl_sources
from sl_sources import search_source, download_source

search_results = await search_source("google", "artificial intelligence")
# returns an array of sources:
# [{'url': 'https://www.openai.com', 'title': 'OpenAI', 'source': 'google'}]
for result in search_results:
    scrape_result = await download_source(result)
    print(scrape_result)

from sl_sources import search_google_scholar, download_from_google_scholar
search_results = await search_google_scholar("artificial intelligence")
# returns an array of sources:
# [{'url': 'https://www.arxiv.org/abs/2402.09974', 'title': 'A Survey of Deep Learning Techniques for Neuroscience', 'source': 'google_scholar'}]
for result in search_results:
    scrape_result = await download_from_google_scholar(result)
    # {'url': 'https://www.arxiv.org/abs/2402.09974', 'full_text': 'A Survey of Deep Learning Techniques for Neuroscience', 'source': 'google_scholar'}
    print(scrape_result)
```

## Captcha solver
This library uses the Capsolver API to solve captchas. Add your API key to .env to enable captcha solving.

```bash
CAPSOLVER_API_KEY=CAP-<your api key here>
```

## Worker
The Media Worker wraps the search and download functions for all sources, and is especially useful for offloading work from the main application. If you are attempting a large simultaneous work load, it is strongly advised that you use a worker.

### Setup
You will need to make a Google account, enable "Google Cloud Functions" and "Google Cloud Build". However, if you initialize gcloud with your Google account and log in, these can be enabled for you automatically when the worker is deployed.

Download and install the gcloud cli
```
brew install --cask google-cloud-sdk # mac

# Linux
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
```

Then initialize gcloud and authenticate:
```
gcloud init
gcloud auth login
```

### Local development
You can run the worker locally using functions-framework
```bash
pip install functions-framework
functions-framework --target handle_request --debug
```

Make sure you have set `CLOUD_FUNCTION_URL=http://127.0.0.1:8080` and `CLOUD_FUNCTION_ENABLED=true` in your .env file.

You can now call the function using curl
```bash
# search
curl -X POST http://127.0.0.1:8080 -H "Content-Type: application/json" -d '{"source_type": "google", "query": "artificial intelligence in neuroscience", "request_type": "search", "num_results": 10}'

# download
curl -X POST http://127.0.0.1:8080 -H "Content-Type: application/json" -d '{"search_result": {"url": "https://www.google.com", "title": "Google", "source_type": "google"}, "request_type": "download"}'
# note that the search_result object is the result of the search function
```

### Deploy the worker
```bash
bash deploy_worker.sh
```

The worker will be deployed using the environment variables in the .env, so make sure those are what you want them to be.

You will need to update your .env and set `CLOUD_FUNCTION_ENABLED` to "true" and `CLOUD_FUNCTION_URL` to your deployed worker URL, which will be shown at deployment time. It should look like this:
```bash
CLOUD_FUNCTION_ENABLED=true
CLOUD_FUNCTION_URL=https://us-<region>-<project>.cloudfunctions.net/media_worker
```

You can initialize and run many workers simultaneously. The one limitation is that cloud functions can run for a maximum of 9 minutes (540 seconds) so make sure that your work is split into smaller chunks than would require that much processing time.

### Testing worker locally
You can test the worker using functions_framework
```bash
pip install functions-framework
functions_framework --target handle_request --debug
```

## PyPI

You can update the library with the following commands:
```
# rmrf the dist folder if it exists
rm -rf dist

# build the library
python setup.py sdist bdist_wheel

# upload to pypi
twine upload dist/*
```
