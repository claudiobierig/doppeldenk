# TODO

- [ ] Cleanup
  - [ ] Remove some of the old rules which won't be used
- [ ] UI
  - [x] cherry-pick from feature branch
  - [ ] switch from svg to artwork
    - [ ] will need to add pics for planets (might just add a svg)
    - [ ] will need to compute which planet we want to from mouse coordinates
    - [ ] might stay with current playerboards
- [ ] rule changes
  - [ ] Add goals
    - [ ] Add earth
      - [ ] Different rules
      - [ ] Different UI
    - [ ] Add meteor
      - [ ] No UI
      - [ ] Just pick up minerals
  - [ ] Influence
  - [x] Fix demand resource
- [ ] AI compatible
  - [ ] Can we add a layer such that logic code can be used for both?

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
