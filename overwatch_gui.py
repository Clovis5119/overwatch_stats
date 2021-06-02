import tkinter as tk


class OverwatchGUI:
    """
    Handles GUI assembly and most of the logic related to the user
     interacting with the interface.

    The class must be passed the main OverwatchStatsManager object to access
     all attributes necessary for dynamically updating the GUI.

    Two methods should be called before launching the GUI loop:
     - boot_gui()
     - fill_starting_content()

    boot_gui() does most of the work by calling all of the necessary methods
     that create, position, and style the GUI's widgets.
    It could also call fill_starting_content(), but separating them allows
     us to fill the content after mainloop() has started, which is cooler.

    TODO: Turn popdown entry boxes into their own objects.
    """

    def __init__(self, main_program):
        """
        Initializes attributes used throughout the class. Only the attributes
         from other classes (passed via the main program) are actually given
         values at this stage, as well as the root Tk() window
        """

        # Still working on which objects and attributes are needed.
        self.main = main_program
        self.files = main_program.files
        self.owh = main_program.owh

        self.players = {}
        self.heroes = []
        self.platforms = ['pc', 'etc']
        self.regions = ['us', 'eu', 'asia']
        self.api = main_program.api

        # Instantiate the root Tk() window and the x/y variables that will
        #  be used to support the user moving the window.
        self.window = tk.Tk()
        self._offsetx = 0
        self._offsety = 0

        # These will hold the three main panels: Profiles, Heroes, Stats.
        self.panel_prof = None
        self.panel_hero = None
        self.panel_stat = None

        # Container for the three main panels to shorten code later on.
        self.panels = None

        # Attributes for widgets placed outside the main panels.
        self.alert = None
        self.run = None
        self.close = None
        self.stat_menu = None
        self.top_bar = TopBar(self.window)

        # Flag to support stat options menu behavior.
        self.hero_box_empty = True

        # Flags for box height adjustments. TODO: Implement these.
        self.prof_ent_add_exists = False
        self.hero_ent_add_exists = False
        self.box_height_adjusted = False

    def boot_gui(self):
        """Calls all of the methods responsible for instantiating, placing,
        and configuring GUI widgets."""
        self._instantiate_main_widgets()
        self._config_main_window()
        self._create_panel_widgets()
        self._place_widgets()
        self._set_widget_commands()
        self._cmd_toggle_checkbox_quickplay()

        self.alert.print("GUI boot successful!")
        self.alert.print("...")
        self.alert.print("...")

    def fill_starting_content(self):
        """Initializes starting content in each panel's listbox."""

        # If player info is already on file, try adding the profile to the box.
        if players := self.files.get_saved_players():
            for tag, info in players.items():
                self._add_players_to_box(tag, info['platform'], info['region'])

        # Fill the hero box with the starting preset, then update the
        #  API-compatible list of currently selected heroes.
        self._cmd_add_preset_heroes()

        # Fill the stat box with the starting preset.
        self._update_stat_menu_options()

    def _instantiate_main_widgets(self):
        """
        Initializes the three main panels (Profiles, Heroes, Stats) as well
         as the other major widgets attached to the main window rather than
         to those panels (AlertBox, RunButton, ExitButton).
        """

        # The three main panels.
        self.panel_prof = InterfacePanel(panel_type='profile')
        self.panel_hero = InterfacePanel(panel_type='hero')
        self.panel_stat = InterfacePanel(panel_type='stat')
        self.panels = {self.panel_prof: 'profile',
                       self.panel_hero: 'hero',
                       self.panel_stat: 'stat'}

        # Widgets outside the main panels.
        self.alert = AlertBox(self.window)
        self.run = RunButton(self.window)
        self.info = self.top_bar.info
        self.close = self.top_bar.close

        self.alert.print("Instantiated main panels and widgets.")

    def _config_main_window(self):
        """Set the root Tk() window parameters."""

        def _cmd_click_window(event):
            """Honestly, I just copied this from someone else."""
            self._offsetx = event.x + event.widget.winfo_rootx() - self.window.winfo_rootx()
            self._offsety = event.y + event.widget.winfo_rooty() - self.window.winfo_rooty()

        def _cmd_drag_window(event):
            """Move the window when it is being dragged."""
            x = self.window.winfo_pointerx() - self._offsetx
            y = self.window.winfo_pointery() - self._offsety
            self.window.geometry(f"+{x}+{y}")

        self.window.title("Overwatch Stat Comparison Tool")
        self.window.resizable(0, 0)
        self.window.overrideredirect(True)

        # Bind mouse clicks and movement for moving the window.
        self.window.bind('<Button-1>', _cmd_click_window)
        self.window.bind('<B1-Motion>', _cmd_drag_window)

        # Size configuration.
        self.window.rowconfigure(0, minsize=30)
        self.window.rowconfigure(1, minsize=510)
        self.window.rowconfigure(2, minsize=0)
        self.window.rowconfigure(3, minsize=50)
        self.window.columnconfigure([0, 2, 4], minsize=300)
        self.window.columnconfigure([1, 3], minsize=0)

        # Makes the window box transparent.
        self.window.config(background='#53560d')
        self.window.wm_attributes("-transparentcolor", "#53560d")

        self.alert.print("Configured main GUI window.")

    def _create_panel_widgets(self):
        """
        Create the widgets that are contained within the three main panels.
        These are all instantiated as attributes of the panels rather than
        attributes of OverwatchGUI, except for the STAT panel's dropdown menu.
        """

        # Create the widgets that are identical across panels.
        for panel in self.panels:
            panel.create_main_frame(self.window)
            panel.create_header()
            panel.create_frm_button()
            panel.create_listbox()
            panel.create_description()

        # Create the buttons for the PROFILES panel.
        self.panel_prof.create_btn_add()
        self.panel_prof.create_btn_del()
        self.panel_prof.create_btn_save()

        # Create the buttons for the HEROES panel.
        self.panel_hero.create_btn_add()
        self.panel_hero.create_btn_del()
        self.panel_hero.create_drop_heroes(self.owh.get_role_list())
        self.panel_hero.create_btn_clear()

        # Create the checkboxes for the STATS panel.
        self.panel_stat.create_checkbox_quickplay()
        self.panel_stat.create_checkbox_comp()

        # Create the dropdown menu for the STATS panel. It's special.
        self.stat_menu = DropdownMenu(
            self.panel_stat.frm_btn, 'average', self.api.menu_options)

        self.alert.print("Created the panel-contained widgets.")

    def _place_widgets(self):
        """Position the GUI elements within their respective grids.
        TODO: Use RadioButton widget for checkboxes?
        TODO: Implement Scrollbar and use PanedWindows?"""

        # Frames inside the main GUI window.
        self.top_bar.bar.grid(row=0, column=4, sticky='nsew')
        self.panel_prof.frm.grid(row=1, column=0, sticky='nsew')
        self.panel_hero.frm.grid(row=1, column=2, sticky='nsew')
        self.panel_stat.frm.grid(row=1, column=4, sticky='nsew')

        # Widgets that are identical across panels.
        for panel in self.panels:
            panel.header.grid(
                row=0, column=0, sticky='snew')
            panel.frm_btn.grid(
                row=1, column=0, sticky='snew')
            panel.box.grid(
                row=3, column=0, sticky='snew', padx=10, pady=(10, 0))
            panel.description.grid(
                row=4, column=0, sticky='ns', pady=10)

        # Buttons in the PROFILE panel's button frame.
        self.panel_prof.btn_add.grid(
            row=0, column=0, sticky='w', pady=(7, 0), padx=(10, 0))
        self.panel_prof.btn_del.grid(
            row=0, column=1, sticky='w', pady=(7, 0))
        self.panel_prof.btn_save.grid(
            row=0, column=3, sticky='e', pady=(7, 0), padx=(0, 10))

        # Buttons in the HERO panel's button frame.
        self.panel_hero.btn_add.grid(
            row=0, column=0, sticky='w', pady=(7, 0), padx=(10, 0))
        self.panel_hero.btn_del.grid(
            row=0, column=1, sticky='w', pady=(7, 0))
        self.panel_hero.drp_hero.grid(
            row=0, column=2, padx=(0, 10), pady=(7, 0))
        self.panel_hero.btn_clear.grid(
            row=0, column=3, sticky='e', pady=(7, 0), padx=(0, 10))

        # Checkboxes in the STAT panel's button frame.
        self.panel_stat.chk_qp.grid(
            row=0, column=0, sticky='w', pady=(7, 0), padx=(10, 7))
        self.panel_stat.chk_cp.grid(
            row=0, column=1, sticky='w', pady=(7, 0))

        # Dropdown menu in the STAT panel's button frame.
        self.stat_menu.menu.grid(row=0, column=3, pady=(7, 0), padx=(0, 10))
        self.stat_menu.menu.config(width=13)

        # Other widgets attached to direction to the root window.
        self.close.pack(side=tk.RIGHT)
        self.info.pack(side=tk.RIGHT)
        self.alert.box.grid(row=3, column=0, columnspan=3, sticky='nsew')
        self.run.button.grid(row=3, column=4, sticky='nsew')

        self.alert.print("Nudged widgets into place.")

    def _set_widget_commands(self):
        """Pair commands to GUI elements the user can interact with."""

        # Widgets in the PROFILES frame.
        self.panel_prof.btn_add.config(command=lambda: self._parse_cmd_add('profile'))
        self.panel_prof.btn_del.config(command=self._cmd_delete_selected_profiles)
        self.panel_prof.btn_save.config(command=self._cmd_save_players)

        # Widgets in the HEROES frame.
        self.panel_hero.btn_add.config(command=lambda: self._parse_cmd_add('hero'))
        self.panel_hero.btn_del.config(command=self._cmd_del_selected_heroes)
        self.panel_hero.var_preset_heroes.trace('w', self._cmd_add_preset_heroes)
        self.panel_hero.btn_clear.config(command=self._cmd_clear_heroes)

        # Widgets in the STATS frame.
        self.panel_stat.chk_qp.config(command=self._cmd_toggle_checkbox_quickplay)
        self.panel_stat.chk_cp.config(command=self._cmd_toggle_checkbox_comp)
        # Keep in mind this runs every time the display text changes.
        self.stat_menu.var_list.trace('w', self._cmd_add_preset_stats)
        self.panel_stat.box.bind('<<ListboxSelect>>', self._check_run_state)

        # Other widgets.
        self.close.config(command=self.main.cmd_quit)
        self.info.config(command=self._cmd_info)
        self.run.button.config(command=self.main.cmd_run_stats)

        self.alert.print("Paired widgets to commands.")

    def _add_players_to_box(self, tag, platform, region):
        """
        Attempts to get a profile corresponding to the provided user info.
        If successful, adds the player to the PROF listbox and updates the
         player list for future saving.
        """
        if self.main.get_profile(tag, platform, region):
            self.panel_prof.box.insert(0, tag)
            self.players[tag] = [platform, region]

            self._check_run_state()

    def _update_stat_menu_options(self):
        """Update the stats options menu."""

        # Get new menu options from the API object.
        new_options = self.api.get_new_stat_menu_presets(self.heroes)

        # If the HERO box is empty, disable STAT menu options.
        if self.panel_hero.box.size() == 0:
            self.stat_menu.clear_options()
            self.hero_box_empty = True

        # If the HERO box's previous state was empty, reset STAT menu
        #  preset to the default (typically 'average').
        elif self.hero_box_empty:
            self.stat_menu.set_new_options(new_options, reset=True)
            self.hero_box_empty = False

        # Update the STAT menu options.
        else:
            self.stat_menu.set_new_options(new_options)
            self.hero_box_empty = False

        # self._cmd_add_preset_stats()

    def _check_run_state(self, *args):
        """
        Enables the RUN button if all the following conditions are satisfied:
         - At least one valid profile has been added.
         - At least one valid hero has been added.
         - An available stat type has been selected.
        """
        active_profiles = True if self.players else False
        active_heroes = True if self.heroes else False
        active_stat = True if self.panel_stat.box.curselection() else False

        if active_profiles and active_heroes and active_stat:
            self.run.enable()
        else:
            self.run.disable()

    def _cmd_info(self):
        """Bring up a window with some helpful information on using the GUI."""
        self.alert.print("Sorry, this doesn't do anything yet.")

    def _parse_cmd_add(self, add_type):
        """
        This in-between method destroys the entry widget that pops down
         when a user clicks an ADD button - if the widget already exists.
        If the widget doesn't already exist, it calls the relevant methods
         for accepting the user's input.
        """

        # Destroy ADD PROFILE entry box if it already exists.
        if add_type == 'profile' and self.prof_ent_add_exists:
            self.panel_prof.frm.grid_slaves()[0].destroy()
            self.prof_ent_add_exists = False
        # Create ADD PROFILE entry box if it doesn't already exist.
        elif add_type == 'profile':
            self._cmd_add_player()
            self.prof_ent_add_exists = True

        # Destroy ADD HERO entry box if it already exists.
        if add_type == 'hero' and self.hero_ent_add_exists:
            self.panel_hero.frm.grid_slaves()[0].destroy()
            self.hero_ent_add_exists = False
        # Create ADD HERO entry box if it doesn't already exist.
        elif add_type == 'hero':
            self._cmd_add_hero()
            self.hero_ent_add_exists = True

        # TODO: Algorithm that adjusts box height when popdown(s) (dis)appear.
        """
        if self.box_height_adjusted and (
                self.prof_ent_add_exists or self.hero_ent_add_exists):
            pass
        elif self.prof_ent_add_exists or self.hero_ent_add_exists:
            self.stat.box.config(height=self.stat.box['height'] + 1)
            self.box_height_adjusted = True
        elif self.box_height_adjusted:
            self.stat.box.config(height=self.stat.box['height'] - 1)
            self.box_height_adjusted = False
        """

    def _cmd_add_player(self):
        """Create a pop-down entry line for the user to enter a new profile."""

        def enter_event(*args):
            """Add the requested player."""
            tag = ent_prof.get()
            platform = drp_platform.var_list.get()
            region = drp_region.var_list.get()

            if tag in self.players:
                self.alert.print("You've already added this profile.",
                                 style='warn')

            self._add_players_to_box(tag, platform, region)
            ent_prof.delete(0, tk.END)

        # Create and place a frame to which to attach the entry and dropdowns.
        self.panel_prof.create_frm_entry()
        self.panel_prof.frm_entry.grid(row=2, column=0, sticky='new', pady=(10, 0))
        self.panel_prof.frm_entry.config(background="#1D9367")

        # Create the entry and dropdown objects.
        ent_prof = tk.Entry(self.panel_prof.frm_entry)
        drp_platform = DropdownMenu(
            self.panel_prof.frm_entry, self.platforms[0], self.platforms)
        drp_region = DropdownMenu(
            self.panel_prof.frm_entry, self.regions[0], self.regions)

        # Place the entry and dropdown objects.
        ent_prof.grid(row=0, column=0, sticky='swen', padx=10)
        drp_platform.menu.grid(row=0, column=1, sticky='w')
        drp_region.menu.grid(row=0, column=2, sticky='w', padx=(5, 10))

        # Bind the ENTER key to a method and give the widget focus.
        ent_prof.bind('<Return>', enter_event)
        ent_prof.focus_set()

    def _cmd_delete_selected_profiles(self):
        """Deletes user-selected profiles line by line in reverse order,
        and removes them from the active player list."""
        for i in self.panel_prof.box.curselection()[::-1]:
            player = self.panel_prof.box.get(i)
            self.panel_prof.box.delete(i)
            self.players.pop(player, None)

            self.alert.print(f"Removed '{player}' from selected players.")

        self._check_run_state()

    def _cmd_save_players(self):
        """Write the current list of players to file so they don't have
        to be added manually the next time the user launches the program."""
        self.files.save_players(self.players)
        self.alert.print(f"Player list has been saved.")

    def _cmd_add_hero(self):
        """Create a pop-down entry line for the user to enter a new hero.
        TODO: Separate the entry creation part to a new object.
        """

        def enter_event(*args):
            """Check the user's input and add the hero if valid."""
            new_hero = self.owh.get_proper_name(ent_hero.get())
            ent_hero.delete(0, tk.END)

            if new_hero is False:
                self.alert.warn("Please enter a valid hero name")
            elif new_hero in self.heroes:
                self.alert.warn(f"Hero '{new_hero}' has already been added")
            elif new_hero:
                self.panel_hero.box.insert(0, new_hero)
                self.heroes.append(new_hero)
                self.alert.print(f"'{new_hero}' has been added to the hero pool.")

                self._update_stat_menu_options()

        # Create or destroy the entry box depending on whether it already exists.
        ent_hero = tk.Entry(self.panel_hero.frm)
        ent_hero.grid(
            row=2, column=0, sticky='ew', pady=(10, 0), padx=10, ipady=4)
        ent_hero.bind('<Return>', enter_event)
        ent_hero.focus_set()

    def _cmd_del_selected_heroes(self):
        """Deletes user-selected heroes line by line in reverse order, and
        removes them from the API-compatible hero list."""
        for i in self.panel_hero.box.curselection()[::-1]:
            lost_hero = self.panel_hero.box.get(i)
            self.heroes.remove(lost_hero)
            self.panel_hero.box.delete(i)
            self.alert.print(f"Goodbye, {lost_hero}.")

        self._update_stat_menu_options()

    def _cmd_add_preset_heroes(self, *args):
        """Wipes the HERO box and API-compatible hero list, then refills them
         based on the chosen preset."""

        # Get the currently selected preset from the widget.
        hero_preset = self.panel_hero.var_preset_heroes.get()

        # Wipe the HERO box and list of API-compatible heroes.
        self.panel_hero.box.delete(0, tk.END)
        self.heroes = self.owh.get_heroes_by_role(hero_preset)

        # Refill the box and list.
        for hero in self.heroes:
            self.panel_hero.box.insert(tk.END, hero)

        self.alert.print(f"Set hero selection to '{hero_preset}' preset.")
        self._update_stat_menu_options()

    def _cmd_clear_heroes(self):
        """Clears the contents of the hero box."""

        # Ensure pressing the CLEAR button only creates an alert if the
        #  HERO box wasn't already empty.
        if self.heroes:
            self.alert.print("Cleared all heroes from the selection.")

        # Wipe the HERO box and list of API-compatible heroes.
        self.panel_hero.box.delete(0, tk.END)
        self.heroes = []

        # Also wipe the STAT box because you can't pick a stat
        #  if no heroes are loaded!
        self.panel_stat.box.delete(0, tk.END)
        self._update_stat_menu_options()

    def _cmd_toggle_checkbox_quickplay(self):
        """Checks the QuickPlay box and unchecks the Comp box."""
        self.panel_stat.chk_qp.select()
        self.panel_stat.chk_cp.deselect()
        self.api.mode = 'quickPlayStats'

        self._update_stat_menu_options()

    def _cmd_toggle_checkbox_comp(self):
        """Unchecks the QuickPlay box and checks the Comp box."""
        self.panel_stat.chk_qp.deselect()
        self.panel_stat.chk_cp.select()
        self.api.mode = 'competitiveStats'

        self._update_stat_menu_options()

    def _cmd_add_preset_stats(self, *args):
        """Change stat box options to the selected preset."""

        # Wipe the contents of the stat box.
        self.panel_stat.box.delete(0, tk.END)

        # Get the selected preset from the dropdown menu widget.
        preset = self.stat_menu.var_list.get()

        # Use the preset to get new stats to display from the API,
        #  then insert them into the stat box.
        if new_stats := self.api.get_new_stat_menu(preset):
            for new_stat in new_stats:
                self.panel_stat.box.insert(tk.END, new_stat)
            self.alert.print(f"Set stat types to '{preset}' preset.")

        self._check_run_state()


