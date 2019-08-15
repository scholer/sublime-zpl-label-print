# Copyright 2019, Rasmus Sorensen <rasmusscholer@gmail.com>

"""


How to print:
--------------


Sublime Text does not natively support printing.

There are other, platform-specific ways of printing,
e.g. using the `print` command on Windows, and using `lp` on Linux and macOS.

How to see available printers on Windows:

    wmic printer list brief
    wmic printer get name

Use `lpq` to display the status of a print queue on a computer running Line printer Daemon (LPD).

    lpq -S <server> -P <printer>


To capture/redirect all printed output to file:

* Go Printer properties -> Ports -> Add port -> Local port -> New Port -> Enter filename.
* https://stackoverflow.com/questions/13586865/get-zpl-code-from-zebra-designer



### Prior art related to printing:

* SublimePrint,
    * https://github.com/svenax/SublimePrint
    * Uses a settings-defined command to print (but expects something like `lp`).
    * Uses `lpstat` to list printers.

* QuickPrint
    * https://packagecontrol.io/packages/QuickPrint
    * https://github.com/agibsonsw/QuickPrint
    * Uses a user-defined command to print (e.g. notepad).
    * Expects the printer to be shared using `net use LPT1 \\hostname\printer_name /persistent:yes`

* LPrint
    * Uses lp/lpstat to print. (So only for Linux and maybe macOS).

"""

import sublime
import sublime_plugin
import sys
import os
from pprint import pformat

from .labelprint.datareader import data_from_csv_content
from .labelprint.zpl import generate_zpl, check_forbidden_characters_in_data, DEFAULT_ZPL_PRINTER_CONFIG, FORBIDDEN_CHARS
from .labelprint.windows_printing import print_content


DEFAULT_PRINT_METHOD = 'print-cmd'


def get_merged_selection(view, sep=""):
    return sep.join(view.substr(region) for region in view.sel())


class PrintDataZplLabelsCommand(sublime_plugin.WindowCommand):

    def run(self):
        # self.view.insert(edit, 0, "Hello, World!")
        s = sublime.load_settings("ZplLabelPrint.sublime-settings")


class PrintZplLabelsFromCsvContentCommand(sublime_plugin.TextCommand):
    """ Command to print one or more ZPL labels using csv content in the current View.

    print_zpl_labels_from_csv_content

    Callable with:
        sublime.run_command("print_zpl_labels_from_csv_content")
    """

    def run(
            self, edit,
            source="selection", sep=None, fieldnames=None, strip_whitespace=None,
            label_template_file=None, printerconfig_zpl=None, printerconfig_zpl_file=None,
            save_to_file=None, do_print=None, printer=None, print_method=None,
            verbose=None):
        """"""
        # self.view.insert(edit, 0, "Hello, World!")
        s = sublime.load_settings("ZPL-Label-Print.sublime-settings")  # Settings name is case-sensitive.
        if sep is None:
            sep = s.get("sep", ",")
        if fieldnames is None:
            fieldnames = s.get("fieldnames", None)
        if label_template_file is None:
            label_template_file = s.get("label_template_file")
        if label_template_file is None:
            raise ValueError("`label_template_file` MUST be specified, "
                             "either in plugin settings or as function parameter."
                             "Please update `label_template_file` in your user settings.")
        else:
            label_template = open(os.path.expanduser(label_template_file)).read()
        if printerconfig_zpl is None:
            printerconfig_zpl_file = s.get("printerconfig_zpl_file")
            if printerconfig_zpl_file:
                printerconfig_zpl = open(os.path.expanduser(printerconfig_zpl_file)).read()
            else:
                printerconfig_zpl = s.get("printerconfig_zpl", DEFAULT_ZPL_PRINTER_CONFIG)
        data_forbidden_chars = s.get("data_forbidden_chars", FORBIDDEN_CHARS)
        if strip_whitespace is None:
            strip_whitespace = s.get("strip_whitespace", False)
        if save_to_file is None:
            save_to_file = s.get("save_to_file")
        if do_print is None:
            do_print = s.get("do_print", False)
        if printer is None:
            printer = s.get("printer")
        if print_method is None:
            print_method = s.get("print_method")
        if verbose is None:
            verbose = s.get("verbose", 1)
        print("verbose:", verbose)

        if source == "selection":
            text_content = get_merged_selection(self.view, sep="\n")
            if not text_content:
                print("Selected text content is '%s'; aborting label print..." %(text_content,))
                return
        elif source == "current_view_buffer":
            text_content = self.view.substr(sublime.Region(0, self.view.size()))
            if not text_content:
                print("Buffer text content is '%s'; aborting label print..." %(text_content,))
                return
        elif source == "clipboard":
            text_content = sublime.get_clipboard()
            if not text_content:
                print("Buffer text content is '%s'; aborting label print..." % (text_content,))
                return
        else:
            print("`source` parameter value '%s' not recognized; aborting label print!" % (source,))
            return
        if verbose:
            print("Loaded %s chars from source %s" % (len(text_content), source))
        eol_char = self.view.line_endings()
        if verbose:
            print("Parsing data from %s text characters using fieldnames %s ..." % (len(text_content), fieldnames))
        data = data_from_csv_content(text_content, sep=sep, fieldnames=fieldnames, eol_char=eol_char)
        if verbose:
            print(" - %s rows of data entries parsed!" % (len(data), ))

        if strip_whitespace:
            if verbose:
                print("Stripping leading/trailing whitespace from fieldnames and values...", file=sys.stderr)
            data = [{key.strip(): val.strip() if isinstance(val, str) else val for key, val in row.items()}
                    for row in data]

        # Check the data for forbidden characters:
        check_forbidden_characters_in_data(data, do_raise=True, forbidden_chars=data_forbidden_chars)

        zpl_content = generate_zpl(data, label_template=label_template, printconfig=printerconfig_zpl)

        if verbose:
            print("\nZPL content generated OK (%s byte characters)." % (len(zpl_content),), file=sys.stderr)

        if save_to_file:
            if save_to_file == "-":
                print("Writing zpl content to stdout...", file=sys.stderr)
                sys.stdout.write(zpl_content)
            else:
                with open(os.path.expanduser(save_to_file), 'w') as f:
                    print("Writing zpl content to file", os.path.expanduser(save_to_file),
                          "...", file=sys.stderr)
                    f.write(zpl_content)

        if do_print:
            if verbose:
                print("Printing zpl content to printer {} using method {} ...".format(
                    printer, print_method
                ), file=sys.stderr)
            if not printer:
                raise ValueError("`printer` MUST be specified in order to print, "
                                 "either in plugin settings or as function parameter.")
            print_content(zpl_content, printer=printer, method=print_method, verbose=verbose)

        return zpl_content


print("ZPL-Label-Print package loaded!")
