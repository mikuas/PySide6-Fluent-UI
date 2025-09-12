from pathlib import Path
import logging

__PATH__ = Path(__file__).resolve().parent


def main():
    logging.basicConfig(
        # filename=r"C:\Projects\PythonModules\PythonModule\QtAppDemo\tests\\app.log",
        filename=rf"{__PATH__}\\application.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logging.info("this is test text")
    logging.shutdown()


if __name__ == '__main__':
    main()