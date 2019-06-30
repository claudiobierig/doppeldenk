# TODO

## Prio

- [ ] New Rules
  - [ ] Shorter Time (80)
    - [ ] Models
      - [ ] Add game model variable
    - [ ] Forms
      - [ ] Add field
    - [ ] Logic
      - [ ] Initialize
        - [ ] Use form entry
        - [ ] Set midgame scoring time resp.
      - [ ] Move
        - [ ] Use game variable instead of 100
    - [ ] Tests
      - [ ] Use gamesetup with 100 and all tests shall pass
      - [ ] Add test to initialize game
  - [ ] Start resources
    - [ ] Models
      - [ ] Add string field with settings where all settings are described
    - [ ] Forms
      - [ ] Add field for start resource
      - [ ] Add field for starting money
      - [ ] Add field for increasing money per player
    - [ ] Logic
      - [ ] Initialize
        - [ ] Use form entries
    - [ ] Tests
      - [ ] Use old gamesetup and all tests shall pass
      - [ ] Add test to initialize game
  - [ ] Influence at higher level
    - [ ] Forms
      - [ ] Add field to setup start influence
    - [ ] Logic
      - [ ] Initialize
        - [ ] Use form entry
    - [ ] Tests
      - [ ] Use old gamesetup and all tests shall pass
      - [ ] Add test to initialize game
  - [ ] Resource against influence
    - [ ] Models
      - [ ] Add game model variable bool
      - [ ] Add game model variable resource
    - [ ] Forms
      - [ ] Create
        - [ ] Add checkbox
      - [ ] Trade
        - [ ] Add checkbox (only if resource is present)
    - [ ] Logic
      - [ ] Initialize
        - [ ] Use form entry
        - [ ] Same as additional_demand
      - [ ] Move
        - [ ] No influence price reduction
        - [ ] Trade of resource against influence
    - [ ] Views
      - [ ] Make sure additional_demand and resource_against_influence are not both selected
      - [ ] planet_market: where to put extra resource? remove 2nd row?
    - [ ] Js
      - [ ] Update influence track when checkbox is clicked
      - [ ] No influence price reduction
    - [ ] Tests
      - [ ] Use old gamesetup and all tests shall pass
      - [ ] Add test to initialize game
      - [ ] Add test to trade resource against influence
  
- [ ] Add JS Live Update
  - [x] Timemarker Update
  - [ ] Influence points
    - [x] rename to numbers
    - [x] On change influence form
      - [x] Get Marker
      - [x] Compute new x,y for all influencemarkers of this planet
      - [x] Update all
    - [ ] On click box of same planet
      - [ ] If larger, change influenceform
  - [ ] Market prices
    - [ ] on change of supply/demand forms
      - [ ] if traded adjust which symbol is used
  - [ ] Allow only possible choices
    - [ ] Market actions
    - [x] Time selection
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
- Improve UI and UX (2h)
  - Different resource symbols, building resource -> oil barrel (2h)
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
