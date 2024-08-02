from __future__ import annotations
import re
from ast import literal_eval
import sys
from mymulti_key_dict import MultiKeyDict
from functools import cache
import subprocess
import ctypes
import threading
import platform
from collections import deque
import os

modconf = sys.modules[__name__]
modconf.all_categories_eventparser = (
    b"sourceNodeId",
    b"windowId",
    b"accessibilityViewId",
    b"virtualDescendantId",
    b"mParentNodeId",
    b"traversalBefore",
    b"traversalAfter",
    b"MovementGranularities",
    b"childAccessibilityIds",
    b"boundsInParent",
    b"boundsInScreen",
    b"packageName",
    b"className",
    b"text",
    b"error",
    b"maxTextLength",
    b"stateDescription",
    b"contentDescription",
    b"tooltipText",
    b"viewIdResName",
    b"checkable",
    b"checked",
    b"focusable",
    b"focused",
    b"selected",
    b"clickable",
    b"longClickable",
    b"contextClickable",
    b"enabled",
    b"password",
    b"scrollable",
    b"importantForAccessibility",
    b"visible",
    b"actions",
    b"AccessibilityAction",
)

mcfg = sys.modules[__name__]
mcfg.debug_mode = False
screenres_reg_cur = re.compile(rb"\bcur=(\d+)x(\d+)\b")
screenres_reg = re.compile(rb"\b(\d+)x(\d+)\b")
not_number_regex = re.compile(rb"\D+")

iswindows = "win" in platform.platform().lower()
if iswindows:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    creationflags = subprocess.CREATE_NO_WINDOW
    invisibledict = {
        "startupinfo": startupinfo,
        "creationflags": creationflags,
        "start_new_session": True,
    }
    from ctypes import wintypes

    windll = ctypes.LibraryLoader(ctypes.WinDLL)
    kernel32 = windll.kernel32
    GetExitCodeProcess = windll.kernel32.GetExitCodeProcess
    _GetShortPathNameW = kernel32.GetShortPathNameW
    _GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
    _GetShortPathNameW.restype = wintypes.DWORD
else:
    invisibledict = {}


@cache
def get_short_path_name(long_name):
    """
    Get the short path name for a given long path name (Windows only).

    Args:
        long_name (str): The long path name.

    Returns:
        str: The short path name.
    """
    try:
        if not iswindows:
            return long_name
        output_buf_size = 4096
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        _ = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        return output_buf.value
    except Exception:
        pass
    return long_name


