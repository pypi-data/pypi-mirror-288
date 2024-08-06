# LOCALTRANS
LOCALTRANS is a library that facilitates local translation by reading previously translated content from a .pyt file for you.

## .pyt file structure
### Valid Structure 

    key=value
    key =value
    key= value
    key = value

> you can use any delimiter instead of '='

### Invalid Structure
    
    keyvalue
    key value
    key
    value
    key=
    =key
    value=
    =value

### Example .pyt file
    
    hello=merhaba
    hello world=merhaba dünya
    lorem ipsum is a test text = lorem ipsum bir deneme metnidir

> This is a valid .pyt file ( english to turkish )

### Usage
> pip install localtrans

#### Basic Usage
```python
from localtrans.translator import Translate

translator = Translate.initialize('/path/to/pyt/files/directory')

# delimiter's default is = so you don't have to add it into parameters
translated = translator.translate(to_lang='fr', text='hello', delimiter='=')

print(translated)
```

