#!/usr/bin/env python3
from .engine import Engine, Args


def main() -> None:
    Engine.run(Args().parse_args())


# See: https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

if __name__ == "__main__":
    main()