class InterfacePanel:
    """A class representing a single panel inside the Overwatch GUI,
    which can be made up of various elements."""

    def __init__(self, panel_type):
        """Initialize all variables that will contain widgets for the panel."""

        # Main frame attributes.
        self.type = panel_type
        self.style = StyleSettings(panel_type)
        self.frm = None
        self.frm_width = 300

        # Major GUI elements.
        self.header = None
        self.box = None
        self.frm_entry = None
        self.ent_hero = None
        self.description = None

        # Button-related attributes.
        self.frm_btn = None
        self.btn_add = None
        self.btn_del = None
        self.btn_save = None
        self.btn_clear = None

        # Dropdown-related attributes.
        self.drp_hero = None
        self.var_preset_heroes = None
        self.drp_stat = None
        self.var_preset_stats = None

        # Checkbox-related attributes.
        self.chk_qp = None
        self.chk_cp = None

    def create_main_frame(self, master):
        """Creates the main frame."""
        self.frm = tk.Frame(
            master=master,
            background=self.style.colors['frame'],
            borderwidth=10,
            height=510,
            highlightthickness=0,
            relief=tk.RAISED,
        )
        self.frm.rowconfigure(0, minsize=40)
        self.frm.rowconfigure(1, minsize=40)
        self.frm.rowconfigure(2, minsize=0)
        self.frm.rowconfigure(3, minsize=400)
        self.frm.rowconfigure(4, minsize=30)
        self.frm.columnconfigure(0, minsize=self.frm_width)

    def create_header(self):
        """Creates a simple label."""
        self.header = tk.Label(
            master=self.frm,
            text=self.style.texts['header'],
            font=self.style.fonts['header'],
            background=self.style.colors['header'],
            foreground=self.style.colors['header_txt'],
            borderwidth=10,
        )

    def create_frm_button(self):
        """Creates an empty frame to hold button."""
        self.frm_btn = tk.Frame(
            master=self.frm,
            background=self.style.colors['frm_button']
        )
        # Uncomment to override button frame color to panel's frame color.
        # self.frm_btn.config(background=self.style.colors['frame'])
        self.frm_btn.columnconfigure(0, minsize=(self.frm_width / 4))
        self.frm_btn.columnconfigure(1, minsize=(self.frm_width / 4))
        self.frm_btn.columnconfigure(2, minsize=(self.frm_width / 4))
        self.frm_btn.columnconfigure(3, minsize=(self.frm_width / 4))

    def create_frm_entry(self):
        """Create an empty frame to hold an entry prompt."""
        self.frm_entry = tk.Frame(master=self.frm)
        self.frm_entry.columnconfigure(0, minsize=178)

    def create_listbox(self):
        """Create a listbox."""
        self.box = tk.Listbox(
            master=self.frm,
            activestyle='none',
            background=self.style.colors['box'],
            borderwidth=10,
            exportselection=0,
            font=self.style.fonts['box'],
            height=15,
            highlightthickness=0,
            relief=tk.SUNKEN,
            selectbackground=self.style.colors['box_select'],
            selectborderwidth=3,
            selectmode=tk.MULTIPLE,
        )
        if self.type == 'stat':
            self.box.config(selectmode=tk.SINGLE)

    def create_btn_add(self):
        """Create a button."""
        self.btn_add = tk.Button(master=self.frm_btn, text='Add', width=7)

    def create_btn_del(self):
        """Create a button."""
        self.btn_del = tk.Button(master=self.frm_btn, text='Del', width=7)

    def create_btn_save(self):
        """Create a button."""
        self.btn_save = tk.Button(master=self.frm_btn, text='Save', width=7)

    def create_btn_clear(self):
        """Create a button."""
        self.btn_clear = tk.Button(master=self.frm_btn, text='Clear', width=7)

    def create_drop_heroes(self, presets):
        """Create a dropdown menu for heroes."""
        self.var_preset_heroes = tk.StringVar()
        self.var_preset_heroes.set("All")
        self.drp_hero = tk.OptionMenu(
            self.frm_btn, self.var_preset_heroes, *presets)
        self.drp_hero.config(width=7, highlightthickness=0)

    def create_checkbox_quickplay(self):
        """Create a checkbox."""
        self.chk_qp = tk.Checkbutton(
            master=self.frm_btn,
            text="QP",
            width=5,
        )

    def create_checkbox_comp(self):
        """Create a checkbox."""
        self.chk_cp = tk.Checkbutton(
            master=self.frm_btn,
            text="Comp",
            width=5,
        )

    def create_description(self):
        self.description = tk.Label(
            master=self.frm,
            text=self.style.texts['description'],
            background=self.style.colors['description'],
            foreground=self.style.colors['description_txt'],
        )


