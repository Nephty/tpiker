# tpiker

## Description

tpiker is a Python theme picker tool.

It consists of two components :

- A Python base that allows for theme switching operations and
- A terminal user interface built with [Textualize](https://github.com/Textualize).

tpiker uses a themes directory structured in this way :

```
themes
├── theme_A
│   ├── configuration_for_program_A
│   │   └── ...
│   └── configuration_for_program_B
│       └── ...
└── theme_B
    ├── configuration_for_program_A
    │   └── ...
    └── configuration_for_program_B
        └── ...
```

Your themes directories contain all your themes. Each theme contains directories. Each directory corresponds to one program. These directories contain the actual configuration of the program. These directories can be named anything since we are copying the content of these directories and not the directories themselves. The only restriction is that **their name must be consistent throughout the different themes**.

## Usage

If you want to create two themes `pirate` and `viking` in order to save two configurations for kitty, you would end up with something like :

```
themes
├── pirate
│   └── kitty_configuration <-- doesn't have to be named 'kitty'
│       └── kitty.conf <-- actual configuration (name matters)
└── viking
    └── kitty_configuration <-- doesn't have to be named 'kitty'
       └── kitty.conf <-- actual configuration (name matters)
```

If you want to apply your `viking` theme, specify it in your configuration file :

```
# Note the trailing slash :
themes_directory=/path/to/your/themes/
```

Then, create a `Config` object in `tpiker.py` :

```
KITTY_CONFIG = Config('/path/to/your/.config/kitty', 'kitty_configuration')
```

This links the live Kitty configuration to the configuration defined in your themes. This definition is the reason why the names of the directories containing each kitty configuration file must be the same.

Finally, to apply one of your themes to Kitty, call the `apply` method on your `Config` object with the desired theme :

```
KITTY_CONFIG.apply('viking')
```

You can also use the target theme of the configuration file :

```
KITTY_CONFIG.apply(TARGET_THEME) # TARGET_THEME is already defined from the configuration file
```

## Installation and set up

1. Clone the repository : `git clone git@github.com:Nephty/tpiker.git`
2. Create a directory that will contain your themes
3. Set up your configuration in `tpicker.conf` :
   - Set the themes directory location : `themes_directory=/path/to/your/themes/` (note the trailing slash)
   - Set a target theme : `target_theme=your_desired_theme`
4. Run the tpiker.py file with your modifications : `python tpiker.py` (see Usage)

The current usage is not optimal and will be modified later in order to use a configuration file to define the `Config` objects.

## Backups

Remember that it is always good practice to have backups of your system. Tpiker cannot be held responsible for any file loss.

In any case, there is a small backup system that will copy the current configuration to `/tmp/tpiker_backups/path/to/your/files` before overwriting the live configuration. This small save procedure is used at each call to the `apply` method.