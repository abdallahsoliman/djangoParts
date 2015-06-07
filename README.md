# djangoParts
A view framework for Django


##Install

- Clone the repo into a place that is in your pythonpath. The repo itself is a Python package.
- Add `"djangoParts.parts"` to your `INSTALLED_APPS` in your project's `settings.py`


##Getting Started

###Creating the Page part

In the terms of a web application, the "page" is the index.html that loads first from the webserver. All dependencies are defined within this html file.

The same is true in Django Parts. This app serves as the "top level" that will be present in all page loads. The template is included in the JP framework, and is structured like this:

```
<html>
    <head>
        <link/>
        <link/>
        <script></script>
        etc...
    </head>
    <body>
        {{page_content}}
    </body>
</html
```

To create the main page app:

- `./manage.py startapp mainPage`
- Make the views.py in the `mainPage` app look like this:

```
from djangoParts.parts import Page

class MainPage(Page):
    PART_LIST = []
```

That's it. You have just created the main page.

###urls.py

- In your main `urls.py` file. Delete everything, and add the following:

```
from mainPage.views import MainPage

urlpatters = MainPage().getUrls(MainPage)
```

That's it. All urls will be generated at application runtime by the main page app

###Your first index app

To create an additional app:

- `manage.py startapp index`
- `mkdir -p index/templates/index`
- make the `index/templates/index/index.html` file look like this:

```
<h1>THIS IS INDEX</h1>
```

- Make `index/views.py` look like this:

```
from djangoParts.parts import Part

class Index(Part):
    NAME = "index"
    TEMPLATE_PATH = "index/index.html"
```

- Install the index app, by adding it to `INSTALLED_APPS` in `settings.py`
- The index will be owned by the main page app, so add it to the `PARTS_LIST` in the `MainPage` part:

`mainPage/views.py`:
```
from djangoParts.parts import Page
from index.views import Index

class MainPage(Page):
    PART_LIST = [
                    Index,
                ]
```

- Run the project, and the index should appear
