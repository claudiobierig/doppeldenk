# TODO

## Prio

- [ ] Add Event additional resource
  - [x] Model Changes:
    - [x] Planet:
      - [x] extra_resource
      - [x] extra_resource_time
      - [x] extra_resource_price
    - [x] Game:
      - [x] new_demand_time
      - [x] new_demand_move
      - [x] new_demand (bool)
  - [x] View Changes:
    - [x] Add planet changes to ? (if new_demand)
    - [x] Add game changes to game_board (if new_demand)
  - [ ] Logic Changes:
    - [x] Initialize:
      - [x] game constant (resp. get from data)
      - [x] planet, need to make sure one of the remaining 3
    - [ ] Move:
      - [ ] Cost Influence needs to be adapted
      - [x] Add new_demand event
  - [x] Form Changes:
    - [x] Add tickbox to create form
  - [ ] JS Changes:
    - [ ] Cost Influence needs to be adapted
  - [ ] Testcases adapt
    - [x] Initial
    - [ ] Move
- [ ] Add JS Live Update
  - [ ] Timemarker Update
    - [ ] Rename to player number
    - [ ] On Change in timeform
      - [ ] Get Timemarker
      - [ ] Compute new x, y
      - [ ] Append to group timemarkers
    - [ ] On click on timebox
      - [ ] change timeform
  - [ ] Influence points
    - [ ] move markers to extra group
    - [ ] rename to numbers
    - [ ] On change influence form
      - [ ] Get Marker
      - [ ] Compute new x,y for all influencemarkers of this planet
      - [ ] Update all
    - [ ] On click box of same planet
      - [ ] If larger, change influenceform
  - [ ] Market prices
    - [ ] on change of supply/demand forms
      - [ ] if traded adjust which symbol is used
  - [ ] Allow only possible choices
    - [ ] Market actions
    - [ ] Time selection
    - [ ] Influence

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
- Fix supply resource to planet (only demand is random)
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
  - Clear seperation of MVC (50h)
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
