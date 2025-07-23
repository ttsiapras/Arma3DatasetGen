0 = [] spawn
{
	enableEnvironment false;
	setWind [0,0,false];
	
	// Names of the Vehicles must match the Official names of the game
	vehicle_names = ["B_Truck_01_ammo_F","Leopard2A6HEL_2","walker_A3_PoliceSUV","AC_F_Ambulance_cute_F","C_Truck_02_fuel_F"];

	times = [7.5,11.5,13.5,19.5];
	vehicleSelection = 1;
	_vehicleName  = vehicle_names select vehicleSelection;
	map = worldName;
	
	while{vehicleSelection<5} do
	{
		_vehicleName  = vehicle_names select vehicleSelection;
		hint _vehicleName;
		_v_spawn_pos = [[6000,6000], 0, 4000, 0, 0, 40, 0] call BIS_fnc_findSafePos;

		weatherLoop = 0;
		while{weatherLoop < 1} do
		{
			//Change the weather
			setAccTime 1;
			//_fog  = weatherLoop*0.15;
			//_rain = weatherLoop*0.10;
			//_over = weatherLoop*0.15;
			_over = 0.10;
			_fog  = 0.10;
			_rain = 0;
			0 setOvercast _over;
			0 setRain _rain;
			0 setFog  _fog;
			setWind [0,0,false];
			forceWeatherChange;
			sleep 2;

			loop = 0;
			_emptyShots = 0;
			while{loop < 2} do
			{
				// Go to random hour of the Day
				timeToSkip = [7,19] call BIS_fnc_randomInt;
				skipTime ((timeToSkip - dayTime + 24) % 24); // skip forward to a specific time, irrespective of the current mission time
				sleep 1;
				// Step 1: Create the vehicle
				_vehicle = createVehicle [_vehicleName, _v_spawn_pos, [], 0, "NONE"]; // Create a vehicle (MRAP for example)

				// Set camera position
				_pos = [_vehicle, 50, 500, 0, 0, 40, 0] call BIS_fnc_findSafePos;
				_cameraPosition = _pos vectorAdd [0, 0, 4];
				_camera = "camera"  camCreate _cameraPosition; // Create a camera object at the defined position
				_camera cameraEffect ["EXTERNAL", "BACK"];
				_camera camSetFocus [-1, -1];
				_camera camSetTarget _vehicle; // This makes the camera point towards the vehicle
				_camera camSetFov 0.51;        // this angle matches our FOV when taking a 1024x1024 part of a 1600x1024 windowed screenshot
				_camera camCommit 0;
				sleep 3;                       // Wait a moment for the camera to settle and assets/textures to load
				waitUntil {camCommitted _camera};
				

				// Get positions of the vehicle and the observer
				// and check if the line between the vehicle and the observer intersects any surface
				_vehiclePos = getPos _vehicle;
				_observerPos = getPos _camera;
				_intersections = lineIntersectsSurfaces [AGLToASL _observerPos, [0,0,2] vectorAdd (AGLToASL _vehiclePos), _camera,_vehicle, false,1];
				_intersection = (_intersections select 0);

				// If no intersection is found, the vehicle is visible
				if (isNil "_intersection") then {
					hint "The vehicle is visible!";
					deleteVehicle _vehicle;
					setAccTime 1;

					// Capture Empty images
					counter = 1;
					while{counter<5} do{
						sleep 1;
						if(counter==1) then
						{
							screenshot (str formatText ["%1-[%2,%3]-%4-%5-%6-%7-empty.png",map,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog]);
						};
						screenshot (str formatText ["%1-%2-[%3,%4]-[%5,%6]-%7-%8-%9-%10-%11-wout.png",map,(vehicle_names select vehicleSelection),_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog,counter]);
						counter = counter +1;
					};

					sleep 0.2;
					_vehicle = createVehicle [_vehicleName, _vehiclePos, [], 0, "NONE"]; // Create a vehicle (MRAP for example)
					sleep 3; //Wait for vehicle to settle

					// Capture images with object
					counter = 1;
					while{counter<5} do{
						sleep 1;
						screenshot (str formatText ["%1-%2-[%3,%4]-[%5,%6]-%7-%8-%9-%10-%11-with.png",map,(vehicle_names select vehicleSelection),_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog,counter]);
						counter = counter +1;
					};

					//true setCamUseTi 0;
					//false setCamUseTi 0;
					sleep 0.1;
					loop = loop +1;
					_emptyShots = 0; //Reset Capacity for empty slots
				} else {
					hint "The vehicle is NOT visible!";
					if(_emptyShots < 2) then  
					{
						screenshot (str formatText ["%1-[%2,%3]-%4-%5-%6-%7-empty.png",map,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog]);
						_emptyShots =_emptyShots + 1;
					}
					else{
						//Up to 2 empty images per one object image
						_v_spawn_pos = [[6000,6000], 0, 4000, 0, 0, 40, 0] call BIS_fnc_findSafePos;
					};
				};

				deleteVehicle _vehicle;

				_camera cameraEffect ["terminate", "back"];
				camDestroy _camera;

				setAccTime 1;
			};
			weatherLoop = weatherLoop +1;
		};
		vehicleSelection = vehicleSelection+1;
	};
};
