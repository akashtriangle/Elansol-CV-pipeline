APPROACH
I recorded a 23 second video of me waving my hands 3 times in it, it was recorded through my laptop's webcam.
I used OpenCV to read the video as instructed in assignment instructions, also OpenCV is tool used commonly in industry for Computer Vision. OpenCV was used to read through frames of video, to apply preprocessing steps like resizing,  detecting contours etc. Based on the contours, I detected event which I converted to json to transmit over network to backend. 
The data flows as: json events ->  web socket client -> web socket server -> database. For this purpose I created websocket client and server.  Since this part of assignment happens outside code in the network, it can be slow and can create bottleneck. So I used async programming.
In order to store the json events I used SQLite. I created it via code and made function to insert data in SQLite. 
I used datetime module, calculated and displayed fps.

SETUP STEPS
I have included requirements.txt file which you can use to create a separate environment on your system.
pip install -r requirements.txt
I have included all code structured in folders and file here itself in repository. Download all files and create parent folder. Traverse to this folder on terminal. Then  just type 'python main.py' . Once done press 'q' to exit completely. You will see result. You can replace path of your video in video_path variable in main.py detect motion in your own video.

ASSUMPTIONS
I assumed that that first frame of video does not have motion. I assumed all videos will be clear and not very dirty and would not require a lot of preprocessing. I assumed the video would not be recorded in very high pixel definition.

IMPROVEMENT
I could have made code to make quality checks on the flow and apply preprocessing dynamically without needing manual work .I could have used Kafka for higher throughput . I can use real time videos like CCTV etc. I could have used AI model like YOLO etc.