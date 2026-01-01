import cv2
import asyncio
import threading
import time
from queue import Queue
from input_and_preprocessing import starter_function, read_frames, part1, part2
from ws_client_server_insertDb import web_socket_server, web_socket_client, create_sqlite_db

video_path = r"C:\Users\DELL\Desktop\Elansol\elansol cv.mp4"

async def main_loop():

    video = cv2.VideoCapture(video_path)
    
    # get 1st frame to put in absdiff()
    _, background = starter_function(video)
    
    # thread the process of reading frames  
    frame_queue = Queue(maxsize=10)
    t = threading.Thread(target=read_frames, args=(video, frame_queue), daemon=True)
    t.start()

    prev_time = 0
    print("Vision System: Processing frames...")

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            
            #  FPS calculation
            new_time = time.time()
            duration = new_time - prev_time
            fps = 1 / duration if duration > 0 else 0
            prev_time = new_time
            
            # get contours and send via ws client to ws server
            contours = part1(frame, background)
            for c in contours:
                event_json = part2(c)
                if event_json:
                    await web_socket_client(event_json)

            # display the frame on screen
            display_frame = cv2.resize(frame, (640, 480))
            # display FPS
            cv2.putText(display_frame, f"FPS: {int(fps)}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Security Feed", display_frame)
        
        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
    print("Vision System: Shutting down.")

async def start_system():

    # 1. Initialize the SQLite database
    create_sqlite_db()
    
    # 2. 
    try:
        await asyncio.gather(
            # starts ws server at beginning for infinite time
            web_socket_server(),
            # uses part1(), part2(), display frame and fps
            main_loop()         
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(start_system()) 