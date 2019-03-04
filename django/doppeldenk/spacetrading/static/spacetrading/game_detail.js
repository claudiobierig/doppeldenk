
lastClickedHex = null

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
    clearMarketActions()
}

function clearMarketActions()
{
    console.log("clear Market Actions")
}