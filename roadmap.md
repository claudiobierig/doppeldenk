# Roadmap

## Planed Features (~120h + Refactoring)

- List of finished games (2h)
- Option to change PW (16h)
- Show number of games in which we are active player (4h)
- JS Live update (6h + refactoring time)
  - time marker
  - influence points
  - market prices
- Fix SVGs so they can be used for both printing and webpage
- Update to new rules after WE (TBD)
- Add EuroCrisis (80h + refactoring)

## Open Bugs (4h)

- Pass is not handled correctly (4h)

## Operations (8h)

- Security Settings Django (4h timeboxed)
- Licensing (4h)
- Make repo public (one click)
  
## Improve Code Quality (~130h)

- Testcases (10h)
  - Move logic (postpone after rule changes)
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
    - move functions from models.py to logic/initiate.py or similar (1h)
    - views.py (8h)
      - create_game: doesn't need to know about content of form (1h)
      - next_game: move subfunction to model, move filter into subfunction (1h)
      - rules: check if we really need this for template (1h)
      - List views: Move querysets to model (1h)
      - Detail View: (4h + js stuff)
        - Move get_next to model, should use the same function as next_game
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
  - use form class for login (4h)
  - Cleanup settings (2h)
  