class DropdownMenu:
    """A class to represent dropdown menus."""
    def __init__(self, master, default_text, choices):
        """Initialize the menu."""

        def _change_dropdown(*args):
            """Change the displayed choice when the user selects an option."""
            self.var_list.get()

        self.var_list = tk.StringVar(master)
        self.var_list.set(default_text)
        self.menu = tk.OptionMenu(
            master, self.var_list, *choices)
        self.menu.config(highlightthickness=0, height=1)
        self.var_list.trace('w', _change_dropdown)

    def set_new_options(self, choices, reset=False):
        """Docstring"""
        menu = self.menu['menu']
        menu.delete(0, 'end')
        for string in choices:
            menu.add_command(label=string,
                             command=lambda
                             value=string: self.var_list.set(value))
        if reset:
            self.var_list.set('average')

    def clear_options(self):
        """Docstring"""
        menu = self.menu['menu']
        menu.delete(0, 'end')
        self.var_list.set('')


class AlertBox:
    """
    Tkinter Listbox for displaying status and error messages in the GUI.

    Pass desired message and style to the class's print() method.
    """
    def __init__(self, master):
        """
        Initializes the Listbox object.

        :param master: Tkinter object to which the AlertBox should be attached
        """
        self.window = master
        self.style = StyleSettings('alert')
        self.box = tk.Listbox(
            master=master,
            activestyle='none',
            background=self.style.colors['background'],
            borderwidth=20,
            exportselection=0,
            font=self.style.fonts['alert'],
            foreground=self.style.colors['foreground'],
            height=4,
            highlightthickness=0,
            relief=tk.SUNKEN,
            selectbackground=self.style.colors['bg_select'],
            selectborderwidth=0,
            selectmode=tk.SINGLE,
        )

    def print(self, text, style='normal', color='white'):
        """
        Prints a message in the GUI's alert box.

        :param text: the message you want to print
        :param style: the display style for the message
        :param color: the color of the message

        **Available display styles:**
         - error
         - success
         - waiting
         - api_fail (see caution)

        **Caution**: If using the 'api_fail' style, pass only the API error code
        as an argument rather than a message string.
        """

        if style == 'error':
            message = f"!! {text} !!"
            color = 'red'
        elif style == 'success':
            message = f" ! {text} !"
            color = '#12E12B'
        elif style == 'waiting':
            message = f"{text}..."
            color = '#0CEAE0'
        elif style == 'api_fail':
            message = self._get_api_error_msg(text)
            color = 'orange'
        else:
            message = f"> {text}"
            color = color

        self._update(message, color)

    def _update(self, message, color):
        """
        Inserts a line in the alert box, then changes the line's color and
        scrolls to the bottom of the box.

        :param message: the line to be inserted
        :param color: the color of the line
        """
        self.box.insert(tk.END, message)
        self.box.itemconfig(tk.END, fg=color)
        self.box.see(tk.END)

    def _get_api_error_msg(self, code):
        """
        Get the API error message corresponding to a code.

        :param code: Error code
        :return: Error message
        """
        errors = {
            400: 'Your request sucks.',
            404: 'The specified profile could not be found.',
            406: 'You requested a format that isn’t json.',
            500: 'We had a problem with our server. Try again later.',
            503: 'We’re temporarily offline for maintenance. Try again later.',
        }
        message = f">> Error {code}: {errors[code]}"
        return message


