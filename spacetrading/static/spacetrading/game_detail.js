lastClickedHex = null
lastClickedHexStrokeColour = "white"
lastClickedHexStrokeWidth = 0.5
lastClickedHexStrokeOpacity = 0.5

function is_before(player1, player2)
{
    if(player1 == null || player1.has_passed){
        return false
    }
    if(player2 == null || player2.has_passed){
        return true
    }
    if(player1.time_spent < player2.time_spent || (player1.time_spent == player2.time_spent && player1.last_move > player2.last_move)){
        return true
    }
    return false
}


function getActivePlayer()
{
    current_player = null
    for(player in game_data.players){
        if(is_before(game_data.players[player], current_player)){
            current_player = game_data.players[player]
        }
    }
    return current_player
}

function getActivePlanet()
{
    if(active_player == null){
        return null
    }
    for(planetnumber in game_data.planets){
        const planet = game_data.planets[planetnumber]
        if(active_player.ship_position[0] == planet.position_of_hexes[planet.current_position][0] &&
            active_player.ship_position[1] == planet.position_of_hexes[planet.current_position][1]){
            return planet
        }
    }
    return null
}

function computeDistance(hex_element){
    if(hex_element == null){
        return 0
    }
    const destination_q = hex_element.getAttribute("coord_q")
    const destination_r = hex_element.getAttribute("coord_r")
    const destination_s = -destination_q -destination_r
    const current_q = active_player.ship_position[0]
    const current_r = active_player.ship_position[1]
    const current_s = -current_q -current_r
    distance = Math.max(
        Math.abs(destination_q-current_q),
        Math.abs(destination_r-current_r),
        Math.abs(destination_s-current_s)
    )
    if(distance > 0){
        return distance + 2
    }
    return 4
}

function clickHex(hex_element)
{
    if (lastClickedHex != null){
        lastClickedHex.style.stroke = lastClickedHexStrokeColour
        lastClickedHex.style['stroke-width'] = lastClickedHexStrokeWidth
        lastClickedHex.style['stroke-opacity'] = lastClickedHexStrokeOpacity
    }

    lastClickedHexStrokeColour = hex_element.style.stroke
    lastClickedHexStrokeWidth = hex_element.style['stroke-width']
    lastClickedHexStrokeOpacity = hex_element.style['stroke-opacity']

    document.getElementById("id_coord_q").value = hex_element.getAttribute("coord_q")
    document.getElementById("id_coord_r").value = hex_element.getAttribute("coord_r")
    hex_element.style['stroke-width'] = 5
    hex_element.style['stroke-opacity'] = 1
    hex_element.style.stroke = "red"
    
    lastClickedHex = hex_element
    var timeField = document.getElementById("id_spend_time")
    const distance = computeDistance(hex_element)
    timeField.value = distance
    setTimeMarker(active_player.time_spent + distance)
}


function refreshChoices()
{
    setViewPlayerState()
    setInfluenceTrack()
}

function getCost(resources, cost, resource)
{
    for(var i=0; i<resources.length; i++){
        if(resource == resources[i]){
            return cost[i]
        }
    }
    return 0
}

function getCurrentInfluence()
{
    for(p in game_data.planets){
        if(active_planet == game_data.planets[p]){
            return game_data.planet_influence_track[p][active_player.player_number]
        }
    }
}

function getCostInfluence(traded, boughtInfluence){
    var cost = 0
    var currentInfluence = getCurrentInfluence()
    if(traded && boughtInfluence > 0){
        cost = cost + 1
        boughtInfluence = boughtInfluence - 1
        currentInfluence = currentInfluence + 1
    }
    cost = cost + (2*currentInfluence + boughtInfluence + 1)*boughtInfluence/2
    return cost
}

function setViewPlayerState()
{
    var player_number = active_player.player_number
    var money = active_player.money
    var traded = false
    for(var resource = 0; resource <5; resource++)
    {
        var amount = active_player.resources[resource]
        if(active_planet != null){
            try{
                const supplySelect = document.getElementById("id_planet_supply_resource_" + (resource + 1))
                const supplyAmount = parseInt(supplySelect.options[supplySelect.selectedIndex].value)
                if(supplyAmount > 0){
                    const cost = supplyAmount*getCost(active_planet.planet_supply_resources, active_planet.planet_supply_resources_price, (resource + 1).toString())
                    amount = amount + supplyAmount
                    money = money - cost
                    traded = true
                }
            }catch{}
            try{
                const demandSelect = document.getElementById("id_planet_demand_resource_" + (resource + 1))
                const demandAmount = parseInt(demandSelect.options[demandSelect.selectedIndex].value)
                if(demandAmount > 0){
                    const cost = demandAmount*getCost(active_planet.planet_demand_resources, active_planet.planet_demand_resources_price, (resource + 1).toString())
                    traded = true
                    amount = amount - demandAmount
                    money = money + cost
                }
            }catch{}
        }
        document.getElementById("resource_amount_" + (resource + 1) + "_" + player_number).innerHTML = amount
    }
    if(active_planet != null){
        const influenceSelect = document.getElementById("id_buy_influence")
        const boughtInfluence = parseInt(influenceSelect.options[influenceSelect.selectedIndex].value)
        const costInfluence = getCostInfluence(traded, boughtInfluence)
        money = money - costInfluence
    }
    document.getElementById("coins_" + player_number).innerHTML = money
}

