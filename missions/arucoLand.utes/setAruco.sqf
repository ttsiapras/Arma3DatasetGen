0 = [] spawn
{
    acucoArray = ["D:\arucos\aruco00B.jpg",
    "D:\arucos\aruco01B.jpg",
    "D:\arucos\aruco02B.jpg",
    "D:\arucos\aruco03B.jpg",
    "D:\arucos\aruco04B.jpg",
    "D:\arucos\aruco05B.jpg",
    "D:\arucos\aruco06B.jpg",
    "D:\arucos\aruco07B.jpg",
    "D:\arucos\aruco08B.jpg",
    "D:\arucos\aruco09B.jpg",
    "D:\arucos\aruco10B.jpg",
    "D:\arucos\aruco11B.jpg",
    "D:\arucos\aruco12B.jpg",
    "D:\arucos\aruco13B.jpg",
    "D:\arucos\aruco14B.jpg",
    "D:\arucos\aruco15B.jpg",
    "D:\arucos\aruco16B.jpg",
    "D:\arucos\aruco17B.jpg",
    "D:\arucos\aruco18B.jpg",
    "D:\arucos\aruco19B.jpg",
    "D:\arucos\aruco20B.jpg",
    "D:\arucos\aruco21B.jpg",
    "D:\arucos\aruco22B.jpg",
    "D:\arucos\aruco23B.jpg",
    "D:\arucos\aruco24B.jpg",
    "D:\arucos\aruco25B.jpg",
    "D:\arucos\aruco26B.jpg",
    "D:\arucos\aruco27B.jpg",
    "D:\arucos\aruco28B.jpg",
    "D:\arucos\aruco29B.jpg",
    "D:\arucos\aruco30B.jpg",
    "D:\arucos\aruco31B.jpg",
    "D:\arucos\aruco32B.jpg",
    "D:\arucos\aruco33B.jpg",
    "D:\arucos\aruco34B.jpg",
    "D:\arucos\aruco35B.jpg",
    "D:\arucos\aruco36B.jpg",
    "D:\arucos\aruco37B.jpg",
    "D:\arucos\aruco38B.jpg",
    "D:\arucos\aruco39B.jpg",
    "D:\arucos\aruco40B.jpg",
    "D:\arucos\aruco41B.jpg",
    "D:\arucos\aruco42B.jpg",
    "D:\arucos\aruco43B.jpg",
    "D:\arucos\aruco44B.jpg",
    "D:\arucos\aruco45B.jpg",
    "D:\arucos\aruco46B.jpg",
    "D:\arucos\aruco47B.jpg"];

    //y_arr_far = [200.00,173.21,100.00,0.00,-100.00,-173.21,-200.00,-173.21,-100.00,0.00,100.00,173.21];
    //x_arr_far = [0.00,100.00,173.21,200.00,173.21,100.00,0.00,-100.00,-173.21,-200.00,-173.21,-100.00];
    
	// 200m
	y_arr_far = [193.19,141.42,51.76,-51.76,-141.42,-193.19,-193.19,-141.42,-51.76,51.76,141.42,193.19,193.19];
	x_arr_far = [51.76,141.42,193.19,193.19,141.42,51.76,-51.76,-141.42,-193.19,-193.19,-141.42,-51.76,51.76];
	// 20m from range(15,375,30)
	y_arr_close = [19.32,14.14,5.18,-5.18,-14.14,-19.32,-19.32,-14.14,-5.18,5.18,14.14,19.32,19.32];
	x_arr_close = [5.18,14.14,19.32,19.32,14.14,5.18,-5.18,-14.14,-19.32,-19.32,-14.14,-5.18,5.18];
	z_arr       = [2,50,120,190];


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// 20m from range(15,375,30)
	y_arr_close = [48.30,35.36,12.94,-12.94,-35.36,-48.30,-48.30,-35.36,-12.94,12.94,35.36,48.30,48,30];
	x_arr_close = [5.18,14.14,19.32,19.32,14.14,5.18,-5.18,-14.14,-19.32,-19.32,-14.14,-5.18,5.18];
	z_arr       = [10,50,120,190];

	// Create Tank
    ship_l = createSimpleObject["HAFM_Naval_RHIB", ( [2100,2600,10])];
	sleep 1;
	ship_l setVectorDirAndUp [[0,1,0], [0,0,1]];
    hint format ["number=%1 \n", position ship_l];
    sleep 1;
    ring = 0;
    while{ring<4} do
    {
        angle=15;
        num=0;
        while{num<12} do
        {
            texIdx = (ring*12)+num;
			pos = [(x_arr_far select num), (y_arr_far select num), (z_arr select ring)] vectorAdd position ship_l;
			block_l = createVehicle ["UserTexture10m_F",pos,[],0,"FLY"]; //"Land_VR_Block_04_F"
			asl_pos = getPosASL ship_l;
			pos set [2, (asl_pos select 2)+(z_arr select ring)];
			block_l setPosASL pos;

            block_l setObjectTexture [0, (acucoArray select texIdx)];
            block_l setDir(angle);
            angle = angle+30;
            hint format ["number=%1 \n", pos];
            sleep 0.1;
            num = num + 1;
        };
        ring = ring +1;
    };
    //block_l setObjectTexture [0, "#(rgb,8,8,3)color(0,1,0,0.01)"];//"C:\Users\user1\Pictures\testAruco.jpg"];
	// _target1 = "Land_VR_CoverObject_01_kneel_F" createVehicle [9544, 6307, 30];
	// _target1 setObjectTexture [0, "C:\Users\user1\Pictures\testAruco.jpg"];
	// 
	//cam = "camera" camCreate [9544, 6307, 20];
	//cam cameraEffect ["INTERNAL", "BACK"];
	// 
	// cam camSetPos [9504, 6307, 100];
	// cam camSetTarget _target1;
	//cam camCommit 0;
	//sleep .2;
	// screenshot "arma3screenshot.png";
};

// a3\boat_f\boat_armed_01\boat_armed_01_minigun_f.p3d
// a3\structures_f_bootcamp\vr\blocks\vr_block_04_f.p3d
// a3\soft_f\mrap_01\mrap_01_unarmed_f.p3d