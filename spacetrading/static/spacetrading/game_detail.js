
lastClickedHex = null

function getActivePlayer()
{
    subgroup = document.getElementById("playerboards")
    for(i=0; i<subgroup.childNodes.length; i++){
        try{
            if(subgroup.childNodes[i].getAttribute("active") == "True"){
                return subgroup.childNodes[i]
            }
        }
        catch(error) {
        }
    }
    return null
}

function getAttributeFromPlayerboard(playerboard, attribute)
{
    if(playerboard == null){
        return 0
    }
    return playerboard.getAttribute(attribute)
}

function clickHex(hex_element)
{
    document.getElementById("id_coord_q").value = hex_element.getAttribute("coord_q")
    document.getElementById("id_coord_r").value = hex_element.getAttribute("coord_r")

    hex_element.style['stroke-width'] = 1.5
    hex_element.style['stroke-opacity'] = 1
    hex_element.style.stroke = "red"
    if (lastClickedHex != null){
        lastClickedHex.style.stroke = "white"
        lastClickedHex.style['stroke-width'] = 0.5
        lastClickedHex.style['stroke-opacity'] = 0.5
    }
    
    lastClickedHex = hex_element
}

function changeInfluence(amount)
{
    console.log(0 + amount)
}

function change_buy_resource(resource, amount)
{
    console.log("change_buy_resource " + resource + " " + amount)
}

function change_sell_resource(resource, amount)
{
    console.log("change_sell_resource " + resource + " " + amount)
}

const active_player = getActivePlayer()
const starting_money = getAttributeFromPlayerboard(active_player, "money")
const resources = [
    getAttributeFromPlayerboard(active_player, "resource_0"),
    getAttributeFromPlayerboard(active_player, "resource_1"),
    getAttributeFromPlayerboard(active_player, "resource_2"),
    getAttributeFromPlayerboard(active_player, "resource_3"),
    getAttributeFromPlayerboard(active_player, "resource_4")
]

console.log(resources)