class Trie:
    def __init__(self):
        """
        Initialize the Trie object.
        """
        self.data = MultiKeyDict({})
        self.compiled_regex = ""
        self._oldhash = 0
        self._isbytes = False

    def _addbytes(self, word):
        """
        Add a byte word to the Trie.

        Args:
            word (bytes): The byte word to add.
        """
        ref = self.data
        for char in range(len(word)):
            ref[word[char : char + 1]] = (
                word[char : char + 1] in ref and ref[word[char : char + 1]] or {}
            )
            ref = ref[word[char : char + 1]]
        ref[b""] = 1

    def _add(self, word: str):
        """
        Add a string word to the Trie.

        Args:
            word (str): The word to add.
        """
        if self._isbytes:
            self._addbytes(word)
        else:
            word2 = list(word)
            word2.append("")
            self.data[word2] = 1

    @cache
    def _quote(self, char):
        """
        Escape special characters in a string for use in a regular expression.

        Args:
            char (str): The character to escape.

        Returns:
            str: The escaped character.
        """
        return re.escape(char)

    def _pattern(self, pdata):
        """
        Generate a regular expression pattern from the Trie data.

        Args:
            pdata (dict): The Trie data.

        Returns:
            str | None: The regular expression pattern.
        """
        data = pdata
        if not self._isbytes:
            if "" in data and len(data) == 1:
                return None
        else:
            if b"" in data and len(data) == 1:
                return None
        alt = []
        cc = []
        q = 0
        for char in sorted(data):
            if isinstance(data[char], dict):
                qu = self._quote(char)
                try:
                    recurse = self._pattern(data[char])
                    alt.append(qu + recurse)
                except Exception:
                    cc.append(qu)
            else:
                q = 1
        cconly = not len(alt) > 0
        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                if not self._isbytes:
                    alt.append("[" + "".join(cc) + "]")
                else:
                    alt.append(b"[" + b"".join(cc) + b"]")
        if len(alt) == 1:
            result = alt[0]
        else:
            if not self._isbytes:
                result = "(?:" + "|".join(alt) + ")"
            else:
                result = b"(?:" + b"|".join(alt) + b")"
        if q:
            if cconly:
                if not self._isbytes:
                    result += "?"
                else:
                    result += b"?"
            else:
                if not self._isbytes:
                    result = f"(?:{result})?"
                else:
                    result = b"(?:" + result + b")?"
        return result

    def _get_pattern(self):
        """
        Get the compiled pattern from the Trie data.

        Returns:
            str: The compiled pattern.
        """
        return self._pattern(self.data)

    def compile(
        self,
        add_before="",
        add_after="",
        boundary_right: bool = False,
        boundary_left: bool = False,
        capture: bool = False,
        match_whole_line: bool = False,
        flags: int = re.IGNORECASE,
    ):
        """
        Compile the Trie data into a regular expression pattern.

        Args:
            add_before (str, optional): Text to add before the pattern. Defaults to "".
            add_after (str, optional): Text to add after the pattern. Defaults to "".
            boundary_right (bool, optional): Whether to add a word boundary at the end. Defaults to False.
            boundary_left (bool, optional): Whether to add a word boundary at the start. Defaults to False.
            capture (bool, optional): Whether to capture the matched text. Defaults to False.
            match_whole_line (bool, optional): Whether to match the whole line. Defaults to False.
            flags (int, optional): Regular expression flags. Defaults to re.IGNORECASE.

        Returns:
            Trie: The compiled Trie object.
        """
        if not self._isbytes:
            anfang = ""
            ende = ""
            if match_whole_line is True:
                anfang += r"^\s*"
            if boundary_right is True:
                ende += r"\b"
            if capture is True:
                anfang += "("
            if boundary_left is True:
                anfang += r"\b"
            if capture is True:
                ende += ")"
            if match_whole_line is True:
                ende += r"\s*$"
        else:
            anfang = b""
            ende = b""
            if match_whole_line is True:
                anfang += rb"^\s*"
            if boundary_right is True:
                ende += rb"\b"
            if capture is True:
                anfang += b"("
            if boundary_left is True:
                anfang += rb"\b"
            if capture is True:
                ende += b")"
            if match_whole_line is True:
                ende += rb"\s*$"
            if not isinstance(add_before, bytes):
                add_before = add_before.encode("utf-8")
            if not isinstance(add_after, bytes):
                add_after = add_after.encode("utf-8")
        if (
            newhash := hash(
                f"""{add_before}{anfang}{self.data.to_dict()}{ende}{add_after}{flags}"""
            )
        ) == self._oldhash:
            return self
        else:
            self.compiled_regex = re.compile(
                add_before + anfang + self._get_pattern() + ende + add_after, flags
            )
            self._oldhash = newhash
        return self

    def regex_from_words(
        self,
        words: list | tuple,
    ):
        """
        Generate a regular expression from a list of words.

        Args:
            words (list | tuple): The list of words.

        Returns:
            Trie: The Trie object.
        """
        if not isinstance(words[0], str):
            self._isbytes = True
            if isinstance(self.compiled_regex, str):
                self.compiled_regex = b""
        for word in words:
            self._add(word)
        return self


def generate_trie_regex(all_categories_eventparser):
    """
    Generate a Trie regular expression from event parser categories.

    Args:
        all_categories_eventparser (tuple): All event parser categories.

    Returns:
        tuple: A tuple containing:
            - all_categories_eventparser_as_unicode (dict): Event parser categories as unicode.
            - all_categories_eventparser_list (list): Event parser categories as a list.
            - compiled_regex (str): The compiled regular expression.
    """
    all_categories_eventparser_as_unicode = {
        k: k.decode() for k in all_categories_eventparser
    }
    all_categories_eventparser_list = list(
        all_categories_eventparser_as_unicode.values()
    )
    return (
        all_categories_eventparser_as_unicode,
        all_categories_eventparser_list,
        (
            Trie()
            .regex_from_words(all_categories_eventparser)
            .compile(
                add_before=rb"(?:\s+)",
                add_after=rb"(?::)",
                boundary_right=True,
                boundary_left=True,
                capture=True,
                match_whole_line=False,
                flags=0,
            )
        ).compiled_regex,
    )


