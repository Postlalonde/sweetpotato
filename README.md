<img src="https://raw.githubusercontent.com/greysonlalonde/sweetpotato/main/media/sweetpotato_github_banner.png" height=25% alt="">

-----
[![alt text](https://img.shields.io/badge/pypi-0.4.a0-blue)](https://pypi.org/project/sweetpotato)
[![alt text](https://img.shields.io/badge/license-MIT-green)](https://github.com/greysonlalonde/sweetpotato/blob/main/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/sweetpotato/badge/?version=latest)](https://sweetpotato.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### *This project is still in early stages of development and is not stable.*

Sweetpotato provides an intuitive wrapper around React Native, making cross-platform development (iOS, Android, Web)
accessible from Python.

- Supported packages include but are not limited to:
    - [react-native](https://reactnative.dev)
    - [expo](https://expo.dev)
    - [react-navigation](https://reactnavigation.org)
    - [react-native-ui-kitten](https://akveo.github.io/react-native-ui-kitten/)

------

See [https://sweetpotato.readthedocs.io](https://sweetpotato.readthedocs.io) for documentation.

-----
You can view the below example at the following links:
[Web](https://snack-web-player.s3.us-west-1.amazonaws.com/v2/44/index.html?initialUrl=exp%3A%2F%2Fexp.host%2F%40greysonlalonde13%2Famused-crackers%2BAAZPRuW6dY&origin=https%3A%2F%2Fsnack.expo.dev&verbose=false)
,
[iOS](https://appetize.io/embed/8bnmakzrptf1hv9dq7v7bnteem?autoplay=false&debug=true&device=iphone12&embed=true&scale=73&screenOnly=false&xDocMsg=true&xdocMsg=true&params=%7B%22EXDevMenuDisableAutoLaunch%22%3Atrue%2C%22EXKernelLaunchUrlDefaultsKey%22%3A%22exp%3A%2F%2Fexp.host%2F%40greysonlalonde13%2Famused-crackers%2BAAZPRuW6dY%22%2C%22EXKernelDisableNuxDefaultsKey%22%3Atrue%7D&osVersion=14.5)
,
[Android](https://appetize.io/embed/xc1w6f1krd589zhp22a0mgftyw?autoplay=false&debug=true&device=pixel4&embed=true&launchUrl=exp%3A%2F%2Fexp.host%2F%40greysonlalonde13%2Famused-crackers%2BAAZPRuW6dY&scale=81&screenOnly=false&xDocMsg=true&xdocMsg=true&params=%7B%22EXDevMenuDisableAutoLaunch%22%3Atrue%2C%22EXKernelLaunchUrlDefaultsKey%22%3A%22exp%3A%2F%2Fexp.host%2F%40greysonlalonde13%2Famused-crackers%2BAAZPRuW6dY%22%2C%22EXKernelDisableNuxDefaultsKey%22%3Atrue%7D&osVersion=11.0)

```python
from sweetpotato.app import App
from sweetpotato.components import Text, Button, Image
from sweetpotato.ui_kitten import Layout
from sweetpotato.config import settings
from sweetpotato.navigation import create_bottom_tab_navigator

settings.USE_UI_KITTEN = True
settings.USE_NAVIGATION = True

view_style = {
    "justifyContent": "center",
    "alignItems": "center", "flex": 1,
}
image_style = {'height': 200, 'width': 200, 'borderRadius': 50}
tab = create_bottom_tab_navigator(name="tab")

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ipomoea_batatas_006.JPG/1920px"
"-Ipomoea_batatas_006.JPG "
home_page = Layout(
    style=view_style,
    children=[
        Image(style=image_style, source={"uri": image_url}),
        Text(style={'margin': 25}, text="Sweet, Sweet Potatoes"),
        Button(title="Info", onPress="() => alert('This app was made with sweetpotato')")
    ]
)

tab.screen(
    screen_name="Home",
    children=[home_page],
)
app = App(component=tab, theme="dark")

if __name__ == "__main__":
    app.run()

```

iOS, Android, and web:
<img src="https://raw.githubusercontent.com/greysonlalonde/sweetpotato/main/media/sweetpotato_readme_example.jpg" width=100% height=25% alt="">

Navigation example:

```python
from sweetpotato.app import App
from sweetpotato.config import settings
from sweetpotato.navigation import create_bottom_tab_navigator
from sweetpotato.components import (
    View,
    Text,
)

settings.USE_NAVIGATION = True

tab = create_bottom_tab_navigator()

tab.screen(screen_name="Screen One", children=[View(children=[Text(text="Hello")])])
tab.screen(screen_name="Screen Two", children=[View(children=[Text(text="World")])])

app = App(component=tab)

if __name__ == "__main__":
    app.run()
```

