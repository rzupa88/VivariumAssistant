from __future__ import annotations

import argparse
import asyncio

from vivariumassistant.packages.core.config_loader import load_enclosure
from vivariumassistant.packages.drivers.factory import build_drivers


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--enclosure", default="enclosure_1")
    ap.add_argument("--channel", type=int, required=True)
    ap.add_argument("--on", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    enc = load_enclosure(args.enclosure)
    bundle = build_drivers(enc)

    if args.dry_run:
        print(f"[dry-run] mode={bundle.mode} set channel={args.channel} on={args.on}")
        return

    await bundle.relay.set_on(args.channel, args.on)
    print(f"Set relay channel {args.channel} -> {args.on}")


if __name__ == "__main__":
    asyncio.run(main())