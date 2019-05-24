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
    timeField.value = computeDistance(hex_element)
}


function refreshChoices()
{
    setViewPlayerState()
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
            const sellSelect = document.getElementById("id_sell_resource_" + (resource + 1))
            const sellAmount = parseInt(sellSelect.options[sellSelect.selectedIndex].value)
            if(sellAmount > 0){
                const cost = sellAmount*getCost(active_planet.sell_resources, active_planet.cost_sell_resource, (resource + 1).toString())
                amount = amount - sellAmount
                money = money + cost
                traded = true
            }
            const buySelect = document.getElementById("id_buy_resource_" + (resource + 1))
            const buyAmount = parseInt(buySelect.options[buySelect.selectedIndex].value)
            if(buyAmount > 0){
                const cost = buyAmount*getCost(active_planet.buy_resources, active_planet.cost_buy_resource, (resource + 1).toString())
                traded = true
                amount = amount + buyAmount
                money = money - cost
            }
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
    if(active_planet != null){
        for(i in active_planet.buy_resources){
            const resource = parseInt(active_planet.buy_resources[i])
            if(resource != 0){
                document.getElementById("price_buy_resource_" + resource).innerHTML = active_planet.cost_buy_resource[i]
            }
        }
        for(i in active_planet.sell_resources){
            const resource = parseInt(active_planet.sell_resources[i])
            if(resource != 0){
                document.getElementById("price_sell_resource_" + resource).innerHTML = active_planet.cost_sell_resource[i]
            }
        }
        document.getElementById("table_head").setAttribute("style", "background-color:" + active_planet.colour)
    }
    /*
    if(active_player != null && active_player.time_spent < 0){
        document.getElementById("id_spend_time").setAttribute("type", "hidden")
    }
    for(var i=1;i<=5;i++){
        if(active_planet == null || !active_planet.sell_resources.includes(i.toString())){
            document.getElementById("id_sell_resource_" + i).style.visibility = 'hidden'
        }
        if(active_planet == null || !active_planet.buy_resources.includes(i.toString())){
            document.getElementById("id_buy_resource_" + i).style.visibility = 'hidden'
        }
    }
    if(active_planet == null){
        document.getElementById("id_buy_influence").style.visibility = 'hidden'
    }*/
}

const game_data = JSON.parse(document.getElementById("game_data").innerHTML)
const active_player = getActivePlayer()
const active_planet = getActivePlanet()

setGameState()

refreshChoices()
