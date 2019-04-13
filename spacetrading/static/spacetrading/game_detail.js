
lastClickedHex = null
lastClickedHexStrokeColour = "white"
lastClickedHexStrokeWidth = 0.5
lastClickedHexStrokeOpacity = 0.5

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

function changeInfluence(amount)
{
    amount_influence_name = "trade_modal_influence_amount"
    amount_influence_element = document.getElementById(amount_influence_name)
    old_amount = parseInt(amount_influence_element.innerHTML)
    new_amount = Math.max(old_amount + amount, 0)
    amount_influence_element.innerHTML = new_amount
}

function change_buy_resource(resource, amount)
{
    amount_element_name = "trade_modal_buy_" + resource + "_amount"
    amount_element = document.getElementById(amount_element_name)
    old_amount = parseInt(amount_element.innerHTML)
    new_amount = Math.max(Math.min(old_amount + amount, 9), 0)
    amount_element.innerHTML = new_amount
}

function change_sell_resource(resource, amount)
{
    amount_element_name = "trade_modal_sell_" + resource + "_amount"
    amount_element = document.getElementById(amount_element_name)
    old_amount = parseInt(amount_element.innerHTML)
    new_amount = Math.max(Math.min(old_amount + amount, 9), 0)
    amount_element.innerHTML = new_amount
}

function on_close_trade_modal()
{
    console.log("on_close")
    for(resource = 1; resource <= 5; resource++)
    {
        name_buy = "trade_modal_buy_" + resource + "_amount"
        element_buy = document.getElementById(name_buy)
        if(element_buy != null){
            element_buy.innerHTML = 0
        }
        name_sell = "trade_modal_sell_" + resource + "_amount"
        element_sell = document.getElementById(name_sell)
        if(element_sell != null){
            element_sell.innerHTML = 0
        }
    }

    name_influence = "trade_modal_influence_amount"
    element_influence = document.getElementById(name_influence)
    element_influence.innerHTML = 0

}

function on_trade()
{
    console.log("on_trade")
    for(resource = 1; resource <= 5; resource++)
    {
        name_buy = "buy_" + resource
        try{
            element_buy = document.getElementById(name_buy)
            if(element_buy != null){
                document.getElementById("id_buy_resource_" + resource).value = parseInt(element_buy.options[element_buy.selectedIndex].value)
            }
        }
        catch(error) {}
        name_sell = "sell_" + resource
        try{
            element_sell = document.getElementById(name_sell)
            if(element_sell != null){
                document.getElementById("id_sell_resource_" + resource).value = parseInt(element_sell.options[element_sell.selectedIndex].value)
            }
        }
        catch(error) {}
    }
    
    name_influence = "buy_i"
    element_influence = document.getElementById(name_influence)
    document.getElementById("id_buy_influence").value = parseInt(element_influence.options[element_influence.selectedIndex].value)
    //TODO: set text in player panel
}

function refreshChoices()
{
    console.log("refreshChoices")
    /*
    TODO:
    getCurrentState();
    setTradeModalPlayerState();
    for i=1:5:
        max_sell = resources[i-1]
        min_sell = get_min_sell(current_money, current_resources)
        set_options(min_sell, max_sell, element)
    for i=1:5:
        min_buy = get_min_buy(current_money, current_resources)
        max_buy = get_max_buy(current_money, current_resources)
        set_options(min_buy, max_buy, element)

    var firstList = document.getElementById("sell_1")

    while (firstList.options.length) {
        firstList.remove(0);
    }
    */
}

function getCurrentState()
{
    current_money = starting_money
    current_resources = resources
    traded = false
    for(resource = 1; resource <= 5; resource++)
    {
        name_buy = "buy_" + resource
        try{
            element_buy = document.getElementById(name_buy)
            if(element_buy != null){
                buying_amount = parseInt(element_buy.options[element_buy.selectedIndex].value)
                current_resources[resource - 1] = resources[resource - 1] + buying_amount
                if(buying_amount != 0){
                    traded = true
                    buying_cost = 1//TODO
                    current_money = current_money - buying_amount*buying_cost
                }
            }
        }
        catch(error) {}
        name_sell = "sell_" + resource
        try{
            element_sell = document.getElementById(name_sell)
            if(element_sell != null){
                selling_amount = parseInt(element_sell.options[element_sell.selectedIndex].value)
                current_resources[resource - 1] = resources[resource - 1] - selling_amount
                if(selling_amount != 0){
                    traded = true
                    selling_cost = 1//TODO
                    current_money = current_money + selling_amount*selling_cost
                }
            }
        }
        catch(error) {}
    }
}

function setTradeModalPlayerState()
{
    //set current_money and current_resources in trade modal 
}

const active_player = getActivePlayer()
const starting_money = getAttributeFromPlayerboard(active_player, "money")
const resources = [
    getAttributeFromPlayerboard(active_player, "resource_1"),
    getAttributeFromPlayerboard(active_player, "resource_2"),
    getAttributeFromPlayerboard(active_player, "resource_3"),
    getAttributeFromPlayerboard(active_player, "resource_4"),
    getAttributeFromPlayerboard(active_player, "resource_5")
]

current_money = starting_money
current_resources = resources