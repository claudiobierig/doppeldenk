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

function getActiveShip()
{
	//TODO: multiplayer
	return document.getElementById("player1");
};

function clickHex(hex)
{
    let ship = getActiveShip();
    if(isActive(hex) && !isShipAtHex(ship, hex))
    {
    	const distance = computeDistance(ship,hex);
    	setShipPosition(hex, ship.id);
    	increaseTime(distance);
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
	let marker = document.getElementById("time_marker1");
	setMarker(marker, 0);
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
		hex.style["fill-opacity"] = "0.1";
	}
};

function startingPositionShip()
{
	const startingPlanet = getRandomPlanet();
	const startingHex = getActiveHex(startingPlanet);
	setShipPosition(startingHex, "player1");
};


function getShipHangar(hex, ship)
{
	//TODO: make this dependent on shipName and hexsize
	let newPosition = [hex.points[5].x - ship.getAttribute("width") - 3, hex.points[5].y - ship.getAttribute("height")/2];
	return newPosition;
};

function setShipPosition(toHex, shipName)
{
	let ship = document.getElementById(shipName);
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
	startingPositionShip();
	
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
	let ship = document.getElementById("player1");
	if(isShipAtHex(ship,oldHex)){
		setShipPosition(newHex,ship.id);
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
	marker.setAttribute("cx", (parseInt(timebox.getAttribute("x")) + parseInt(timebox.getAttribute("width"))/2).toString());
	marker.setAttribute("cy", (parseInt(timebox.getAttribute("y")) + parseInt(timebox.getAttribute("height"))/2).toString());
};


function executeEvents(start, end)
{
	events = document.getElementsByClassName("event");
	for(let i=0; i<events.length;i++)
	{
		eventTime = parseInt(events[i].getAttribute("time"));
		if(start < eventTime && eventTime <= end)
		{
			executeEvent(events[i]);
		}
	}
};
function increaseTime(strTime)
{
	let marker = document.getElementById("time_marker1");
	const timeStart = parseInt(marker.getAttribute("time"));
	const timePassed = parseInt(strTime);
	const timeEnd = timeStart + timePassed;
	setMarker(marker,timeEnd);
	executeEvents(timeStart, timeEnd);

};
