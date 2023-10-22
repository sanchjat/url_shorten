# -*- coding: utf-8 -*-

import os
from short_url import create_app


app = create_app(os.getenv("APP_CONFIGURATION", "Production"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
