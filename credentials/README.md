# Credentials Directory

In this directory are the files with the credentials of the services used by the video-pymaker. In the current version, the following files are required:

```
content
│    algorithmia.json
│    watson-nlu.json
│    google-search.json
│    client-secrets.json
```

## Algorithmia Credentials

Credentials used to access Algorithmia features. This JSON file (`algorithmia.json`) has the following structure:

```
{
    "api_key": "YOUR_API_KEY"
}
```
You can find this API Key on your Algorithmia dashboard. 

## IBM Watson NLU Credentials

Credentials used to access IBM Watson Natural Language Understanding features. This JSON file (`watson-nlu.json`) has the following structure:

```
{
    "apikey": "YOUR_API_KEY",
    "iam_apikey_description": "API_KEY_DESCRIPTION",
    "iam_apikey_name": "API_KEY_NAME",
    "iam_role_crn": "ROLE_IDENTIFIER",
    "iam_serviceid_crn": "SERVICE_ID",
    "url": "YOUR_WATSON_NLU_INSTANCE_URL"
}
```
After configuring the service, you can find these credentials on the IBM Cloud website. 

## Google CSE Credentials

Credentials used to access Google Custom Search Engine features. This JSON file (`google-search.json`) has the following structure:

```
{
    "api-key": "YOUR_API_KEY",
    "search-engine-id": "YOUR_CUSTOM_SEARCH_ENGINE_IDENTIFIER"
}
```
After configuring the service, you can find these credentials on your Google Cloud Platform dashboard. 

## YouTube Data API Credentials

Credentials used to access YouTube Data API features. This JSON file (`client-secrets.json`) has the following structure:

```
{
    "web":
    { 
        "client_id": "CLIENT_ID",
        "project_id": "GOOGLE_CLOUD_PLATFORM_PROJECT_ID",
        "auth_uri": "OAUTH_URI",
        "token_uri": "OAUTH_TOKEN_URI",
        "auth_provider_x509_cert_url": "OAUTH_PROVIDER",
        "client_secret": "YOUR_API_KEY",
        "redirect_uris":
        [
          "REDIRECT_URI_AFTER_AUTHENTICATION"
        ],
        "javascript_origins":
        [
          "INITIAL_URI_BEFORE_AUTHENTICATION"
        ]
    }
}
```
After configuring the service, you can find these credentials on your Google Cloud Platform dashboard.