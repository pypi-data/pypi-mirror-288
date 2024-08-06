from typing import Any

from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware  # type:ignore


class WhiteNoiseSPAMiddleware(WhiteNoiseMiddleware):
    def __init__(self, *args: Any, **kwargs: Any):
        self.urls: list[str] = getattr(settings, "WHITENOISE_SPA_URLS", ["/"])
        super().__init__(*args, **kwargs)  # type:ignore
        root = getattr(settings, "WHITENOISE_SPA_ROOT", None)
        if root is not None:
            self.add_files(root)  # type:ignore

    def update_files_dictionary(self, *args: Any, **kwargs: Any):
        # add spa urls (DEBUG=False)
        super().update_files_dictionary(*args, **kwargs)  # type:ignore
        self.files: dict[str, Any]
        if "/index.html" not in self.files:
            return
        for url in self.urls:
            self.files[url] = self.files["/index.html"]

    def find_file(self, url: str):
        # add spa urls (DEBUG=True)
        if url in self.urls:
            url = "/index.html"
        return super().find_file(url)  # type:ignore
