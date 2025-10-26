import streamlit as st
import cv2
import pandas as pd
import time
import threading
import smtplib
from email.message import EmailMessage
from playsound import playsound
from tagger import ObjectDetector

st.set_page_config(page_title="Aranyaksh Surveillance", layout="wide")

ANIMAL_MODEL_PATH = "animal_model.pt"
FIRE_MODEL_PATH = "best.pt"

# --- Sound Alert Configuration ---
SOUND_MAPPING = {
    "lion": "lion_alert.mp3",
    "bear": "bear_alert.mp3",
    "fire": "fire_alert.mp3"
}
SOUND_COOLDOWN_SECONDS = 00
EMAIL_COOLDOWN_SECONDS = 60 # Cooldown for email alerts (1 minute)

if "last_played" not in st.session_state:
    st.session_state.last_played = {key: 0 for key in SOUND_MAPPING}
if "last_email_sent" not in st.session_state:
    st.session_state.last_email_sent = 0

def play_alert_sound(filepath):
    try:
        playsound(filepath)
    except Exception as e:
        print(f"Error playing sound: {e}")

def send_email_alert():
    try:
        creds = st.secrets["email_credentials"]
        msg = EmailMessage()
        msg.set_content("A fire has been detected by the Aranyaksh Ornithopter Surveillance System. Please review the live feed immediately.")
        msg['Subject'] = '!!! FIRE ALERT !!!'
        msg['From'] = creds["ornithopter_alert@gmail.com"]
        msg['To'] = creds["arjunramkumar.menon2023@vitstudent.ac.in"]

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(creds["ornithopter_alert@gmail.com"], creds["aranyaksh"])
        server.send_message(msg)
        server.quit()
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@st.cache_resource
def load_detector():
    try:
        detector = ObjectDetector(ANIMAL_MODEL_PATH, FIRE_MODEL_PATH)
        return detector
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

detector = load_detector()

st.markdown("<h1 style='text-align: center;'>🦅 Aranyaksh Ornithopter Surveillance</h1>", unsafe_allow_html=True)
st.sidebar.header("Configuration")

if "detection_log" not in st.session_state:
    st.session_state.detection_log = pd.DataFrame(columns=["Object", "Confidence"])

if detector:
    confidence_thresh = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.70, 0.05)
    detector.confidence_threshold = confidence_thresh
    
    run = st.sidebar.checkbox('Run Surveillance', value=True)
    
    st.sidebar.header("Log Management")
    csv = st.session_state.detection_log.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("Download Log as CSV", csv, "detection_log.csv", "text/csv")

    if st.sidebar.button("Clear Detection Log"):
        st.session_state.detection_log = pd.DataFrame(columns=["Object", "Confidence"])
        st.toast("Detection log cleared!")
        st.rerun() # <<< THIS IS THE CORRECTED LINE

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Live Camera Feed")
        FRAME_WINDOW = st.image([])

    with col2:
        st.subheader("Live Metrics")
        fps_metric = st.empty()
        detections_count_metric = st.empty()
        
        st.subheader("Detection Log")
        LOG_WINDOW = st.dataframe(st.session_state.detection_log, height=300)

    camera = cv2.VideoCapture(1) 
    frame_count = 0
    total_detections = 0
    start_time = time.time()

    while run:
        ret, frame = camera.read()
        if not ret:
            st.warning("Failed to capture image from camera.")
            break
        
        frame_count += 1
        processed_frame, frame_detections = detector.process_frame(frame)
        
        if frame_detections:
            total_detections += len(frame_detections)
            new_log_entries = pd.DataFrame(frame_detections)
            st.session_state.detection_log = pd.concat([new_log_entries, st.session_state.detection_log], ignore_index=True)
            
            current_time = time.time()
            for detection in frame_detections:
                object_name = detection["Object"].lower()
                if object_name in SOUND_MAPPING:
                    last_played_time = st.session_state.last_played[object_name]
                    if (current_time - last_played_time) > SOUND_COOLDOWN_SECONDS:
                        st.session_state.last_played[object_name] = current_time
                        sound_file = SOUND_MAPPING[object_name]
                        threading.Thread(target=play_alert_sound, args=(sound_file,)).start()
                
                if object_name == "fire":
                    if (current_time - st.session_state.last_email_sent) > EMAIL_COOLDOWN_SECONDS:
                        st.session_state.last_email_sent = current_time
                        threading.Thread(target=send_email_alert).start()
                        st.toast("🔥 FIRE DETECTED! Sending email alert... 🔥")

            max_log_size = 20
            if len(st.session_state.detection_log) > max_log_size:
                st.session_state.detection_log = st.session_state.detection_log.head(max_log_size)

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            fps_metric.metric("Frames Per Second", f"{fps:.2f}")

        detections_count_metric.metric("Total Detections", f"{total_detections}")
        LOG_WINDOW.dataframe(st.session_state.detection_log, height=300)
        
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(processed_frame_rgb)
    else:
        st.warning('Surveillance is stopped. Check the "Run Surveillance" box to begin.')

else:
    st.warning("Models could not be loaded. Please check the model paths and restart.")

if 'camera' in locals() and camera.isOpened():
    camera.release()