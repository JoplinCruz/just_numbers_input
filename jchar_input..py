#
# JUST CHAR INPUT: jn_input.py
# Function for entry only character data, especifically integer with screen position option.
# Exemplo:
#       jn_input('Digit text: ')            # Text will appear with prompt cursor
#       jn_input('Name: ', 5, 20)           # Age: will appear with prompt cursor
#                                                  at position line 5, column 20,
#                                                  in prompt screen
#

#------------------------------------------| code imported  |--------------------------------+
import contextlib


try:
    import msvcrt

    # Length 0: sequences; length 1: sequences...
    ESCAPE_SEQUENCES = [frozenset(("\x00", "\xe0"))]

    get_key = msvcrt.getwch

    set_terminal_raw = contextlib.nullcontext

    key_ready = msvcrt.kbhit

except ImportError:  # Unix
    import sys, tty, termios, \
        select, functools

    # Length 0: sequences; length 1: sequences...
    ESCAPE_SEQUENCES = [
        frozenset(("\x1b",)),
        frozenset(("\x1b\x5b", "\x1b\x4f"))]

    @contextlib.contextmanager
    def set_terminal_raw():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    get_key = functools.partial(sys.stdin.read, 1)

    def input_ready():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


MAX_ESCAPE_SEQUENCE_LENGTH = len(ESCAPE_SEQUENCES)    # Calculate the sequence will be used

def get_keystroke():                                   # Capture key pressed
    key = get_key()
    if (len(key) <= MAX_ESCAPE_SEQUENCE_LENGTH and     # Verify sequence
            key in ESCAPE_SEQUENCES[len(key)-1]):
        key += get_key()                              # Assign the sequence \xe0
    return key

def is_flush():                                           # Clear keystroke buffer
    while key_ready():
        get_key()

#------------------------------------------------------------------------------------------------^


def jchar_input(limiter: int | None = None, *, message: str | None = '', flush: bool | None = True) -> str:
    """_summary_

    Args:
        limiter (int | None, optional): number of characters up to input data, None is unlimited. Defaults to None.
        message (str | None, optional): refer a text message displayed on screen before input data. Defaults to ''.
        flush (bool | None, optional): refresh hit key buffer. Defaults to True.

    Returns:
        str: results on selected type of data: numbers, strings, alpha...
    """
    
    # Variables:
    
    DIGIT_SEQUENCE = [chr(i) for i in range(48,58)]       # ['0', '1', '2', '3', ..., '8', '9']
    
    UPPERCASE_CHARACTER_SEQUENCE = [chr(32)] + [chr(i) for i in range(65,91)]

    LOWERCASE_CHARACTER_SEQUENCE = [chr(32)] + [chr(j) for j in range(97,123)]

    LATIM_SEQUENCE = [chr(i) for i in range(192,255)]
    
    SYMBOLS_SEQUENCE = [chr(i) for i in range(33,48)] + [chr(j) for j in range(58,65)] + [chr(k) for k in range(91,97)] + [chr(l) for l in range(123,127)]
    
    LOAD_SEQUENCE = UPPERCASE_CHARACTER_SEQUENCE + LOWERCASE_CHARACTER_SEQUENCE + SYMBOLS_SEQUENCE
    
    ESCAPE_KEYS = ['\r', '\x08', '\x1b', '\xe0\x53', '\xe0\x4b', '\xe0\x4d']       # ['enter', 'backspace', 'esc', 'delete', '<- arrow', '-> arrow']
    
    left_cursor_keystrokes = ''            # acumulate keystroke on the left side of cursor
    
    right_cursor_keystrokes = ''           # acumulate keystroke on the right side of cursor: this is a buffer
    
    data = ''                              # Will be returned
    
    key = ''                               # Key almost be reset after used in algorithim
    
    sensitive = 0                          # Define the sensitive key for backspace cursor position
    
    print (message, end='')                # Start message text to input data
    if flush:
        is_flush()
    
    with set_terminal_raw():               # Verify system: Windows, Unix
        
        while True:
            
            # Set prompt cursor:
            print (data + ' ', end=''); print ('\033[{0}D'.format(len(right_cursor_keystrokes) + 1), end='')
            
            while key not in LOAD_SEQUENCE and key not in ESCAPE_KEYS:   # Wait pressed key
                if key_ready() == True:                                    # Verify if key was pressed
                    key = get_keystroke()
            
            if key == '\r' or key == '\n':          # return or line feed
                if data == '':
                    data = '0'
                print ('\n', end='')
                return data
            
            if key == '\x1b':                       # escape: not return value
                return
            
            if key in LOAD_SEQUENCE:                  # add digit
                if limiter == None or len(data) < limiter:
                    if len(left_cursor_keystrokes) == 0:
                        sensitive = -2
                    else:
                        sensitive = -1
                    left_cursor_keystrokes += key
            
            if key == '\x08':                           # Backspace
                if len(left_cursor_keystrokes) == 0:
                    sensitive = -1
                else:
                    right_cursor_keystrokes = right_cursor_keystrokes
                    left_cursor_keystrokes = left_cursor_keystrokes[0:-1]
                    sensitive = 1
            
            if key == '\xe0\x53':                       # Delete
                if len(right_cursor_keystrokes) == 0:
                    if len(left_cursor_keystrokes) == 0:
                        sensitive = -1
                    else:
                        sensitive = 0
                else:
                    if len(left_cursor_keystrokes) == 0:
                        sensitive = -2
                    else:
                        sensitive = 0
                    right_cursor_keystrokes = right_cursor_keystrokes[1:]
                    left_cursor_keystrokes = left_cursor_keystrokes
            
            if key == '\xe0\x4b':                       # <- arrow cursor
                if len(left_cursor_keystrokes) == 0:
                    sensitive = -1
                else:
                    right_cursor_keystrokes = left_cursor_keystrokes[-1] + right_cursor_keystrokes
                    left_cursor_keystrokes = left_cursor_keystrokes[0:-1]
                    sensitive = 1
                               
            if key == '\xe0\x4d':                       # -> arrow cursor
                if len(right_cursor_keystrokes) == 0:
                    if len(left_cursor_keystrokes) == 0:
                        sensitive = -1
                    else:
                        sensitive = 0
                else:
                    if len(left_cursor_keystrokes) == 0:
                        sensitive = -2
                    else:
                        sensitive = -1
                    left_cursor_keystrokes = left_cursor_keystrokes + right_cursor_keystrokes[0]
                    right_cursor_keystrokes = right_cursor_keystrokes[1:]
            
            data = left_cursor_keystrokes + right_cursor_keystrokes             # number data

            if flush:                                                           # Reset buffer
                is_flush()
            key = ''                                                            # reset key
            
            # Positioning prompt cursor to print data on screen
            print (f'\033[{len(left_cursor_keystrokes) + sensitive}D', end=''); sensitive = 0

if __name__ == "__main__":
    name = jchar_input(20, message="name: ")
    print (name)