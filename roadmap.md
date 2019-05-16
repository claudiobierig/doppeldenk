# Roadmap

## Prio

- Change UI/UX of planet market
- Create printing material
- Add Event additional resource
- Add Event midgame scoring
- Refactoring

## Planed Features (~80h + Refactoring + ~80h Eurocrisis)

- List of finished games (2h)
- Option to change PW (16h)
- Send reminder if its your turn (12h)
- Show number of games in which we are active player (4h)
- JS Live update (6h + refactoring time)
  - time marker
  - influence points
  - market prices
- Fix SVGs so they can be used for both printing and webpage (10h)
- Update to new rules after WE (22h)
  - Add event to add demand resources (8h)
  - Change cost influence (4h)
  - Add event mid game scoring (8h)
  - Rulebook update (2h)
  - Adjust offer/demand times
- Improve UI and UX (30h)
  - Planet market (16h)
    - Split planet market and influence track
    - How to display multiple demand resources in planet market
    - Change direction of one resource
    - How to make clear offer/demand difference
    - Maybe put resources on planet board (2h)
  - Different resource symbols, building resource -> oil barrel (2h)
  - Fit on screen (8h)
- Update Printing Material (8h)
- Add EuroCrisis (80h + refactoring)

## Open Bugs (4h)

- Pass is not handled correctly (4h)

## Operations (8h)

- Security Settings Django (4h timeboxed)
- Licensing (4h)
- Make repo public (one click, but needs to be cleaned before)
  
## Improve Code Quality (~130h)

- Testcases (10h)
  - Move logic (8h)
  - Create/Join logic (4h)
- Refactoring (~120h)
  - Groundwork to add EuroCrisis (10h)
    - Move lists, etc. to doppeldenk (4h)
      - Check how to present multiple lists in one view
    - Dropdown for rules (2h)
    - Create game: Dropdown -> different forms depending on choice (4h)
  - Clear seperation of MVC (~70h)
    - move stuff to js (~60h)
      - Add game model data so it can be read by js (4h)
      - create current view via js and game_detail.html will be fixed not using safe tags (4h)
      - Setup automatic generation of game_detail.html (6h)
      - get rid of templatetags (0h)
      - move stuff from generate_svg to js (40h)
    - views.py (6h + js stuff)
      - rules: check if we really need this for template (1h)
      - List views: Move querysets to model (1h)
      - Detail View: (4h + js stuff)
        - context should be simplified by a lot after moving stuff to js
      - get_* functions should all vanish after js move, otherwise move to model
  - autopep8 (4h)
  - consistent naming (8h)
    - rename open games
    - buy/sell, offer/demand, etc.
  - doxygens (4h)
  - move 2dArray to extra app (maybe even extra Repo) (10h)
    - refactor the used functions once transistion is made
    - check for licensing
  - Move all Magic Numbers to gamesettings
  - use form class for login (4h)
  - Cleanup settings (2h)
