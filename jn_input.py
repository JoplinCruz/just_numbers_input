#
# JUST NUMBER INPUT: jn_input.py
# Function for entry only numeric data, especifically integer with screen position option.
# Exemplo:
#       jn_input('Digit numbers: ')         # Text will appear with prompt cursor
#       jn_input('Age: ', 5, 20)            # Age: will appear with prompt cursor at position line 5, column 20, in prompt screen
#

#------------------------------------------| code imported  |--------------------------------+
import contextlib as _contextlib


try:
    import msvcrt as _msvcrt

    # Length 0: sequences; length 1: sequences...
    _ESCAPE_SEQUENCES = [frozenset(("\x00", "\xe0"))]

    _get_key = _msvcrt.getwch

    _set_terminal_raw = _contextlib.nullcontext

    _key_ready = _msvcrt.kbhit

except ImportError:  # Unix
    import sys as _sys, tty as _tty, termios as _termios, \
        select as _select, functools as _functools

    # Length 0: sequences; length 1: sequences...
    _ESCAPE_SEQUENCES = [
        frozenset(("\x1b",)),
        frozenset(("\x1b\x5b", "\x1b\x4f"))]

    @_contextlib.contextmanager
    def _set_terminal_raw():
        fd = _sys.stdin.fileno()
        old_settings = _termios.tcgetattr(fd)
        try:
            _tty.setraw(_sys.stdin.fileno())
            yield
        finally:
            _termios.tcsetattr(fd, _termios.TCSADRAIN, old_settings)

    _get_key = _functools.partial(_sys.stdin.read, 1)

    def _input_ready():
        return _select.select([_sys.stdin], [], [], 0) == ([_sys.stdin], [], [])


_MAX_ESCAPE_SEQUENCE_LENGTH = len(_ESCAPE_SEQUENCES)    # Calculate the sequence will be used

def _get_keystroke():                                   # Capture key pressed
    key = _get_key()
    if (len(key) <= _MAX_ESCAPE_SEQUENCE_LENGTH and     # Verify sequence
            key in _ESCAPE_SEQUENCES[len(key)-1]):
        key += _get_key()                              # Assign the sequence \xe0
    return key

def _flush():                                           # Clear keystroke buffer
    while _key_ready():
        _get_key()

#------------------------------------------------------------------------------------------------^


def jn_input(message: str | None = '', *, flush: bool | None = True) -> str:
    
    # Variables:
    
    _DIGIT_SEQUENCE = [str(i) for i in range(10)]       # ['0', '1', '2', '3', ..., '8', '9']
    
    _ESCAPE_KEYS = ['\r', '\x08', '\x1b', '\xe0\x53', '\xe0\x4b', '\xe0\x4d']       # ['enter', 'backspace', 'esc', 'delete', '<- arrow', '-> arrow']
    
    _left_cursor_keystrokes = ''            # acumulate keystroke on the left side of cursor
    
    _right_cursor_keystrokes = ''           # acumulate keystroke on the right side of cursor: this is a buffer
    
    _number = ''                            # Will be returned
    
    key = ''                                # Key almost be reset after used in algorithim
    
    _sensitive = 0                          # Define the sensitive key for backspace cursor position
    
    print (message, end='')                 # Start message text to input data
    if flush:
        _flush()
    
    with _set_terminal_raw():               # Verify system: Windows, Unix
        
        while True:
            
            # Set prompt cursor:
            print (_number + ' ', end=''); print ('\033[{0}D'.format(len(_right_cursor_keystrokes) + 1), end='')
            
            while key not in _DIGIT_SEQUENCE and key not in _ESCAPE_KEYS:   # Wait pressed key
                if _key_ready() == True:                                    # Verify if key was pressed
                    key = _get_keystroke()
            
            if key == '\r' or key == '\n':          # return or line feed
                if _number == '':
                    _number = '0'
                print ('\n', end='')
                return int(_number)
            
            if key == '\x1b':                       # escape: not return value
                return
            
            if key in _DIGIT_SEQUENCE:                  # add digit
                if len(_left_cursor_keystrokes) == 0:
                    _sensitive = -2
                else:
                    _sensitive = -1
                _left_cursor_keystrokes += key
            
            if key == '\x08':                           # Backspace
                if len(_left_cursor_keystrokes) == 0:
                    _sensitive = -1
                else:
                    _right_cursor_keystrokes = _right_cursor_keystrokes
                    _left_cursor_keystrokes = _left_cursor_keystrokes[0:-1]
                    _sensitive = 1
            
            if key == '\xe0\x53':                       # Delete
                if len(_right_cursor_keystrokes) > 0:
                    _right_cursor_keystrokes = _right_cursor_keystrokes[1:]
                    _left_cursor_keystrokes = _left_cursor_keystrokes
            
            if key == '\xe0\x4b':                       # <- arrow cursor
                if len(_left_cursor_keystrokes) == 0:
                    _sensitive = -1
                else:
                    _right_cursor_keystrokes = _left_cursor_keystrokes[-1] + _right_cursor_keystrokes
                    _left_cursor_keystrokes = _left_cursor_keystrokes[0:-1]
                    _sensitive = 1
            
            if key == '\xe0\x4d':                       # -> arrow cursor
                if len(_right_cursor_keystrokes) == 0:
                    _sensitive = 0
                else:
                    if len(_left_cursor_keystrokes) == 0:
                        _sensitive = -2
                    else:
                        _sensitive = -1
                    _left_cursor_keystrokes = _left_cursor_keystrokes + _right_cursor_keystrokes[0]
                    _right_cursor_keystrokes = _right_cursor_keystrokes[1:]
            
            _number = _left_cursor_keystrokes + _right_cursor_keystrokes        # number data

            if flush:                                                           # Reset buffer
                _flush()
            key = ''                                                            # reset key
            
            # Positioning prompt cursor to print data on screen
            print (f'\033[{len(_left_cursor_keystrokes) + _sensitive}D', end=''); _sensitive = 0

