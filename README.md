OverwatchStats is a project I started to compare hero stats between people in my former Overwatch friend group.

Users can:
- Add/remove any number of profiles
- Add/remove any number of heroes
- Pick from menus of stats to view for these profiles and heroes
  - including Quick Play and Competitive
  - available stats are dynamic, so if you choose only one hero, you'll be able to see hero-specific stats
- Save added profiles so that next time the program is started, it will automatically attempt to fetch their data

The program can show stats in a variety of combinations:
- One hero, one player
- One hero, multiple players
- Multiple heroes, multiple players

When a stat has been selected, the RUN button activates. It's big and red. Click it to draw basic Plotly bar charts.

The program uses a Tkinter GUI. It was my first attempt at using Tkinter and I'm fairly happy with it.

Data is fetched via ow-api.com.

Limitations:
- I haven't played the game since about Summer 2021, and lost interest in updating the program. It's therefore deprecated.
  - Cassidy is still McCree
  - Hero classes are still Damage, Tank, and Support
  - New heroes are not available for selection
- By default the program will make a new API call for profile data if the current data stored locally is more than a day out of date
  - This can result in a lot of data being saved
  - The goal was to allow for comparisons between past and present stats but I never got that far
- Unusual behavior will probably make it break, though I did try to catch a variety of possible errors

Thanks for reading! This was a project for me to learn Python, Tkinter, and start dipping my toes in Pandas and Plotly, and I had fun with it.
