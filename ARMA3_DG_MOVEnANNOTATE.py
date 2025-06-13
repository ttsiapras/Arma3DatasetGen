import numpy as np
import os
import os.path
from pathlib import Path
import time
import shutil
import csv
import glob
from ARMA3_DG_BB import get_BB_BackroundSubtraction,get_BB_FrameDiff
from ARMA3_DG_CLASSES import ARMA3_DG_vehiclesClasses
import cv2
from time import sleep

LAND = False


def genID():
    return(int(time.time()*10))

def move_file(src, dest):
    """ 
    Given a file 'src', move that file to the correct file specified by 'dest' 
    """
    # exit with error code 4 if this fails...
    img_moved = False
    while not img_moved:
        try:
            shutil.move(src, dest)
        except OSError as e:
            if e.errno == 13:
                # print('File move error caught with OSError.errno 13') #  for debugging
                # This sleep could be 0.2 secs but I don't want to use this high a sleep time.
                # Could be an issue if the user makes the camera rotation time too low
                time.sleep(0.1)
                continue
            # raise the exception if it is not this particular error
            print('ERROR:')
            print('The image file mover process has encountered some unknown error. Please restart the script.')
            print('See the python error description here:')
            print(e)
            exit(4)
        # explicitly raise any other exception type
        except Exception as weirdE:
            print('ERROR:')
            print('The image file mover process has encountered some unknown error. Please restart the script.')
            print('See the python error description here:')
            print(weirdE)
            exit(4)
        img_moved = True

def get_next_id(directory):
    """
    Get a folder, search for all files with integet as their name.
    Return the next integer in line.
    """
    existing_ids = []
    
    # Scan the directory for image files
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # You can add more extensions if needed
            try:
                # Extract the numeric ID from the filename (e.g., "1.jpg", "25.png")
                id_part = filename.split('.')[0]
                existing_ids.append(int(id_part))
            except ValueError:
                continue  # Skip if the filename doesn't have a valid integer ID
    
    # If there are existing IDs, get the next one
    next_id = max(existing_ids, default=0) + 1
    return next_id

def SearchAndMove_Empty(screenshot_path,dest_dir,verbose=False):
    # Using '*' pattern 
    for filepath in glob.glob(str(screenshot_path)+'/*empty.png'):
        # Make sure file is released
        try:
            os.rename(filepath, filepath)
        except:
            sleep(1.5)

        # Extract information from filename
        file_name = filepath.split('\\')[-1]
        print("SearchAndMove_Empty::Parsing"+file_name)
        try:
            filename_tokens = file_name.split('-')
            if(len(filename_tokens)!=7): raise Exception("Wrong number of tokens")
            world           = filename_tokens[0]
            c_x,c_y         = [float(coo) for coo in filename_tokens[1][1:-1].split(',') ]
            game_time       = int(filename_tokens[2])
            overcast        = float(filename_tokens[3])
            rain            = float(filename_tokens[4])
            fog             = float(filename_tokens[5])
        except:
            print("Problem parsing name of :"+file_name)
            os.remove(filepath)
            return
        
        # Move to world directory
        dest_dir_path = dest_dir / Path('samples_negative')
        if not Path.exists(dest_dir_path):
            os.makedirs(str(dest_dir_path), 0o777)  # create the directory if it doesnt exist
        if(verbose): print("SearchAndMove_Empty::DestinationDir::"+str(dest_dir_path))
        # Get Ascending ID
        ID = genID()

        # Find or create Annotation File
        annotation_file = dest_dir_path / Path('AnnotationData.csv')
        if not annotation_file.exists():
            annotation_csv = open(annotation_file, 'w+', newline='')
            annotation_writer = csv.writer(annotation_csv)
            annotation_writer.writerow(['id','World','c_x','c_y','Sensor','game_time(ex. 13.5 = 1:30 pm)','overcast [0:1]','rain [0:1]','fog [0:1]','orig_file'])
            annotation_csv.close()
            if(verbose): print("SearchAndMove_Empty::InitialisedAnnotationFile")
            
        # Open to append data
        annotation_csv = open(annotation_file, 'a', newline='')
        annotation_writer = csv.writer(annotation_csv)
        data = [ID,world,c_x,c_y,'Vis',game_time,overcast,rain,fog,file_name]
        annotation_writer.writerow(data)
        annotation_csv.close()
        if(verbose): print("SearchAndMove_Empty::Annotation::"+str(data))

        dest_dir_path = dest_dir_path / Path(f'%06ld.png'%(ID))
        move_file(filepath, dest_dir_path)
        if(verbose): print("AnnotateAndMove_Full::Moved::"+str(filepath))

