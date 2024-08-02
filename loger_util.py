from loguru import logger


logger.add("logs/debug.log", format="{time} {level} {message}", rotation="8:00", compression="zip")
__all__ = ["logger"]