def _killthread(threadobject):
    """
    Kill a thread.

    Args:
        threadobject (threading.Thread): The thread object to kill.

    Returns:
        bool: True if thread was killed, False otherwise.
    """
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


@cache
def parse_single_values(v1, v2):
    """
    Parse single values from byte strings.

    Args:
        v1 (bytes): The first value.
        v2 (bytes): The second value.

    Returns:
        tuple: A tuple containing the parsed values.
    """
    try:
        v1 = v1.strip()
    except Exception:
        pass
    try:
        v2 = v2.strip()
    except Exception:
        pass
    try:
        v2 = v2.rstrip(b";")
    except Exception:
        pass
    try:
        if v1.startswith(b"add("):
            v1 = v1[4:]
    except Exception:
        pass
    try:
        v1 = v1.decode("utf-8", "backslashreplace")
    except Exception:
        pass
    if v2.startswith(b"0x") or "AccessibilityNodeInfo" in v1:
        try:
            v2 = int(v2, 16)
            return v1, v2
        except Exception:
            pass

    if v2.startswith(b"Rect("):
        try:
            v2_1, v2_2 = v2.split(b" - ")
            v2_1 = tuple((int(x) for x in not_number_regex.split(v2_1) if x))
            v2_2 = tuple((int(x) for x in not_number_regex.split(v2_2) if x))
            v2 = v2_1 + v2_2
            return v1, v2
        except Exception:
            pass
    if v2 == b"true":
        v2 = True
        return v1, v2
    if v2 == b"false":
        v2 = False
        return v1, v2

    try:
        v2 = literal_eval(v2)
        return v1, v2
    except Exception:
        pass

    try:  # v1,v2
        v2 = v2.decode("utf-8", "backslashreplace")
        return v1, v2
    except Exception:
        pass
    return v1, v2


all_categories_eventparser_unicode = sorted(
    set(
        [x.decode("utf-8") for x in modconf.all_categories_eventparser]
        + [
            "aa_startx",
            "aa_starty",
            "aa_endx",
            "aa_endy",
            "aa_centerx",
            "aa_centery",
            "aa_area",
            "aa_width",
            "aa_height",
            "android.view.accessibility.AccessibilityNodeInfo",
        ]
    ),
    key=lambda x: x.lower(),
)

(
    all_categories_eventparser_as_unicode,
    all_categories_eventparser_list,
    compiled_regex_categories,
) = generate_trie_regex(modconf.all_categories_eventparser)


def splitlinesregex(l):
    """
    Split lines using a compiled regular expression and parse values.

    Args:
        l (bytes): The line to split.

    Returns:
        dict: The parsed values.
    """
    vay = l.replace(b"\r\n", b"\n")
    results_dict = dict.fromkeys(all_categories_eventparser_unicode)
    vay = compiled_regex_categories.split(vay)
    vay = vay[0].rsplit(b"@", maxsplit=1) + vay[1:]
    for l1 in range(0, len(vay) - 1, 2):
        try:
            dictkey, dictvalue = parse_single_values(vay[l1], vay[l1 + 1])
            results_dict[dictkey] = dictvalue
        except Exception:
            pass
    try:
        startx, starty, endx, endy = results_dict["boundsInScreen"]
        centerx = (startx + endx) // 2
        centery = (starty + endy) // 2
        width = endx - startx
        height = endy - starty
        area = width * height
        results_dict["aa_startx"] = startx
        results_dict["aa_starty"] = starty
        results_dict["aa_endx"] = endx
        results_dict["aa_endy"] = endy
        results_dict["aa_centerx"] = centerx
        results_dict["aa_centery"] = centery
        results_dict["aa_area"] = area
        results_dict["aa_width"] = width
        results_dict["aa_height"] = height
    except Exception:
        pass
    return results_dict