function setGameState()
{
    document.getElementById("resource_limit").innerHTML = "Resource limit: " + game_data.resource_limit
    if(game_data.midgame_scoring)
    {
        document.getElementById("midgame_scoring").innerHTML = "Midgame scoring (2, 1)"
    }
    else
    {
        document.getElementById("midgame_scoring").innerHTML = "No midgame scoring"
    }
    
    if(active_planet != null){
        document.getElementById("table_head").setAttribute("style", "background-color:" + active_planet.colour)
    }
}

function getStackPositionTimeline(time)
{
    var stack_position = 0
    for(player in game_data.players)
    {
        if(time == game_data.players[player].time_spent &&
           game_data.players[player].player_number != active_player.player_number &&
           !game_data.players[player].has_passed
        ){
                stack_position++
        }
    }
    if(game_data.planet_rotation_event_time == time)
    {
        stack_position++
    }
    if(game_data.offer_demand_event_time == time)
    {
        stack_position++
    }
    if(game_data.midgame_scoring && game_data.midgame_scoring_event_time == time)
    {
        stack_position++
    }
    return stack_position
}

function getPosition(time_spent)
{
    const SIZE_TIMEBOX = 30
    const stack_position = getStackPositionTimeline(time_spent)
    var time_space = time_spent % 100
    var x_pos = 0
    var y_pos = 0

    if(0 <= time_space && time_space <= 30)
    {
        x_pos = time_space * SIZE_TIMEBOX
        y_pos = 15
    }
    else if( 30 < time_space && time_space <= 50)
    {
        x_pos = 30 * SIZE_TIMEBOX
        y_pos = 15 + (time_space - 30) * SIZE_TIMEBOX
    }
    else if( 50 < time_space && time_space <= 80)
    {
        x_pos = (80 - time_space) * SIZE_TIMEBOX
        y_pos = 15 + 20*SIZE_TIMEBOX
    }
    else if( 80 < time_space && time_space < 100)
    {
        x_pos = 0
        y_pos = 15 + (100 - time_space) * SIZE_TIMEBOX
    }
    y_pos = y_pos - stack_position*4
    return [x_pos.toString(), y_pos.toString()]
}

function setTimeMarker(time)
{
    const position = getPosition(time)
    var timemarkers = document.getElementById("timemarkers")
    var timemarker = document.getElementById("timemarker_player_" + active_player.player_number)
    timemarker.setAttribute("x", position[0])
    timemarker.setAttribute("y", position[1])
    timemarkers.appendChild(timemarker)
}

function timeChanged()
{
    const distance = computeDistance(lastClickedHex)
    var timeField = document.getElementById("id_spend_time")
    if(timeField.value < distance){
        timeField.value = distance
    }
    setTimeMarker(active_player.time_spent + parseInt(timeField.value))
}

function clickTimebox(timebox)
{
    const timeChosen = parseInt(timebox.getAttribute("time"))
    const distance = computeDistance(lastClickedHex)
    const minTime = active_player.time_spent + distance
    var timeField = document.getElementById("id_spend_time")
    if(timeChosen > minTime){
        timeField.value = timeChosen - active_player.time_spent
    }
    else
    {
        timeField.value = minTime - active_player.time_spent
    }
    setTimeMarker(active_player.time_spent + parseInt(timeField.value))
}

function getPositionInfluence(influence, stack_position)
{
    return [active_planet.planet_number*30, (20 - influence)*30 + 15 - 4*stack_position]
}

function setInfluenceMarker(player_number, influence, stack_position)
{
    var influenceMarker = document.getElementById("influence_marker_" + player_number + "_" + active_planet.name)
    console.log(influenceMarker)
    console.log("influence_marker_" + player_number + "_" + active_planet.name)
    const position = getPositionInfluence(influence, stack_position)
    influenceMarker.setAttribute("x", position[0])
    influenceMarker.setAttribute("y", position[1])
}

function setInfluenceTrack()
{
    if(active_planet == null){
        return
    }
    const currentInfluence = getCurrentInfluence()
    const influenceField = document.getElementById("id_buy_influence")
    const influenceSelect = document.getElementById("id_buy_influence")
    const boughtInfluence = parseInt(influenceSelect.options[influenceSelect.selectedIndex].value)
    const totalInfluence = currentInfluence + boughtInfluence
    var influence_points = []
    for(p in game_data.players){
        var influence = 0
        if(game_data.players[p].player_number == active_player.player_number){
            influence = totalInfluence
        }else{
            influence = game_data.planet_influence_track[active_planet.planet_number][p]
        }
        const stack_position = influence_points.filter(x => x === influence).length
        influence_points.push(influence)
        setInfluenceMarker(game_data.players[p].player_number, influence, stack_position)
    }
}

const game_data = JSON.parse(document.getElementById("game_data").innerHTML)
const active_player = getActivePlayer()
const active_planet = getActivePlanet()

setGameState()

refreshChoices()
