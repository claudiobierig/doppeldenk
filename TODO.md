# Roadmap

## Prio

- Change UI/UX of planet market
- Create printing material
- Add Event additional resource
- Add Event midgame scoring
- Refactoring

## Planed Features (~50h + Refactoring + ~80h Eurocrisis)

- List of finished games (2h)
- Option to change PW (16h)
- Send reminder if its your turn (12h)
- Show number of games in which we are active player (4h)
- JS Live update (6h + refactoring time)
  - time marker
  - influence points
  - market prices
- Fix SVGs so they can be used for both printing and webpage (10h)
- Update to new rules after WE (14h)
  - Add event to add demand resources (8h)
  - Change cost influence (4h)
  - Rulebook update (2h)
- Improve UI and UX (2h)
  - Different resource symbols, building resource -> oil barrel (2h)
- Fix supply resource to planet
- Update Printing Material (8h)
- Add EuroCrisis (80h + refactoring)

## Open Bugs

## Operations (8h)

- Security Settings Django (4h timeboxed)
- Licensing (4h)
- Make repo public (one click, but needs to be cleaned before)
  
## Improve Code Quality (~100h)

- Refactoring (~100h)
  - Groundwork to add EuroCrisis (10h)
    - Move lists, etc. to doppeldenk (4h)
      - Check how to present multiple lists in one view
    - Dropdown for rules (2h)
    - Create game: Dropdown -> different forms depending on choice (4h)
  - Clear seperation of MVC (~60h)
    - move stuff to js (50h)
      - create current view via js and game_detail.html will be fixed not using safe tags (4h)
      - Setup automatic generation of game_detail.html (6h)
      - move stuff from generate_svg to js (40h)
  - doxygens (4h)
  - move 2dArray to extra app (maybe even extra Repo) (10h)
    - refactor the used functions once transistion is made
    - check for licensing
  - Move all Magic Numbers to gamesettings
  - use form class for login (4h)
  - Cleanup settings (2h)
