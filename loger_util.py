from loguru import logger


logger.add("debug.log", format="{time} {level} {message}")
__all__ = ["logger"]