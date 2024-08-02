# Accessibility parser for Android

### Tested against Windows 10 / Python 3.11 / Anaconda 

### pip install logaccessparse

```PY

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
```