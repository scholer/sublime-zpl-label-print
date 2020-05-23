
"""

The purpose of this script it to generate all the "Print ZPL label(s)" commands listed in the `ZPL-Label-Print.sublime-commands` file.

Generate with:

    > python generate_sublime_commands.py > ZPL-Label-Print.sublime-commands

OBS: Sublime Text looks for `.sublime-commands` files *recursively* in plugin folders.
If you see duplicate commands, make sure you only have one copy of the `ZPL-Label-Print.sublime-commands` file.

"""

import json


def generate_sublime_commands(
        caption_fmt="Print ZPL label(s) using {sep}-separated values from {source} ({fieldnames}).",
        command="print_zpl_labels_from_csv_content",
    ):

    source_opts = {
        "selection": "SELECTED TEXT",
        "clipboard": "CLIPBOARD",
        "current_view_buffer": "the ENTIRE FILE/buffer", 
    }

    sep_opts = {
        "\t": "TAB",
        ",": "COMMA",
        None: "SETTINGS-DEFINED CUSTOM",
    }

    fieldnames_opts = {
        None: "first line is header with fieldnames",
        "settings-defined": "no header; use header defined in settings",
    }

    sublime_commands = [
        {
            "caption": caption_fmt.format(source=source_desc, sep=sep_desc, fieldnames=fieldnames_desc),
            "command": command,
            "args": {"source": source, "sep": sep, "fieldnames": fieldnames}
        }
        for source, source_desc in source_opts.items()
        for sep, sep_desc in sep_opts.items()
        for fieldnames, fieldnames_desc in fieldnames_opts.items()
    ]

    commands_str = json.dumps(sublime_commands, sort_keys=False, indent=4)
    print(commands_str)



if __name__ == "__main__":
    generate_sublime_commands()
