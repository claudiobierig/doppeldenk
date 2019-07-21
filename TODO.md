# TODO

## **Shorter Time (80)**

- [x] Models
  - [x] Add game model variable
- [x] Forms
  - [x] Add field
- [ ] Logic
  - [x] Initialize
    - [x] Use form entry
    - [x] Set midgame scoring time resp.
  - [ ] Move
    - [ ] Use game variable instead of 100
- [ ] Tests
  - [ ] Use gamesetup with 100 and all tests shall pass
  - [ ] Add test to initialize game

## **Influence at higher level**

- [ ] Forms
  - [ ] Add field to setup start influence
- [ ] Logic
  - [ ] Initialize
    - [ ] Use form entry
- [ ] Tests
  - [ ] Use old gamesetup and all tests shall pass
  - [ ] Add test to initialize game

## **Resource against influence**

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

## **List of finished games**

## **Option to change PW**

## **Send reminder if its your turn**

## **Show number of games in which we are active player**

## **JS Live update**

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

## **Fix SVGs so they can be used for both printing and webpage**

## **Improve UI and UX**

- [ ] Different resource symbols, building resource -> oil barrel
- [ ] Change red border for planet we want to fly to

## **Add EuroCrisis**

## **Refactoring**

- [ ] Groundwork to add EuroCrisis
  - [ ] Move lists, etc. to doppeldenk
    - [ ] Check how to present multiple lists in one view
  - [ ] Dropdown for rules
  - [ ] Create game: Dropdown -> different forms depending on choice
- [ ] Clear seperation of MVC
  - [ ] move stuff to js
    - [ ] create current view via js and game_detail.html will be fixed not using safe tags
      - [ ] was probably not such a good idea, need to think more about this
    - [ ] Setup automatic generation of game_detail.html
    - [ ] move stuff from generate_svg to js
- [ ] doxygens
- [ ] move 2dArray to extra app (maybe even extra Repo)
  - [ ] refactor the used functions once transistion is made
- [ ] Move all Magic Numbers to gamesettings
- [ ] use form class for login
- [ ] Cleanup settings
