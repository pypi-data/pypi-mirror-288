import glob
import shutil
import os

from bs4 import BeautifulSoup

from .util import find_pkg_dir


class CdnCmd:
    """
    Commands for hotfixing streamlit and streamlit compoents to use CDN.
    """

    @property
    def dump(self):
        return dump
    
    @property
    def patch(self):
        return patch
    
    @property
    def restore(self):
        return restore


def dump(pkg_name: str, out_dir= './out'):
    """
    Find static assets in the package and dump them to the out_dir.

    Args:
        pkg_name (str): The package name.
        out_dir (str): The output directory
    """
    static_dir = os.path.dirname(_get_index_html(pkg_name))
    os.makedirs(out_dir, exist_ok=True)
    shutil.copytree(static_dir, out_dir, dirs_exist_ok=True)
    

def patch(pkg_name: str, cdn_url: str, 
          script_tempate = 'window.__WEBPACK_PUBLIC_PATH_OVERRIDE = "{cdn_url}";'):
    """
    Replace the static assets in the index.html with the cdn_url,
    and inject the script tag to override the webpack public path.

    Args:
        pkg_name (str): The package name.
        cdn_url (str): The cdn url.
        script_tempate (str): The script template to inject into the index.html.
    """
    index_html = _get_index_html(pkg_name)
    index_html_bak = f"{index_html}.bak"
    if not os.path.exists(index_html_bak):
        shutil.copy(index_html, index_html_bak)
    with open(index_html_bak, 'r') as f:
        html_doc = f.read()
    modified_html = _patch_index_html(html_doc, cdn_url, script_tempate)
    with open(index_html, 'w') as f:
        f.write(modified_html)
    print(f"file {index_html} patched.")


def restore(pkg_name: str):
    """
    Restore the index.html to the original state.

    Args:
        pkg_name (str): The package name.
    """
    index_html = _get_index_html(pkg_name)
    index_html_bak = f"{index_html}.bak"
    if not os.path.exists(index_html_bak):
        print(f"Backup file {index_html_bak} not found.")
        return
    shutil.copy(index_html_bak, index_html)
    print(f"file {index_html} restored.")


def _patch_index_html(html_doc: str, cdn_url: str, script_tempate: str):
    if not cdn_url.endswith('/'):
        cdn_url = cdn_url + '/'
    soup = BeautifulSoup(html_doc, 'html.parser')
    # Add the new script tag
    new_script = soup.new_tag("script")
    new_script.string = script_tempate.format(cdn_url=cdn_url)
    soup.head.insert(0, new_script)

    # Replace all href attributes in <script> and <link> tags
    for tag in soup.find_all(['script', 'link']):
        if 'href' in tag.attrs:
            old_href = tag['href'].lstrip('.').lstrip('/')
            tag['href'] = f"{cdn_url}{old_href}"
    return str(soup)


def _get_index_html(pkg_name: str):
    pkg_path = find_pkg_dir(pkg_name)
    results = glob.glob(f"{pkg_path}/**/index.html", recursive=True)
    if not results:
        raise ValueError(f"index.html not found in {pkg_name}")
    if len(results) > 1:
        print(f"Multiple index.html found in {pkg_name}, using the first one.")
        for result in results:
            print(result)
    return results[0]
