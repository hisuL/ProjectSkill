#!/usr/bin/env python3
"""Open the PingCode OAuth authorize page in a browser."""

from __future__ import annotations

import argparse
import os
import urllib.parse
import webbrowser


def main() -> None:
    parser = argparse.ArgumentParser(description="打开 PingCode OAuth 授权页面")
    parser.add_argument("--oauth2-root", default=os.getenv("PINGCODE_BASE_URL", "https://open.pingcode.com"))
    parser.add_argument("--client-id", default=os.getenv("PINGCODE_CLIENT_ID"))
    parser.add_argument("--redirect-uri", default=os.getenv("PINGCODE_REDIRECT_URI"))
    args = parser.parse_args()

    if not args.client_id:
        raise SystemExit("缺少 client_id。请传入 --client-id 或设置 PINGCODE_CLIENT_ID。")

    query = {"response_type": "code", "client_id": args.client_id}
    if args.redirect_uri:
        query["redirect_uri"] = args.redirect_uri
    authorize_url = f"{args.oauth2_root.rstrip('/')}/oauth2/authorize?{urllib.parse.urlencode(query)}"

    print("PingCode OAuth 授权")
    print(authorize_url)
    print("浏览器将尝试打开授权页面。授权后，从回调地址中复制 code 参数。")
    webbrowser.open(authorize_url)


if __name__ == "__main__":
    main()
