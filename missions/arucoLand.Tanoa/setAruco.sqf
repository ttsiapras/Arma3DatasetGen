0 = [] spawn
{
    acucoArray = ["C:\Users\user1\Pictures\arucos\aruco00B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco01B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco02B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco03B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco04B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco05B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco06B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco07B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco08B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco09B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco10B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco11B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco12B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco13B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco14B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco15B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco16B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco17B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco18B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco19B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco20B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco21B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco22B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco23B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco24B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco25B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco26B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco27B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco28B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco29B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco30B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco31B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco32B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco33B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco34B.jpg",
    "C:\Users\user1\Pictures\arucos\aruco35B.jpg"];

    y_arr = [200.00,173.21,100.00,0.00,-100.00,-173.21,-200.00,-173.21,-100.00,0.00,100.00,173.21];
    x_arr = [0.00,100.00,173.21,200.00,173.21,100.00,0.00,-100.00,-173.21,-200.00,-173.21,-100.00];
    z_arr = [20,45,80];

    // Create the required vehicle
    boat_l = "B_T_Boat_armed_01_minigun_F" createVehicle [9544, 6307, 0];
    hint format ["number=%1 \n", position boat_l];
    sleep 2;

    ring = 0;
    while{ring<3} do
    {
        angle=0;
        num=0;
        while{num<12} do
        {
            texIdx = (ring*12)+num;
            pos = [(x_arr select num), (y_arr select num), (z_arr select ring)] vectorAdd position boat_l;
            block_l = createVehicle ["UserTexture10m_F",pos,[],0,"FLY"]; //"Land_VR_Block_04_F"
            block_l setObjectTexture [0, (acucoArray select texIdx)];
            block_l setDir(angle);
            angle = angle+30;
            hint format ["number=%1 \n", pos];
            sleep 0.2;
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