def SearchAnnotateAndMove_Full(screenshot_path,dest_dir,copies=4,showIntermediate=False,verbose=False):
    """
    Search for sull set of produced data. If found, find the object by comparins images and save the results 
    in the appropriate folder. Then remove the excess files.
    """
    # Check if the last file of the set is has been ganarated
    for fullSet_lastImage in glob.glob(str(screenshot_path)+f'/*%d-wout.png'%copies):
        # Make sure file is released
        try:
            os.rename(fullSet_lastImage, fullSet_lastImage)
        except:
            sleep(1.5)

        if("Extract information from filename"):
            try:
                file_name = fullSet_lastImage.split('\\')[-1]
                print("Parsing :",file_name)
                prefix = ('-'.join(file_name.split('-')[:-2]))
                filename_tokens = file_name.split('-')
                if(len(filename_tokens)!=10): raise Exception("Bad number of tokens")
                idx             = 0
                world           = filename_tokens[idx]; idx+=1
                v_name          = filename_tokens[idx]; idx+=1
                v_x,v_y         = [float(coo) for coo in filename_tokens[idx][1:-1].split(',') ]; idx+=1
                c_x,c_y         = [float(coo) for coo in filename_tokens[idx][1:-1].split(',') ]; idx+=1
                game_time       = int(filename_tokens[idx]); idx+=1
                overcast        = float(filename_tokens[idx]); idx+=1
                rain            = float(filename_tokens[idx]); idx+=1
                fog             = float(filename_tokens[idx]); idx+=1
                if(v_name not in ARMA3_DG_vehiclesClasses.keys()):
                    v_class = 'NA'
                else:
                    v_class = ARMA3_DG_vehiclesClasses[v_name]
            except Exception  as e:
                print(e)
                f = open(logFile,'a')
                f.write("Parsing Error:"+file_name+'\n')
                f.close()
                print("Parsing Error:"+file_name)
                print("Deleting file set")
                for image in glob.glob(str(screenshot_path)+'\\'+file_name[:-10]+'*.png'):
                    print(image)
                    try:
                        os.remove(image)
                    except:
                        sleep(1.5)
                        os.remove(image)
                return
        if("Check all files exist"):
            print("AnnotateAndMove_Full::cheking that full set exists.",end='::')
            valid_paths_with = []
            valid_paths_wout = []
            set_exists = True
            for copy in range(copies):
                idx = copy+1
                check_path_with = screenshot_path / Path(prefix+f'-%d-with.png'%idx)
                check_path_wout = screenshot_path / Path(prefix+f'-%d-wout.png'%idx)
                if (not check_path_with.exists() or not check_path_with.exists()):
                    set_exists = False
                    break
                else:
                    valid_paths_with.append(check_path_with)
                    valid_paths_wout.append(check_path_wout)
            
            if(not set_exists):
                print("Incomplete Set::Breaking")
                for image in glob.glob(str(screenshot_path)+'\\'+file_name[:-11]+'*.png'):
                    try:
                        os.remove(image)
                    except:
                        sleep(1.5)
                        os.remove(image)
                return
            else:
                print("Complete Set")

        if("Get Bounding box for images"):
            if(set_exists):
                if LAND:
                    BB = get_BB_BackroundSubtraction(valid_paths_wout,valid_paths_with,inclussionDiameter=350,open_mask=True,showIntermediate=showIntermediate)
                else:
                    BB = get_BB_FrameDiff(valid_paths_wout,valid_paths_with,inclussionDiameter=900,showIntermediate=showIntermediate)
            objectFound = (BB is not None)
            if(objectFound):
                if(verbose): print("AnnotateAndMove_Full::Object located::",BB)
                BB = np.array(BB)+[-7,-7,14,14] # Scale up the BB to encaptulate more
                TL = (BB[0], BB[1])
                TR = (BB[0] + BB[2], BB[1])
                BL = (BB[0], BB[1] + BB[3])
                BR = (BB[0] + BB[2], BB[1] + BB[3])
                marked = cv2.rectangle(cv2.imread(valid_paths_with[-1],1), TL, BR, (255, 0, 0), 2)
            else:
                if(verbose): print("AnnotateAndMove_Full::Object not located")
                TL=TR=BL=BR=(-1,-1)
            
        if("Get appropriate world directory"):
            # Move to world directory
            if objectFound:
                dest_dir_path = dest_dir / Path('samples_positive')
            else:
                dest_dir_path = dest_dir / Path('samples_inconclusive')
            if not Path.exists(dest_dir_path):
                os.makedirs(str(dest_dir_path), 0o777)  # create the directory if it doesnt exist
            if(verbose): print("AnnotateAndMove_Full::DestinationDir::"+str(dest_dir_path))
            
        if("Produce new ID"):
            # Get Ascending ID
            ID = genID()
            if(verbose): print("AnnotateAndMove_Full::NewID::"+str(ID))

        if("Initialize Annotation file if required"):
            annotation_file = dest_dir_path / Path('AnnotationData.csv')
            if not annotation_file.exists():
                annotation_csv = open(annotation_file, 'w+', newline='')
                annotation_writer = csv.writer(annotation_csv)
                annotation_writer.writerow(['id','World','TL','TR','BR','BL','v_name','v_class','v_x','v_y','c_x','c_y','Sensor','game_time(ex. 13.5 = 1:30 pm)','overcast [0:1]','rain [0:1]','fog [0:1]','orig_file'])
                annotation_csv.close()
                if(verbose): print("AnnotateAndMove_Full::InitialisedAnnotationFile")

        if("Append annoatation data"):
            annotation_csv = open(annotation_file, 'a', newline='')
            annotation_writer = csv.writer(annotation_csv)
            data = [ID,world,TL,TR,BR,BL,v_name,v_class,v_x,v_y,c_x,c_y,'Vis',game_time,overcast,rain,fog,file_name];
            annotation_writer.writerow(data)
            annotation_csv.close()
            if(verbose): print("AnnotateAndMove_Full::Annotation::"+str(data))

        if("Now move files to appropriate folder"):
            if(objectFound):
                #move one blank(PNG), one with the object(PNG) and the marked resized(JPG)
                # With Object
                dest_path = dest_dir_path / Path(f'%06ld.png'%(ID))
                move_file(valid_paths_with[-1], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(valid_paths_with[-1]))
                # Blank
                dest_path = dest_dir_path / Path(f'%06ld_blank.png'%(ID))
                move_file(valid_paths_wout[-1], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(valid_paths_wout[-1]))
                # Marked
                dest_path = dest_dir_path / Path(f'%06ld_marked.jpg'%(ID))
                cv2.imwrite(dest_path,marked)
                if(verbose): print("AnnotateAndMove_Full::Stored::"+str(dest_path))
                # Delete the rest
                for srcpath in valid_paths_wout[:-1]:
                    os.remove(srcpath)
                    if(verbose): print("AnnotateAndMove_Full::Removed::"+str(srcpath))
                for srcpath in valid_paths_with[:-1]:
                    os.remove(srcpath)
                    if(verbose): print("AnnotateAndMove_Full::Removed::"+str(srcpath))
            else:
                file_name = str(valid_paths_wout[0]).split('\\')[-1]
                dest_path = dest_dir_path / Path(file_name)
                move_file(valid_paths_wout[0], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(file_name))
                file_name = str(valid_paths_with[0]).split('\\')[-1]
                dest_path = dest_dir_path / Path(file_name)
                move_file(valid_paths_with[0], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(file_name))
                for srcpath in valid_paths_wout[1:]:
                    os.remove(srcpath)
                    if(verbose): print("AnnotateAndMove_Full::Removed::"+str(srcpath))
                for srcpath in valid_paths_with[1:]:
                    os.remove(srcpath)
                    if(verbose): print("AnnotateAndMove_Full::Removed::"+str(srcpath))

