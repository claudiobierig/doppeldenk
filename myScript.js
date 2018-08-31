const player_names = ["player1", "player2", "player3", "player4"];
const number_of_markers_to_y = [15,19,23,27];
/**
 * Returns a random number between min (inclusive) and max (exclusive)
 */
function getRandomArbitrary(min, max)
{
    return Math.floor(Math.random() * (max - min) + min);
};

function getRandomPlanet()
{
	const planets = document.getElementsByClassName("planet");
	const i = getRandomArbitrary(0,planets.length);
	return planets[i].id;
};

function isActive(hex)
{
	return hex.style["fill-opacity"] == "1";
};

function getActiveHex(planetName)
{
	const searchName = planetName + "_hex";
	let hexes = document.getElementsByClassName(searchName);
	for(let i=0; i<hexes.length;i++){
		if (isActive(hexes[i]))
		{
			return hexes[i];
		}
	}
};

function getActivePlayer()
{
	const markers = document.getElementsByClassName("timemarker");
	let active_player = markers[0];
	let min_time = parseInt(markers[0].getAttribute("time"));
	let min_y = parseInt(markers[0].getAttribute("y"));
	for(let i=1;i<markers.length;i++){
		if(min_time > parseInt(markers[i].getAttribute("time")) || 
			(min_time == parseInt(markers[i].getAttribute("time")) && min_y > parseInt(markers[i].getAttribute("y")))){
				active_player = markers[i];
				min_time = parseInt(markers[i].getAttribute("time"));
				min_y = parseInt(markers[i].getAttribute("y"));
			}
	}
	return active_player.parentNode;
};

function getActiveShip()
{
	return getShip(getActivePlayer().getAttribute("id"));
};

function clickHex(hex)
{
    let ship = getActiveShip();
    if(isActive(hex) && !isShipAtHex(ship, hex))
    {
    	const distance = computeDistance(ship,hex);
    	setShipPosition(hex, getActivePlayer().getAttribute("id"));
    	increaseTime(distance, getActivePlayer().getAttribute("id"));
    }
};

function isShipAtHex(ship, hex)
{
	const hex_q = hex.getAttribute("coord_q");
    const hex_r = hex.getAttribute("coord_r");
    const ship_q = ship.getAttribute("coord_q");
    const ship_r = ship.getAttribute("coord_r");
    return hex_q == ship_q && hex_r == ship_r;
}

function computeDistance(position1, position2)
{
	const q_1 = parseInt(position1.getAttribute("coord_q"));
	const r_1 = parseInt(position1.getAttribute("coord_r"));
	const q_2 = parseInt(position2.getAttribute("coord_q"));
	const r_2 = parseInt(position2.getAttribute("coord_r"));
	return Math.max(Math.abs(q_1-q_2), Math.abs(r_1-r_2), Math.abs(q_1+r_1 - q_2 - r_2));
};

function mouseOverHex(hex)
{
};

function mouseOutHex(hex)
{
};

function resetTime()
{
	for(let i =0;i<player_names.length;i++){
		let marker = document.getElementById("timemarker_" + player_names[i]);
		marker.setAttribute("time", -1);
	}
	for(let i =0;i<player_names.length;i++){
		let marker = document.getElementById("timemarker_" + player_names[i]);
		setMarker(marker, 0);
	}
};

function startingPositionPlanet(planet)
{
	let hexes = document.getElementsByClassName(planet + "_hex");
	const newStartingPosition = getRandomArbitrary(0, hexes.length);
	for (let i = 0; i < hexes.length; i++) {
		fillPlanet(i==newStartingPosition, hexes[i]);
	}
};

function fillPlanet(planetActive, hex)
{
	if(planetActive)
	{
		hex.style["fill-opacity"] = "1";
	}
	else
	{
		hex.style["fill-opacity"] = "0.2";
	}
};

function startingPositionShip(player_name)
{
	const startingPlanet = getRandomPlanet();
	const startingHex = getActiveHex(startingPlanet);
	setShipPosition(startingHex, player_name);
};


