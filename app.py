
import streamlit as st
import os
import json
import random
import time

# Load captions
with open("captions.json", "r") as f:
    all_captions = json.load(f)

st.title("🔊 Audio Caption Rating App")
username = st.text_input("Enter your name:", "")

if username:
    if not os.path.exists("ratings"):
        os.makedirs("ratings")

    st.write("Rate each caption (1–10). The order is randomized for each audio.")

    if "caption_mapping" not in st.session_state:
        st.session_state.caption_mapping = {}

    ratings = {}

    for audio_id, captions in all_captions.items():
        st.markdown(f"### 🎧 Audio {audio_id}")
        audio_path = f"audios/{audio_id}.wav"
        if os.path.exists(audio_path):
            audio_bytes = open(audio_path, "rb").read()
            st.audio(audio_bytes, format="audio/wav")
        else:
            st.warning(f"Missing audio file: {audio_path}")

        # Shuffle and store in session state
        if audio_id not in st.session_state.caption_mapping:
            shuffled = captions["gt"] + [captions["pred"]]
            roles = ["gt", "gt", "pred"]
            combined = list(zip(shuffled, roles))
            random.shuffle(combined)
            shuffled, roles = zip(*combined)
            st.session_state.caption_mapping[audio_id] = {"captions": shuffled, "roles": roles}
        else:
            shuffled = st.session_state.caption_mapping[audio_id]["captions"]
            roles = st.session_state.caption_mapping[audio_id]["roles"]

        ratings[audio_id] = []
        for idx, cap in enumerate(shuffled):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Caption {idx + 1}:** {cap}")
            with col2:
                key = f"{audio_id}_{idx}"
                val = st.slider(f"Rating for Caption {idx + 1}", 1, 10, 5, key=key)
                ratings[audio_id].append({
                    "text": cap,
                    "score": val,
                    "type": roles[idx]
                })

    if st.button("✅ Submit Ratings"):
        
        timestamp = int(time.time())
        filename = f"{username}_{timestamp}.json"
        filepath = f"ratings/{filename}"

        with open(filepath, "w") as f:
            json.dump(ratings, f, indent=2)
        st.success(f"Ratings saved as `{filepath}`")