def SearchAnnotateAndMove_Full_VR(screenshot_path,dest_dir,showIntermediate=False,verbose=False):
    """
    Search for sull set of produced data. If found, find the object by comparins images and save the results 
    in the appropriate folder. Then remove the excess files.
    """
    # Check if the last file of the set is has been ganarated
    for fullSet_lastImage in glob.glob(str(screenshot_path)+f'/*0-wout.png'):
        # Make sure file is released
        try:
            os.rename(fullSet_lastImage, fullSet_lastImage)
        except:
            sleep(2)

        if("Extract information from filename"):
            try:
                file_name = fullSet_lastImage.split('\\')[-1]
                print("Parsing :",file_name)
                prefix = ('-'.join(file_name.split('-')[:-2]))
                filename_tokens = file_name.split('-')
                if(len(filename_tokens)!=10): raise Exception("Bad number of tokens")
                idx             = 0
                world           = filename_tokens[idx]; idx+=1
                v_name          = filename_tokens[idx]; idx+=1
                v_x,v_y         = [float(coo) for coo in filename_tokens[idx][1:-1].split(',') ]; idx+=1
                c_x,c_y         = [float(coo) for coo in filename_tokens[idx][1:-1].split(',') ]; idx+=1
                game_time       = int(filename_tokens[idx]); idx+=1
                overcast        = float(filename_tokens[idx]); idx+=1
                rain            = float(filename_tokens[idx]); idx+=1
                fog             = float(filename_tokens[idx]); idx+=1
                if(v_name not in ARMA3_DG_vehiclesClasses.keys()):
                    v_class = 'NA'
                else:
                    v_class = ARMA3_DG_vehiclesClasses[v_name]
            except Exception  as e:
                print(e)
                f = open(logFile,'a')
                f.write("Parsing Error:"+file_name+'\n')
                f.close()
                print("Parsing Error:"+file_name)
                print("Deleting file set")
                for image in glob.glob(str(screenshot_path)+'\\'+file_name[:-10]+'*.png'):
                    print(image)
                    try:
                        os.remove(image)
                    except:
                        sleep(1.5)
                        os.remove(image)
                return
            
        if("Check all files exist"):
            print("AnnotateAndMove_Full::cheking that full set exists.",end='::')
            valid_paths_with = []
            valid_paths_wout = []
            set_exists = True

            check_path_with = screenshot_path / Path(prefix+f'-0-with.png')
            check_path_wout = screenshot_path / Path(prefix+f'-0-wout.png')
            if (not check_path_with.exists() or not check_path_with.exists()):
                set_exists = False
                break
            else:
                valid_paths_with.append(check_path_with)
                valid_paths_wout.append(check_path_wout)
            
            if(not set_exists):
                print("Incomplete Set::Breaking")
                for image in glob.glob(str(screenshot_path)+'\\'+file_name[:-11]+'*.png'):
                    try:
                        os.remove(image)
                    except:
                        sleep(1.5)
                        os.remove(image)
                return
            else:
                print("Complete Set")

        if("Get Bounding box for images"):
            if(set_exists):
                BB = get_BB_BackroundSubtraction(valid_paths_wout,valid_paths_with,inclussionDiameter=1000,open_mask=True,showIntermediate=showIntermediate)
            objectFound = (BB is not None)
            if(objectFound):
                if(verbose): print("AnnotateAndMove_Full::Object located::",BB)
                BB = np.array(BB)+[-7,-7,14,14] # Scale up the BB to encaptulate more
                TL = (BB[0], BB[1])
                TR = (BB[0] + BB[2], BB[1])
                BL = (BB[0], BB[1] + BB[3])
                BR = (BB[0] + BB[2], BB[1] + BB[3])
                marked = cv2.rectangle(cv2.imread(valid_paths_with[-1],1), TL, BR, (255, 0, 0), 2)
            else:
                os.remove(valid_paths_wout[0])
                os.remove(valid_paths_with[0])
                if(verbose): print("AnnotateAndMove_Full::Object not located:: Deleting images")
                TL=TR=BL=BR=(-1,-1)
            
        if("Get appropriate world directory"):
            # Move to world directory
            if objectFound:
                dest_dir_path = dest_dir / Path('samples_positive_VR')
                if not Path.exists(dest_dir_path):
                    os.makedirs(str(dest_dir_path), 0o777)  # create the directory if it doesnt exist
            
        if("Produce new ID"):
            # Get Ascending ID
            ID = genID()

        if("Initialize Annotation file if required"):
            if objectFound:
                annotation_file = dest_dir_path / Path('AnnotationData.csv')
                if not annotation_file.exists():
                    annotation_csv = open(annotation_file, 'w+', newline='')
                    annotation_writer = csv.writer(annotation_csv)
                    annotation_writer.writerow(['id','World','TL','TR','BR','BL','v_name','v_class','v_x','v_y','c_x','c_y','Sensor','game_time(ex. 13.5 = 1:30 pm)','overcast [0:1]','rain [0:1]','fog [0:1]','orig_file'])
                    annotation_csv.close()
                    if(verbose): print("AnnotateAndMove_Full::InitialisedAnnotationFile")

        if("Append annoatation data"):
            if objectFound:
                annotation_csv = open(annotation_file, 'a', newline='')
                annotation_writer = csv.writer(annotation_csv)
                data = [ID,world,TL,TR,BR,BL,v_name,v_class,v_x,v_y,c_x,c_y,'Vis',game_time,overcast,rain,fog,file_name];
                annotation_writer.writerow(data)
                annotation_csv.close()
                if(verbose): print("AnnotateAndMove_Full::Annotation::"+str(data))

        if("Now move files to appropriate folder"):
            if(objectFound):
                #move one blank(PNG), one with the object(PNG) and the marked resized(JPG)
                # With Object
                dest_path = dest_dir_path / Path(f'%06ld.png'%(ID))
                move_file(valid_paths_with[0], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(valid_paths_with[-1]))
                # Blank
                dest_path = dest_dir_path / Path(f'%06ld_blank.png'%(ID))
                move_file(valid_paths_wout[0], dest_path)
                if(verbose): print("AnnotateAndMove_Full::Moved::"+str(valid_paths_wout[-1]))
                # Marked
                dest_path = dest_dir_path / Path(f'%06ld_marked.jpg'%(ID))
                cv2.imwrite(dest_path,marked)
                if(verbose): print("AnnotateAndMove_Full::Stored::"+str(dest_path))


if __name__ == '__main__':
    global logFile

    logFile         = Path(os.path.expanduser('D:\\synthetic_dataset\\arma\\log.txt'))
    screenshot_path = Path(os.path.expanduser('~\\Documents\\Arma 3\\Screenshots'))
    if(LAND):
        dest_dir = Path(os.path.expanduser('D:\\synthetic_dataset\\arma'))
        copies= 3
    else:
        dest_dir = Path(os.path.expanduser('D:\\synthetic_dataset\\arma\\sea'))
        copies= 4

    while(1):
        time.sleep(1)
        SearchAndMove_Empty(screenshot_path,dest_dir,verbose=False)
        SearchAnnotateAndMove_Full(screenshot_path,dest_dir,copies=copies,showIntermediate=True,verbose=True)
        SearchAnnotateAndMove_Full_VR(screenshot_path,dest_dir,showIntermediate=True,verbose=False)
        for image in glob.glob(str(screenshot_path)+f'/*%d-wout.png'%(copies+1)):
            try:
                os.remove(image)
            except:
                pass
