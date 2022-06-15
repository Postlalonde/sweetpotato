# Sweetpotato

-----
[![alt text](https://img.shields.io/badge/pypi-0.1.a0-blue)](https://pypi.org/project/shareable) [![alt text](https://img.shields.io/badge/license-MIT-green)](https://github.com/greysonlalonde/shareable/blob/main/LICENSE)

Sweetpotato provides an intuitive wrapper around React Native, making cross-platform development accessible from Python.
- Supported packages:
  - [react-native](https://reactnative.dev)
  - [expo](https://expo.dev)
  - [react-navigation](https://reactnavigation.org)
  - [react-native-ui-kitten](https://akveo.github.io/react-native-ui-kitten/)
------

### Installation:
1. Install sweetpotato
  - pip:
```commandline
pip install sweetpotato
```
  - conda:
```commandline
conda install sweetpotato
```
2. Install [Node.js](https://nodejs.org/en/)
3. Install [Git](https://git-scm.com)
4. Install [yarn](https://classic.yarnpkg.com/en/docs/install) and [expo](https://docs.expo.dev/get-started/installation/)
```commandline
npm install --global yarn expo-cli
```
-----
Simple example:

```python
from sweetpotato.app import App
from sweetpotato.components import (
    View, 
    Text,
)

app = App(
    children=[
        View(
            style={"justifyContent": "center", "alignItems": "center", "height": "100%"},
            children=[
                Text(text="Hello World")
            ],
        )
    ]
)


if __name__ == "__main__":
    app.run()                
```
(cant see this as a private repo, go to media folder)
<img src="https://raw.githubusercontent.com/greysonlalonde/sweetpotato/main/media/readme_example.png?token=GHSAT0AAAAAABRVMLYCCZOSMGMRDYIRP4QCYSYUQRA" width=25% height=25%>

Navigation example:
```python
from sweetpotato.app import App
from sweetpotato.navigation import TabNavigator
from sweetpotato.components import (
  View, 
  Text,
)

tab = TabNavigator()

tab.screen(screen_name="Screen One", children=[View(children=[Text(text="Hello")])])
tab.screen(screen_name="Screen Two", children=[View(children=[Text(text="World")])])

app = App(children=[tab])

if __name__ == "__main__":
    app.run()
```
(cant see this as a private repo, go to media folder)
<img src="https://raw.githubusercontent.com/greysonlalonde/sweetpotato/main/media/readme_example.png?token=GHSAT0AAAAAABRVMLYCCZOSMGMRDYIRP4QCYSYUQRA" width=25% height=25%>