class LogCatParser:
    def __init__(
        self,
        adb_path=None,
        device_serial=None,
        path_logcat="logcat",
        path_top="top",
        path_grep="grep",
        path_awk="awk",
        path_kill="kill",
        path_sh="sh",
        path_printf="printf",
        path_wm="wm",
        path_tail="tail",
        path_sed="sed",
        path_su="su",
        path_pm="pm",
        path_tmp_folder="/sdcard/_lgcattmp",
        screen_width=0,
        screen_height=0,
        sleep_logcat=1,
        kwargs_subprocess=None,
        thread_daemon=True,
        buffer_stdout=10000,
        buffer_stderr=10000,
        search_string=b"add(",
        refresh_screen_add_width=0,
        refresh_screen_add_height=1,
    ):
        """
                Initialize the LogCatParser object.

                Args:
                    adb_path (str, optional): Path to adb. Defaults to None (when running directly on the emulator).
                    device_serial (str, optional): Device serial. Defaults to None (when running directly on the emulator).
                    path_logcat (str, optional): Path to logcat. Defaults to "logcat".
                    path_top (str, optional): Path to top. Defaults to "top".
                    path_grep (str, optional): Path to grep. Defaults to "grep".
                    path_awk (str, optional): Path to awk. Defaults to "awk".
                    path_kill (str, optional): Path to kill. Defaults to "kill".
                    path_sh (str, optional): Path to sh. Defaults to "sh".
                    path_printf (str, optional): Path to printf. Defaults to "printf".
                    path_wm (str, optional): Path to wm. Defaults to "wm".
                    path_tail (str, optional): Path to tail. Defaults to "tail".
                    path_sed (str, optional): Path to sed. Defaults to "sed".
                    path_su (str, optional): Path to su. Defaults to "su".
                    path_pm (str, optional): Path to pm. Defaults to "pm".
                    path_tmp_folder (str, optional): Path to temporary folder. Defaults to "/sdcard/_lgcattmp".
                    screen_width (int, optional): Screen width. Defaults to 0.
                    screen_height (int, optional): Screen height. Defaults to 0.
                    sleep_logcat (int, optional): Sleep time for logcat. Defaults to 1.
                    kwargs_subprocess (dict, optional): Subprocess kwargs. Defaults to None.
                    thread_daemon (bool, optional): Whether the thread is a daemon. Defaults to True.
                    buffer_stdout (int, optional): Buffer size for stdout. Defaults to 10000.
                    buffer_stderr (int, optional): Buffer size for stderr. Defaults to 10000.
                    search_string (bytes, optional): Search string for logcat. Defaults to b"add(".
                    refresh_screen_add_width (int, optional): Additional width for screen refresh. Defaults to 0.
                    refresh_screen_add_height (int, optional): Additional height for screen refresh. Defaults to 1.
                Example:
                    from logaccessparse import LogCatParser
                    import time
                    import shutil
                    logadb = LogCatParser(
                        #adb_path=shutil.which("adb.exe"),
                        adb_path=None,
                        device_serial="127.0.0.1:5625",
                        path_logcat="logcat",
                        path_top="top",
                        path_grep="grep",
                        path_awk="awk",
                        path_kill="kill",
                        path_sh="sh",
                        path_printf="printf",
                        path_wm="wm",
                        path_tail="tail",
                        path_sed="sed",
                        path_su="su",
                        path_pm="pm",
                        path_tmp_folder="/sdcard/_lgcattmp",
                        screen_width=0,
                        screen_height=0,
                        sleep_logcat=1,
                        kwargs_subprocess=None,
                        thread_daemon=True,
                        buffer_stdout=10000,
                        buffer_stderr=10000,
                        search_string=b"add(",
                        refresh_screen_add_width=0,
                        refresh_screen_add_height=1,
                    )
                    #logadb.install_apk()
                    #input("Press Enter to continue...")
                    logadb.save_sh_command_to_disk().run_pause_logcat_script().start_logcat_subprocess().run_logcat_script().clear_stderr_stdout().clear_cache()

                    try:
                        while True:
                            counter = 0
                            while logadb.stdout_buffer:
                                element = logadb.stdout_buffer.pop()
                                if "null" not in element["text"] and element["visible"]:
                                    print(element["text"])
                                    print(element["boundsInScreen"])
                                    print(element)
                                counter += 1
                            if counter == 0:
                                logadb.run_update_screen_script()
                                time.sleep(1)
                            else:
                                time.sleep(0.1)
                            print(counter)
                    except KeyboardInterrupt:
                        try:
                            time.sleep(1)
                        except Exception:
                            pass
                    logadb.kill_all_subprocesses()

        """
        self.refresh_screen_add_width = refresh_screen_add_width
        self.refresh_screen_add_height = refresh_screen_add_height
        self.kwargs_subprocess = kwargs_subprocess
        if not self.kwargs_subprocess:
            self.kwargs_subprocess = {}
        self.adb_path = adb_path
        self.device_serial = device_serial
        self.path_logcat = path_logcat
        self.path_top = path_top
        self.path_grep = path_grep
        self.path_awk = path_awk
        self.path_kill = path_kill
        self.path_sh = path_sh
        self.path_printf = path_printf
        self.path_wm = path_wm
        self.path_tail = path_tail
        self.path_sed = path_sed
        self.path_su = path_su
        self.path_pm = path_pm
        self.path_tmp_folder = "/" + path_tmp_folder.strip(" /")
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sleep_logcat = sleep_logcat
        self.thread_daemon = thread_daemon
        self.stdout_buffer = deque([], buffer_stdout)
        self.stderr_buffer = deque([], buffer_stderr)
        self._cache_dict = {}
        self.search_string = search_string
        self.apk_path = get_short_path_name(
            os.path.normpath(os.path.join(os.path.dirname(__file__), "ac.apk"))
        )

        if not self.adb_path:
            self.subprocess_command = self.path_sh
            self.install_cmd = [self.path_pm, "install", "-g", self.apk_path]

        else:
            self.adb_path = get_short_path_name(self.adb_path)
            self.subprocess_command = [
                self.adb_path,
                "-s",
                self.device_serial,
                "shell",
            ]
            self.install_cmd = [
                self.adb_path,
                "-s",
                self.device_serial,
                "install",
                "-g",
                self.apk_path,
            ]
        add_sleep = f"sleep {self.sleep_logcat}" if self.sleep_logcat else ""
        ###########################################################
        self.script_logcat_cmd_path = f"{self.path_tmp_folder}/startlcat.sh"
        self.script_start_logcat = (
            f"{self.path_sh} {self.script_logcat_cmd_path}".encode()
        )
        self.script_logcat_cmd = f"""
mkdir -p {self.path_tmp_folder}
{self.path_printf} "%s\n" '{self.path_logcat} -c\nwhile true; do
    {self.path_logcat } -v raw -d -e "AccessibilityNodeInfo@" 
    {self.path_logcat } -c
    {add_sleep}
done' > {self.script_logcat_cmd_path}
""".encode()
        ###########################################################
        if not self.screen_width or not self.screen_height:
            self.script_refresh_screen_cmd = f"""resolution="$({self.path_wm} size | {self.path_tail} -n1 | {self.path_grep} -oE "[[:digit:]]+x[[:digit:]]+")"
newres="$({self.path_printf} "%s"  "$resolution" | {self.path_sed} 's/.$/1/')"
{self.path_wm} size "$newres" && {self.path_wm} size "$resolution"
    """.encode()
        else:
            self.script_refresh_screen_cmd = f"""{self.path_wm} size {self.screen_width+self.refresh_screen_add_width}x{self.screen_height+self.refresh_screen_add_height} && {self.path_wm} size {self.screen_width}x{self.screen_height}""".encode()
        ###########################################################
        self.script_pause_logcat = f"""{self.path_su}\n{self.path_top} -b -n1 | {self.path_grep} "{self.path_logcat }" | {self.path_grep} -v "grep" | {self.path_awk} '{{$1=$1}}1' | {self.path_awk } '{{print "{self.path_kill} -STOP " $1}}' | {self.path_sh}""".encode()
        ###########################################################
        self.script_kill_logcat = f"""{self.path_su}\n{self.path_top} -b -n1 | {self.path_grep} "startlcat.sh" | {self.path_grep}  -v "grep" | {self.path_awk} '{{$1=$1}}1' |  {self.path_awk} '{{print "{self.path_kill} -9 " $1}}' | {self.path_sh}""".encode()

        self._t1 = None
        self._t2 = None
        self._proc = None

    def install_apk(self):
        """
        Install the APK.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        subprocess.run(
            self.install_cmd,
            **{
                **invisibledict,
                **self.kwargs_subprocess,
            },
        )
        self._subprocess_run(
            cmd="""settings put secure accessibility_button_targets 