class RunButton:
    """A run button that listens for events maybe?"""
    def __init__(self, master):
        """Initialize the button."""
        self.style = StyleSettings()
        self.button = tk.Button(
            master=master,
            text='RUN',
            background='red',
            activebackground='orange',
            activeforeground='white',
            font=self.style.fonts['run'],
            borderwidth=20,
            relief=tk.RAISED,
        )
        self.disable()

    def disable(self):
        """Disable the button."""
        self.button.config(state=tk.DISABLED, bg='grey')

    def enable(self):
        """Enable the button."""
        self.button.config(state=tk.NORMAL, bg='red')


class TopBar:
    def __init__(self, master):
        """Initialize a frame to contain buttons above the UI."""
        self.bar = tk.Frame(
            master=master,
            background='#53560d',
            highlightthickness=0,
        )

        self.info = tk.Button(
            master=self.bar,
            bitmap='info',
            background='blue',
            borderwidth=5,
            relief=tk.RAISED,
        )

        self.close = tk.Button(
            master=self.bar,
            bitmap='error',
            background='red',
            borderwidth=5,
            relief=tk.RAISED,
        )


class HelpButton:
    def __init__(self, master):
        """Initialize a help button."""
        self.button = tk.Button(
            master=master,
            bitmap='info',
            background='blue',
            borderwidth=5,
            relief=tk.RAISED,
        )


