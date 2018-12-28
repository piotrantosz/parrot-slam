# parrot ar marker follow
Parrot AR 2.0 drone software for following AR markers

## Configuration
To use _ps_drone.py_ on mac:

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
    
Using python 2.7 because of ps_drone.py. It's old and it sucks. But it also exist.
    
## Run
drone control api

    python api/ps_drone.py

video capture / tracker

    python video_capture.py cascade.xml
    
