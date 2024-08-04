# streamlit-hotfix
A command line tool to provide advanced features (CDN, etc) for streamlit by apply patch to the installed packages.

## Get started

```bash
pip install streamlit-hotfix
st-hotfix --help
```

For developer,

```
cd streamlit-hotfix
poetry install

python -m st_hotfix --help
```

Note that you have to install this tool in the same environment as streamlit and streamlit components you want to patch.
Otherwise, the patch may not work as expected.

## Examples

### Load streamlit assets from CDN


```bash
st-hotfix cdn dump streamit ./path/to/streamlit-assets

# now you can distribut streamlit-assets with CDN, for example jsDelivr 

st-hotfix cdn patch streamlit --cdn_url https://cdn.jsdelivr.net/gh/link89/assets@0.1.0/cdn/streamlit/
```
Now when you run your streamlit app, it will load assets from the CDN.
Note that the CDN tool makes use of the on-the-fly mode of webpack publicPath. 
Since `streamlit` 1.36.0, the publicPath of streamlit frontend can be override in runtime by setting `window.____WEBPACK_PUBLIC_PATH_OVERRIDE`.

If the components are not allow to change the publicPath on-the-fly, 
you have to patch them first by yourself before using this tool to patch it with CDN URL.
For example: https://github.com/mik-laj/streamlit-ketcher/pull/120/files