class ExitButton:
    """An exit button for the OverwatchGUI."""
    def __init__(self, master):
        """Initialize the button."""
        self.button = tk.Button(
            master=master,
            bitmap='error',
            background='red',
            borderwidth=5,
            relief=tk.RAISED,
        )


class StyleSettings:
    """Holds style settings for the Overwatch GUI."""
    def __init__(self, panel_type=None):
        self.colors = None
        self.texts = None
        self.fonts = {
            'header': ("Helvetica", 16, "bold"),
            'box': ("Calibri", 12, "normal"),
            'alert': ("Courier New", 10, "normal"),
            'run': ("Calibri", 19, "bold"),
        }

        if panel_type == 'window':
            self.set_style_window()
        elif panel_type == 'profile':
            self.set_style_profile()
        elif panel_type == 'hero':
            self.set_style_hero()
        elif panel_type == 'stat':
            self.set_style_stat()
        elif panel_type == 'alert':
            self.set_style_alert()

    def set_style_window(self):
        self.texts = {
            'title': 'Overwatch Stat Comparison Tool'
        }

    def set_style_profile(self):
        """Colors and text for the profile panel."""
        self.colors = {
            'frame': '#1D9367',
            'header': '#146648',
            'header_txt': '#FFFFFF',
            'frm_button': '#4AA886',
            'box': '#E8F4EF',
            'box_select': '#77BEA3',
            'description': '#1D9367',
            'description_txt': '#FFFFFF',
        }
        self.texts = {
            'header': 'Player Profiles',
            'description': 'Add or remove profiles to compare'
        }

    def set_style_hero(self):
        """Colors and text for the hero panel."""
        self.colors = {
            'frame': '#2471A3',
            'header': '#1A5276',
            'header_txt': '#FFFFFF',
            'frm_button': '#5499C7',
            'box': '#D4E6F1',
            'box_select': '#5499C7',
            'description': '#2471A3',
            'description_txt': '#FFFFFF',
        }
        self.texts = {
            'header': 'Heroes',
            'description': 'Add or remove heroes to compare',
        }

    def set_style_stat(self):
        """Colors and text for the stat panel."""
        self.colors = {
            'frame': '#A569BD',
            'header': '#4A235A',
            'header_txt': '#FFFFFF',
            'frm_button': '#BB8FCE',
            'box': '#D2B4DE',
            'box_select': '#8E44AD',
            'description': '#A569BD',
            'description_txt': '#FFFFFF',
        }
        self.texts = {
            'header': 'Stat Config',
            'description': 'Select a preset and click the stat you want to see',
        }

    def set_style_alert(self):
        """Colors and text for the alert box."""
        self.colors = {
            'background': '#111111',
            'bg_select': '#111111',
            'foreground': '#FFFFFF',
        }
