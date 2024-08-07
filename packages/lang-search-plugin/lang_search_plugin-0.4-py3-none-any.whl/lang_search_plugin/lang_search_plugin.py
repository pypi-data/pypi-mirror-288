from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation
from mkdocs.config import config_options
import logging

log = logging.getLogger("mkdocs.plugins." + __name__)

class LangSearchPlugin(BasePlugin):
    config_scheme = (
        ('default_language', config_options.Type(str, default='en')),
        ('languages', config_options.Type(list, default=['en', 'pt'])),
    )

    def __init__(self):
        super().__init__()
        log.info("LangSearchPlugin initialized")

    def on_pre_page(self, page: Page, config, files):
        """Process each page before it is converted to HTML."""
        try:
            log.info(f"Processing page: {page.file.src_path}")
            language = self._get_language_from_path(page.file.src_path)
            page.meta['language'] = language
            log.debug(f"Set language for {page.file.src_path} to {language}")
        except Exception as e:
            log.error(f"Error processing page {page.file.src_path}: {e}")
        return page

    def on_nav(self, nav: Navigation, config, files):
        """Modify navigation items based on the selected language."""
        try:
            log.info("Modifying navigation items based on selected language")
            selected_language = self._get_selected_language(config)
            nav.items = [item for item in nav.items if item.file.src_path.startswith(f"{selected_language}/")]
            log.debug(f"Filtered navigation items to selected language: {selected_language}")
        except Exception as e:
            log.error(f"Error modifying navigation items: {e}")
        return nav

    def on_page_context(self, context, page: Page, config, nav: Navigation):
        """Set the search index context for each page."""
        try:
            log.info(f"Setting search index context for page: {page.file.src_path}")
            selected_language = self._get_selected_language(config)
            context['search'] = {
                'index': [p for p in nav.pages if p.file.src_path.startswith(f"{selected_language}/")]
            }
            log.debug(f"Search context set for selected language: {selected_language}")
        except Exception as e:
            log.error(f"Error setting search index context for page {page.file.src_path}: {e}")
        return context

    def on_config(self, config):
        """Handle updates to the configuration."""
        try:
            log.info("Configuring LangSearchPlugin")
        except Exception as e:
            log.error(f"Error configuring LangSearchPlugin: {e}")
        return config

    def _get_language_from_path(self, path):
        """Extract the language from the file path."""
        parts = path.split('/')
        if parts[0] in self.config['languages']:
            return parts[0]
        return self.config['default_language']

    def _get_selected_language(self, config):
        """Determine the selected language from the configuration or environment."""
        return config.get('selected_language', self.config['default_language'])

