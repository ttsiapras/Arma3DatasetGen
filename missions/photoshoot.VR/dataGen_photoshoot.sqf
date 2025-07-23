0 = [] spawn
{
	enableEnvironment false;
	imageLoop   = 11; //Number of images per vehicle per position
	emptyCntMax = 2; //number of empty images allowed per vehicle per position
	vehicleSelection = 0;	
	map = "VR";
	
	//Change the weather
	setAccTime 1;

	height_max    = 20;
	offset_max    = 40;
	_v_spawn_pos  = [4000,4000];

	while{(vehicleSelection<nof_vehicles)} do
	{
		_vehicleName  = vehicle_names select vehicleSelection;
		loop=0;
		while{loop < imageLoop} do
		{
			//Create the vehicle
			_vehicle = createVehicle [_vehicleName, _v_spawn_pos, [], 0, "NONE"]; // Create a vehicle (MRAP for example)

			// Set camera position
			_pos = [_vehicle, 10, offset_max, 0, 0, 40, 0] call BIS_fnc_findSafePos;
			_height = [1,height_max] call BIS_fnc_randomInt;
			_cameraPosition = _pos vectorAdd [0, 0, _height];
			_camera = "camera"  camCreate _cameraPosition; // Create a camera object at the defined position
			_camera cameraEffect ["EXTERNAL", "BACK"];
			_camera camSetFocus [-1, -1];
			_camera camSetTarget _vehicle; // This makes the camera point towards the vehicle
			_camera camSetFov 0.51;        // this angle matches our FOV when taking a 1024x1024 part of a 1600x1024 windowed screenshot
			_camera camCommit 0;
			//true setCamUseTI 0;
			sleep 1;                       // Wait a moment for the camera to settle and assets/textures to load
			waitUntil {camCommitted _camera};
			
			// Get positions of the vehicle and the observer
			// and check if the line between the vehicle and the observer intersects any surface
			_vehiclePos    = getPos _vehicle;
			_observerPos   = getPos _camera;

			screenshot (str formatText ["%1-%2-(%3,%4)-(%5,%6)-%7-%8-%9-%10-%11-with.png",map,_vehicleName,_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,0,0,0,0,0]);
			sleep 1;
			deleteVehicle _vehicle;
			sleep 1;
			screenshot (str formatText ["%1-%2-(%3,%4)-(%5,%6)-%7-%8-%9-%10-%11-wout.png",map,_vehicleName,_vehiclePos # 0, _vehiclePos #1,_cameraPosition # 0, _cameraPosition #1,0,0,0,0,0]);
			sleep 1;
			loop = loop +1;
			_camera cameraEffect ["terminate", "back"];
			camDestroy _camera;
		}; //while image loop
		vehicleSelection = vehicleSelection+1;
	};
};
