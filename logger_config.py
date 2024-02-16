import logging

# Define custom colors using ANSI escape codes
COLORS = {
    'DEBUG': '\033[94m',   # Blue
    'INFO': '\033[92m',    # Green
    'WARNING': '\033[93m', # Yellow
    'ERROR': '\033[91m',   # Red
    'CRITICAL': '\033[95m' # Magenta
}
RESET = '\033[0m'  # Reset to default color

# Custom formatter to add color to log messages
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = COLORS.get(levelname, RESET)
        return f'{color}{message}{RESET}'

def configure_logging():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('EscapePod.log'),
            logging.StreamHandler()
        ]
    )

    # Create logger
    logger = logging.getLogger()

    # Add console handler with custom formatter
    ch = logging.StreamHandler()
    ch.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

if __name__ == '__main__':
    configure_logging()
    print('main')
    logging.info('testing logger')