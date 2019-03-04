
function clickHex(hex_element)
{
    document.getElementById("id_coord_q").value = hex_element.getAttribute("coord_q")
    document.getElementById("id_coord_r").value = hex_element.getAttribute("coord_r")
    clearMarketActions()
}

function clearMarketActions()
{
    console.log("clear Market Actions")
}