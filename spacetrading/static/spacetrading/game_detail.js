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
}


function refreshChoices()
{
    getCurrentState()
    setViewPlayerState()
}

function setViewPlayerState()
{
}

function getCurrentState()
{
}



const game_data = JSON.parse(document.getElementById("game_data").innerHTML)

const active_player = getActivePlayer()
console.log(active_player)
refreshChoices()
