from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


# ----------------------------------------
# Load Voice Encoder
# ----------------------------------------

@st.cache_resource
def load_voice_encoder():

    # Load and cache the Resemblyzer voice encoder
    try:
        return VoiceEncoder()

    except Exception as e:
        st.error(f"Unable to load voice encoder: {e}")
        return None


# ----------------------------------------
# Generate Voice Embedding
# ----------------------------------------

def get_voice_embedding(audio_bytes):

    # Convert audio data into a voice embedding
    try:

        # Load the voice encoder
        encoder = load_voice_encoder()

        if encoder is None:
            return None

        # Load audio and resample it to 16 kHz
        audio, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # Preprocess the audio for Resemblyzer
        wav = preprocess_wav(audio)

        # Generate the speaker embedding
        embedding = encoder.embed_utterance(wav)

        # Convert NumPy array to list for database storage
        return embedding.tolist()

    except Exception as e:

        # Handle voice processing errors
        st.error(f'Voice Recognition Error: {e}')
        return None


# ----------------------------------------
# Identify Speaker
# ----------------------------------------

def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65
):

    # Check whether a valid embedding and candidates are available
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    # ----------------------------------------
    # Compare With Candidate Speakers
    # ----------------------------------------

    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding:

            try:

                # Calculate similarity between voice embeddings
                similarity = np.dot(
                    new_embedding,
                    stored_embedding
                )

                # Keep the speaker with the highest similarity
                if similarity > best_score:
                    best_score = similarity
                    best_sid = sid

            except Exception as e:

                # Skip invalid speaker embeddings
                print(
                    f"Speaker comparison failed for {sid}: {e}"
                )
                continue

    # ----------------------------------------
    # Apply Similarity Threshold
    # ----------------------------------------

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score


# ----------------------------------------
# Process Bulk Audio
# ----------------------------------------

def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65
):

    # Process classroom audio and identify speakers
    try:

        # Load the voice encoder
        encoder = load_voice_encoder()

        if encoder is None:
            return {}

        # ----------------------------------------
        # Load Audio
        # ----------------------------------------

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # ----------------------------------------
        # Detect Speech Segments
        # ----------------------------------------

        segments = librosa.effects.split(
            audio,
            top_db=30
        )

        identified_results = {}

        # ----------------------------------------
        # Process Each Audio Segment
        # ----------------------------------------

        for start, end in segments:

            # Ignore very short audio segments
            if (end - start) < sr * 0.5:
                continue

            # Extract the current audio segment
            segment_audio = audio[start:end]

            # Preprocess the audio segment
            wav = preprocess_wav(segment_audio)

            # Generate voice embedding
            embedding = encoder.embed_utterance(wav)

            # ----------------------------------------
            # Identify Speaker
            # ----------------------------------------

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            # ----------------------------------------
            # Store Best Speaker Score
            # ----------------------------------------

            if sid:

                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):
                    identified_results[sid] = score

        return identified_results

    except Exception as e:

        # Handle bulk audio processing errors
        st.error(f'Bulk process error: {e}')
        return {}