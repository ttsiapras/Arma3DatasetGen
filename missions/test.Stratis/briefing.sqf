0 = [] spawn
{
skipTime (6 - daytime + 24 ) % 24;
sleep 1;
0 setFog 0;
0 setOvercast 0;
0 setRain 0;
angleface = 0;
fogvalue = 0;
timevalue = 6;
enableEnvironment [false, false];
angle = 361;

	while {timevalue < 19.5} do
	{
		while {fogvalue < .8} do
		{
			while {angleface < 360} do
			{
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos2 = pos1 vectorAdd [50,0,50];
				cam camSetPos pos2;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos3 = pos1 vectorAdd [-25,43,50];
				cam camSetPos pos3;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos4 = pos1 vectorAdd [-25,-43,50];
				cam camSetPos pos4;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				angleface = angleface+angle;
				sleep 3;
			};
		fogvalue = fogvalue + 0.50;
		1 setFog fogvalue;
		sleep 3;
		angleface = 0;
		};
	timevalue = timevalue + 12;
	skipTime (timevalue - daytime + 24 ) % 24;
	0 setFog 0;
	0 setOvercast 0;
	0 setRain 0;
	fogvalue = 0;
	sleep 3;
	};
skipTime (6 - daytime + 24 ) % 24;
sleep 1;
0 setFog 0;
0 setOvercast 0;
0 setRain 0;
angleface = 0;
fogvalue = 0;
timevalue = 6;
enableEnvironment [false, false];
angle = 361;

	while {timevalue < 19.5} do
	{
		while {fogvalue < .8} do
		{
			while {angleface < 360} do
			{
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos2 = pos1 vectorAdd [50,0,50];
				cam camSetPos pos2;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos3 = pos1 vectorAdd [-25,43,50];
				cam camSetPos pos3;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_CTRG_LSV_01_light_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos4 = pos1 vectorAdd [-25,-43,50];
				cam camSetPos pos4;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				angleface = angleface+angle;
				sleep 3;
			};
		fogvalue = fogvalue + 0.50;
		1 setFog fogvalue;
		sleep 3;
		angleface = 0;
		};
	timevalue = timevalue + 12;
	skipTime (timevalue - daytime + 24 ) % 24;
	0 setFog 0;
	0 setOvercast 0;
	0 setRain 0;
	fogvalue = 0;
	sleep 3;
	};
skipTime (6 - daytime + 24 ) % 24;
sleep 1;
0 setFog 0;
0 setOvercast 0;
0 setRain 0;
angleface = 0;
fogvalue = 0;
timevalue = 6;
enableEnvironment [false, false];
angle = 361;

	while {timevalue < 19.5} do
	{
		while {fogvalue < .8} do
		{
			while {angleface < 360} do
			{
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos2 = pos1 vectorAdd [50,0,50];
				cam camSetPos pos2;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos3 = pos1 vectorAdd [-25,43,50];
				cam camSetPos pos3;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [6258, 5474, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos4 = pos1 vectorAdd [-25,-43,50];
				cam camSetPos pos4;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				angleface = angleface+angle;
				sleep 3;
			};
		fogvalue = fogvalue + 0.50;
		1 setFog fogvalue;
		sleep 3;
		angleface = 0;
		};
	timevalue = timevalue + 12;
	skipTime (timevalue - daytime + 24 ) % 24;
	0 setFog 0;
	0 setOvercast 0;
	0 setRain 0;
	fogvalue = 0;
	sleep 3;
	};
skipTime (6 - daytime + 24 ) % 24;
sleep 1;
0 setFog 0;
0 setOvercast 0;
0 setRain 0;
angleface = 0;
fogvalue = 0;
timevalue = 6;
enableEnvironment [false, false];
angle = 361;

	while {timevalue < 19.5} do
	{
		while {fogvalue < .8} do
		{
			while {angleface < 360} do
			{
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos2 = pos1 vectorAdd [50,0,50];
				cam camSetPos pos2;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos3 = pos1 vectorAdd [-25,43,50];
				cam camSetPos pos3;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				_currentVehicle = "B_GEN_Van_02_transport_F" createVehicle [5998, 4960, 0];
				createVehicleCrew _currentVehicle;
				_currentVehicle setdir angleface;
				_currentVehicle setVehiclePosition [_currentVehicle, [], 0];
				sleep 3;
				pos1 = _currentVehicle modelToWorld [0,5,5];
				cam = "camera" camCreate pos1;
				cam cameraEffect ["INTERNAL", "BACK"];

				pos4 = pos1 vectorAdd [-25,-43,50];
				cam camSetPos pos4;
				cam camSetTarget _currentVehicle;
				cam camCommit 3;
				waitUntil {camCommitted cam};
				sleep .2;
				screenshot "arma3screenshot.png";

				{_currentVehicle deleteVehicleCrew _x} forEach crew _currentVehicle;
				deleteVehicle _currentVehicle;
				sleep 3;
				screenshot "arma3blank.png";

				sleep 3;
				angleface = angleface+angle;
				sleep 3;
			};
		fogvalue = fogvalue + 0.50;
		1 setFog fogvalue;
		sleep 3;
		angleface = 0;
		};
	timevalue = timevalue + 12;
	skipTime (timevalue - daytime + 24 ) % 24;
	0 setFog 0;
	0 setOvercast 0;
	0 setRain 0;
	fogvalue = 0;
	sleep 3;
	};
};