settings put secure accessibility_display_inversion_enabled 0
settings put secure accessibility_display_magnification_enabled 0
settings put secure accessibility_display_magnification_scale 2.0
settings put secure accessibility_enabled 1
settings put secure accessibility_shortcut_target_service com.microsoft.accessibilityinsightsforandroidservice/com.microsoft.accessibilityinsightsforandroidservice.AccessibilityInsightsForAndroidService
settings put secure enabled_accessibility_services com.microsoft.accessibilityinsightsforandroidservice/com.microsoft.accessibilityinsightsforandroidservice.AccessibilityInsightsForAndroidService:com.microsoft.accessibilityinsightsforandroidservice/microsoft.accessibilityinsightsforandroidservice.AccessibilityInsightsForAndroidService""".encode(),
        )
        return self

    def clear_cache(self):
        """
        Clear the cache.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._cache_dict.clear()
        return self

    def clear_stderr_stdout(self):
        """
        Clear the stderr and stdout buffers.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self.stderr_buffer.clear()
        self.stdout_buffer.clear()
        return self

    def _subprocess_run(self, cmd):
        """
        Run a subprocess command.

        Args:
            cmd (bytes): The command to run.
        """
        subprocess.run(
            self.subprocess_command,
            input=cmd,
            **{
                **invisibledict,
                **self.kwargs_subprocess,
            },
        )

    def save_sh_command_to_disk(self):
        """
        Save the shell command to disk.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._subprocess_run(self.script_logcat_cmd)
        return self

    def start_logcat_subprocess(self):
        """
        Start the logcat subprocess.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._proc = subprocess.Popen(
            self.subprocess_command,
            **{
                "bufsize": 0,
                **invisibledict,
                **self.kwargs_subprocess,
                "stdout": subprocess.PIPE,
                "stdin": subprocess.PIPE,
                "stderr": subprocess.PIPE,
            },
        )
        self._t1 = threading.Thread(
            target=self._capture_stdout, daemon=self.thread_daemon
        )
        self._t2 = threading.Thread(
            target=self._capture_stderr, daemon=self.thread_daemon
        )
        self._t1.start()
        self._t2.start()
        return self

    def _capture_stdout(self):
        """
        Capture stdout from the subprocess.
        """
        try:
            for l in iter(self._proc.stdout.readline, b""):
                if self.search_string in l:
                    try:
                        self.stdout_buffer.append(
                            self._cache_dict.setdefault(l, splitlinesregex(l))
                        )
                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)

    def _capture_stderr(self):
        """
        Capture stderr from the subprocess.
        """
        try:
            for l in iter(self._proc.stderr.readline, b""):
                self.stderr_buffer.append(l)

        except Exception as e:
            print(e)

    def stdin_write(self, cmd):
        """
        Write a command to stdin of the subprocess.

        Args:
            cmd (str | bytes): The command to write.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        if isinstance(cmd, str):
            cmd = cmd.encode()
        self._proc.stdin.write(cmd + b"\n")
        self._proc.stdin.flush()
        return self

    def run_logcat_script(self):
        """
        Run the logcat script.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self.stdin_write(self.script_start_logcat)
        return self

    def run_update_screen_script(self):
        """
        Run the screen update script.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._subprocess_run(self.script_refresh_screen_cmd)
        return self

    def run_kill_logcat_script(self):
        """
        Run the script to kill the logcat process.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._subprocess_run(self.script_kill_logcat)
        return self

    def run_pause_logcat_script(self):
        """
        Run the script to pause the logcat process.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        self._subprocess_run(self.script_pause_logcat)
        return self

    def kill_all_subprocesses(self):
        """
        Kill all subprocesses.

        Returns:
            LogCatParser: The LogCatParser object.
        """
        try:
            self.run_kill_logcat_script()
        except Exception as e:
            print(e)
        try:
            self.stdin_write(b"exit\n")
        except Exception as e:
            print(e)
        try:
            self._proc.stdin.close()
        except Exception as e:
            print(e)
        try:
            self._proc.stdout.close()
        except Exception as e:
            print(e)
        try:
            self._proc.stderr.close()
        except Exception as e:
            print(e)
        try:
            self._proc.kill()
        except Exception as e:
            print(e)
        try:
            _killthread(self._t1)
        except Exception as e:
            print(e)
        try:
            _killthread(self._t2)
        except Exception as e:
            print(e)
        return self
