# video-pymaker

This is a Python application to create and upload videos to YouTube automatically from a search term entered by the user. 

## Getting Started

To run this application, the following installations are required:

* Python 3.8.1 (or higher)
* ImageMagick 6.9.10-92 (or higher): used by the Wand for image editing

In addition, you must create an Algorithmia account, an IBM Cloud account and a Google Cloud account, as the services used by this application are available on these platforms. 

For more information on configuring these APIs, please visit this [link](https://github.com/filipedeschamps/video-maker#instala%C3%A7%C3%A3o) (in Portuguese) and/or visit the official pages for each service (links available in the [Built With](#built-with) section).

## Built With

* [Wikipedia Parser](https://algorithmia.com/algorithms/web/WikipediaParser) via [Algorithmia](https://algorithmia.com/)
* [NLTK](https://www.nltk.org/)
* [IBM Watson Natural Language Understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding)
* [Google Custom Search Engine](https://developers.google.com/custom-search) 
* [Wand](http://docs.wand-py.org/en/0.5.9/)
* [MoviePy](https://zulko.github.io/moviepy/)
* [YouTube Data API v3](https://developers.google.com/youtube/v3)

## Versions

[Version 1.0](https://github.com/limacaiquelg/video-pymaker/releases/tag/v1.0) - Initial Version

## Authors

| [<img src="https://avatars2.githubusercontent.com/u/17394016?v=3&s=115"><br><sub>@limacaiquelg</sub>](https://github.com/limacaiquelg) |
| :---: |

## Acknowledgments

This application is inspired by the incredible [video-maker](https://github.com/filipedeschamps/video-maker) project developed by [@filipedeschamps](https://github.com/filipedeschamps). Thank you so much Filipe for the learning opportunity!