
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

function on_close_trade_modal()
{
    console.log("on_close")
    for(resource = 1; resource <= 5; resource++)
    {
        document.getElementById("id_buy_resource_" + resource).value = 0
        document.getElementById("id_sell_resource_" + resource).value = 0
        name_buy = "buy_" + resource
        element_buy = document.getElementById(name_buy)
        if(element_buy != null){
            //TODO: add only option 0 and select
        }
        name_sell = "sell_" + resource
        element_sell = document.getElementById(name_sell)
        if(element_sell != null){
            //TODO: add only option 0 and select
        }
    }

    name_influence = "buy_i"
    element_influence = document.getElementById(name_influence)
    //TODO: select 0
    
    //TODO refresh choices

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
    getCurrentState()
    setTradeModalPlayerState()
    /*
    TODO:
    
    for i=1:5:
        max_sell = starting_resources[i-1]
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
    traded = false
    for(resource = 1; resource <= 5; resource++)
    {
        current_resources[resource-1] = starting_resources[resource-1]
        name_buy = "buy_" + resource
        try{
            element_buy = document.getElementById(name_buy)
            if(element_buy != null){
                buying_amount = parseInt(element_buy.options[element_buy.selectedIndex].value)
                current_resources[resource - 1] = starting_resources[resource - 1] + buying_amount
                if(buying_amount != 0){
                    traded = true
                    name_buy_price =  "price_buy_resource_" + resource
                    buying_cost = parseInt(document.getElementById(name_buy_price).innerHTML)
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
                current_resources[resource - 1] = starting_resources[resource - 1] - selling_amount
                if(selling_amount != 0){
                    traded = true
                    name_sell_price =  "price_sell_resource_" + resource
                    selling_cost = parseInt(document.getElementById(name_sell_price).innerHTML)
                    current_money = current_money + selling_amount*selling_cost
                }
            }
        }
        catch(error) {}
    }
    element_influence = document.getElementById("buy_i")
    buy_influence_amount = parseInt(element_influence.options[element_influence.selectedIndex].value)
    current_influence = starting_influence
    if(buy_influence_amount > 0 && traded){
        buy_influence_amount--
        current_money--
        current_influence++
    }
    current_money = current_money - (2*current_influence + buy_influence_amount + 1)*buy_influence_amount/2
    current_influence = current_influence + buy_influence_amount
}

function setTradeModalPlayerState()
{
    //set current_money and current_resources in trade modal
    document.getElementById("trade_modal_money").innerHTML = current_money
    document.getElementById("trade_modal_resource_1").innerHTML = current_resources[0]
    document.getElementById("trade_modal_resource_2").innerHTML = current_resources[1]
    document.getElementById("trade_modal_resource_3").innerHTML = current_resources[2]
    document.getElementById("trade_modal_resource_4").innerHTML = current_resources[3]
    document.getElementById("trade_modal_resource_5").innerHTML = current_resources[4]
    document.getElementById("trade_modal_influence").innerHTML = current_influence
}

const active_player = getActivePlayer()
const starting_money = parseInt(getAttributeFromPlayerboard(active_player, "money"))
const starting_resources = [
    parseInt(getAttributeFromPlayerboard(active_player, "resource_1")),
    parseInt(getAttributeFromPlayerboard(active_player, "resource_2")),
    parseInt(getAttributeFromPlayerboard(active_player, "resource_3")),
    parseInt(getAttributeFromPlayerboard(active_player, "resource_4")),
    parseInt(getAttributeFromPlayerboard(active_player, "resource_5"))
]
const starting_influence = parseInt(document.getElementById("trade_modal_influence").innerHTML)

current_money = starting_money
current_resources = [starting_resources[0], starting_resources[1], starting_resources[2], starting_resources[3], starting_resources[4]]
current_influence = starting_influence
refreshChoices()
