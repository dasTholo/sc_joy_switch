import time

import lxml

try:
    import layouter
except ImportError:
    from . import layouter
    print("bin ex")


def hello_world():
    print("Hello World!")
    print(f"Version {lxml.__version__}")
    print("Layouter")
    print(layouter.check_device(old_xml=layouter.root, device_list=["{812F3344-0000-0000-0000-504944564944}"]))
    time.sleep(10)


if __name__ == "__main__":
    print("Hello World!")
    hello_world()
    print(f"gertfig")
