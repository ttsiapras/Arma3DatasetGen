0 = [] spawn
{
	enableEnvironment false;
	imageCnt    = 4; // Number of images for redundancy
	imageLoop   = 2; //Number of images per vehicle per position
	emptyCntMax = 1; //number of empty images allowed per vehicle per position
	vehicleSelection = 0;	
	map = "Generic";
	
	//Change the weather
	setAccTime 1;
	_fog  = 0.1;
	_over = 0.15;
	_rain = 0;
	//0 setOvercast _over;
	//0 setRain _rain;
	0 setFog  [0.8,0.8,1];
	0 setWaves 0.8;
	//setWind [0,0,true];
	//forceWeatherChange;
	sleep 2;


	while{(vehicleSelection<nof_vehicles)} do
	{
		pos_count= 0;
		failed   = 0;
		_vehicleName  = vehicle_names select vehicleSelection;
		while{pos_count<nof_positions} do
		{
			_v_spawn_pos  = positions select pos_count;
			//_v_spawn_pos  = [_v_spawn_pos, 0, 10, 0, 0, 40, 0] call BIS_fnc_findSafePos;
			// loop over how many  pictures of the vehicle wewant inthis position
			loop        = 0;
			_emptyShots = 0;
			failed      = 0;
			while{loop < imageLoop  && failed<1} do
			{
				// Go to random hour of the Day
				timeToSkip = [6,18] call BIS_fnc_randomInt;
				//skipTime ((timeToSkip - dayTime + 24) % 24); // skip forward to a specific time, irrespective of the current mission time
				sleep 1;
				//Create the vehicle
				_vehicle = createVehicle [_vehicleName, _v_spawn_pos, [], 0, "NONE"]; // Create a vehicle (MRAP for example)

				// Set camera position
				_pos = [_vehicle, 50, 300, 0, 2, 40, 0] call BIS_fnc_findSafePos;
				elevation = [2,20] call BIS_fnc_randomInt;
				_cameraPosition = _pos vectorAdd [0, 0, elevation];
				_camera = "camera"  camCreate _cameraPosition; // Create a camera object at the defined position
				_camera cameraEffect ["EXTERNAL", "BACK"];
				_camera camSetFocus [-1, -1];
				_camera camSetTarget _vehicle; // This makes the camera point towards the vehicle
				_camera camSetFov 0.51;        // this angle matches our FOV when taking a 1024x1024 part of a 1600x1024 windowed screenshot
				_camera camCommit 0;
				sleep 3;                       // Wait a moment for the camera to settle and assets/textures to load
				waitUntil {camCommitted _camera};
				
				if(damage _vehicle <0.1) then
				{
					// Get positions of the vehicle and the observer
					// and check if the line between the vehicle and the observer intersects any surface
					_vehiclePos    = getPos _vehicle;
					_observerPos   = getPos _camera;
					_intersections = lineIntersectsSurfaces [AGLToASL _observerPos, [0,0,2] vectorAdd (AGLToASL _vehiclePos), _camera,_vehicle, false,1];
					_intersection = (_intersections select 0);

					// If no intersection is found, the vehicle is visible
					if (isNil "_intersection") then {
						hint "The vehicle is visible!";
						// Capture images with object 
						counter = 1;
						while{counter<(imageCnt+1)} do{
							sleep 1;
							screenshot (str formatText ["%1-%2-(%3,%4)-(%5,%6)-%7-%8-%9-%10-%11-with.png",map,_vehicleName,_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog,counter]);
							counter = counter +1;
						};
						sleep 0.5;


						deleteVehicle _vehicle;
						sleep 1;
						screenshot (str formatText ["%1-(%2,%3)-%4-%5-%6-%7-empty.png",map,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog]);
						counter = 1;
						// Capture Empty images 
						while{counter<(imageCnt+2)} do{
							sleep 1;
							screenshot (str formatText ["%1-%2-(%3,%4)-(%5,%6)-%7-%8-%9-%10-%11-wout.png",map,(vehicle_names select vehicleSelection),_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog,counter]);
							counter = counter +1;
						};
						//true setCamUseTi 0;
						//false setCamUseTi 0;
						loop = loop +1;
						_emptyShots = 0; //Reset Capacity for empty slots
					} else {
						deleteVehicle _vehicle;
						sleep 0.5;
						hint "The vehicle is NOT visible!";
						_emptyShots =_emptyShots + 1;
						if(_emptyShots < (emptyCntMax +1)) then  
						{
							screenshot (str formatText ["%1-(%2,%3)-%4-%5-%6-%7-empty.png",map,_cameraPosition # 0, _cameraPosition #1,timeToSkip,_over,_rain,_fog]);
							
						};
						if(_emptyShots >=5) then
						{
							failed =1;
						};
					};
				} else {
					failed =1;
				};
				sleep 2;
				_camera cameraEffect ["terminate", "back"];
				camDestroy _camera;
			}; //while image loop
			pos_count = pos_count +1;
		};
		vehicleSelection = vehicleSelection+1;
	};
};
