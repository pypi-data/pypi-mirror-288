from click import group, option
from loguru import logger

from .browser import get_page_source


@group(name='web', help="Web utilities")
def web():
    pass


@web.command(help="View a web page (support js)")
@option('-l', '--link', type=str, required=True, prompt=True,
        help="Link to the web page")
def view(link: str):
    logger.debug("conv list")
    source = get_page_source(link)
    print(source)
