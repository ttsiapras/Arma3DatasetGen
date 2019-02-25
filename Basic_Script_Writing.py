def script(pos, cc, angle, file):
    f = open(file, "w+")
    f.write('pos1 = player modelToWorld [0,5,5];\n')
    f.write('cam = "camera" camCreate pos1;\n')
    f.write('cam cameraEffect ["INTERNAL", "BACK"];\n\n')
    f.write('angleface = 0;\n')
    f.write('fogvalue = 0;\n')
    f.write('angle = %d;\n\n' % angle)
    f.write('0 = [] spawn\n')
    f.write('{\n')
    f.write('\twhile {fogvalue < .8} do\n')
    f.write('\t{\n')
    f.write('\t\twhile {angleface < 360} do\n')
    f.write('\t\t{\n')
    f.write('\t\t\twaitUntil {camCommitted cam};\n')
    f.write('\t\t\tscreenshot "arma3screenshot.png";\n')
    for idx, val in enumerate(pos):
        f.write('\t\t\tpos%d = player modelToWorld [%d,%d,%d];\n' % (idx + 2, pos[idx][0], pos[idx][1], pos[idx][2]))
        f.write('\t\t\tcam camSetPos pos%s;\n' % str(int(idx)+2))
        f.write('\t\t\tcam camSetDir (pos%s vectorFromTo pos1);\n' % str(int(idx)+2))
        f.write('\t\t\tcam camCommit %d;\n' % cc)
        f.write('\t\t\twaitUntil {camCommitted cam};\n')
        f.write('\t\t\tscreenshot "arma3screenshot.png";\n\n')
    f.write('\t\t\tangleface = angleface+angle;\n')
    f.write('\t\t\tunit1 setDir angleface;\n')
    f.write('\t\t\tsleep %d;\n' % cc)
    f.write('\t\t};\n')
    f.write('\tfogvalue = fogvalue + .2;\n')
    f.write('\t1 setfog fogvalue;\n')
    f.write('\tsleep %d;\n' % cc)
    f.write('\tangleface = 0;\n')
    f.write('\t};\n')
    f.write('};\n')
    f.close()


#script([(1, 2, 3), (4, 5, 6), (7, 8, 9)], 6)
