#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