function getShipHangar(hex, ship)
{
	//TODO: make this dependent on shipName and hexsize
	let newPosition = [0,0]
	const shipName = ship.getAttribute("id");
	if(shipName == "ship_player1"){
		newPosition = [hex.points[5].x - ship.getAttribute("width") - 3, hex.points[5].y - ship.getAttribute("height")/2];
	}else if(shipName == "ship_player2"){
		newPosition = [hex.points[2].x + 3, hex.points[2].y - ship.getAttribute("height")/2];
	}else if(shipName == "ship_player3"){
		newPosition = [hex.points[4].x - ship.getAttribute("width")/2, 3 + hex.points[4].y + ship.getAttribute("height")];
	}else if(shipName == "ship_player4"){
		newPosition = [hex.points[3].x - ship.getAttribute("width")/2, 3 + hex.points[3].y + ship.getAttribute("height")];
	}
	return newPosition;
};

function setShipPosition(toHex, player_name)
{
	let ship = getShip(player_name);
	const newPosition = getShipHangar(toHex, ship);
	ship.setAttribute("x",newPosition[0]);
	ship.setAttribute("y",newPosition[1]);
	ship.setAttribute("coord_q",toHex.getAttribute("coord_q"));
	ship.setAttribute("coord_r",toHex.getAttribute("coord_r"));
};

function startingPosition()
{
	resetTime();
	const planets = document.getElementsByClassName("planet");
	for(let i=0;i<planets.length;i++){
		startingPositionPlanet(planets[i].id);
	}
	for(let i=0; i<player_names.length; i++){
		startingPositionShip(player_names[i]);
	}
};

function rotatePlanet(planetName)
{
	let planet = getActiveHex(planetName);
	const planetId = planet.id;
	const oldPosition = parseInt(planetId.replace(planetName + "_",""));
	const searchName = planetName + "_hex";
	let hexes = document.getElementsByClassName(searchName);
	const newPosition = (oldPosition + 1) % hexes.length;
	let oldHex = hexes[oldPosition];
	let newHex = hexes[newPosition];
	fillPlanet(false,oldHex);
	fillPlanet(true,newHex);
	for(let i=0;i<player_names.length;i++){
		let ship = getShip(player_names[i]);
		if(isShipAtHex(ship,oldHex)){
			setShipPosition(newHex,player_names[i]);
		}	
	}
	
};

function rotatePlanets()
{
	const planets = document.getElementsByClassName("planet");
	for(let i=0;i<planets.length;i++){
		rotatePlanet(planets[i].id);
	}
};


function executeEvent(event)
{
	//TODO: only working for planet rotation at the moment
	if(event.getAttribute("event") == "planet_rotation")
	{
		rotatePlanets();
	}
};

function setMarker(marker, time)
{
	marker.setAttribute("time", time.toString());
	const timebox = document.getElementById("timebox_" + time.toString());
	const markers = document.getElementsByClassName("timemarker");
	let markersWithSameTime = -1;
	for(let i=0;i<markers.length;i++){
		if(parseInt(markers[i].getAttribute("time"))==time){
			markersWithSameTime++;
		}
	}
	marker.setAttribute("x", timebox.getAttribute("x"));
	marker.setAttribute("y", (parseInt(timebox.getAttribute("y")) + parseInt(timebox.getAttribute("height")) - number_of_markers_to_y[markersWithSameTime]).toString());
	let player = marker.parentNode;
	let players = player.parentNode;
	players.appendChild(player);
};


function executeEvents(start)
{
	const events = document.getElementsByClassName("event");
	const end = getMarker(getActivePlayer().getAttribute("id")).getAttribute("time");
	for(let i=0; i<events.length;i++)
	{
		eventTime = parseInt(events[i].getAttribute("time"));
		if(start < eventTime && eventTime <= end)
		{
			executeEvent(events[i]);
		}
	}
};

function getShip(player_name)
{
	return document.getElementById("ship_" + player_name);	
}

function getMarker(player_name)
{
	return document.getElementById("timemarker_" + player_name);
};


function increaseTime(strTime, player_name)
{
	let marker = getMarker(player_name);
	const timeStart = parseInt(marker.getAttribute("time"));
	const timePassed = parseInt(strTime);
	const timeEnd = timeStart + timePassed;
	setMarker(marker,timeEnd);
	executeEvents(timeStart);
};

startingPosition();
