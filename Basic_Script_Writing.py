def script(pos, cc, angle):
    print('pos1 = player modelToWorld [0,5,5];')
    print('cam = "camera" camCreate pos1;')
    print('cam cameraEffect ["INTERNAL", "BACK"];\n')
    print('angleface = 0;')
    print('angle = %d;\n' % angle)
    print('0 = [] spawn')
    print('{')
    print('\twhile {angle <= 360} do')
    print('\t{')
    print('\t\twaitUntil {camCommitted cam};')
    print('\t\tscreenshot "";')
    for idx, val in enumerate(pos):
        print('\t\tpos%d = player modelToWorld [%d,%d,%d];' % (idx + 2, pos[idx][0], pos[idx][1], pos[idx][2]))
        print('\t\tcam camSetPos pos%s;' % str(int(idx)+2))
        print('\t\tcam camSetDir (pos%s vectorFromTo pos1);' % str(int(idx)+2))
        print('\t\tcam camCommit %d;' % cc)
        print('\t\twaitUntil {camCommitted cam};')
        print('\t\tscreenshot "";\n')
    print('\t\tunit1 setDir angleface;')
    print('\t\tsleep %d;' % cc)
    print('\t\tangleface = angleface+angle;')
    print('\t};')
    print('};')
