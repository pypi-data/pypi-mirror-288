from .utils import record_user, record_interruption, record_user_stream
from .vad import VoiceActivityDetection
import re
from time import monotonic
import numpy as np
from threading import Thread
from queue import Queue
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

TIMING = int(os.environ.get('TIMING', 0))
TIMING_PATH = os.environ.get('TIMING_PATH', 'times.csv')


class BaseEar:
    def __init__(self, silence_seconds=2,
                 not_interrupt_words=None,
                 listener=None,
                 stream=False):
        if not_interrupt_words is None:
            not_interrupt_words = ['you', 'yes', 'yeah', 'hmm']  # you because whisper says "you" in silence
        self.silence_seconds = silence_seconds
        self.not_interrupt_words = not_interrupt_words
        self.vad = VoiceActivityDetection()
        self.listener = listener
        self.stream = stream
        if TIMING:
            if not os.path.exists(TIMING_PATH):
                columns = ['Model', 'Time Taken']
                df = pd.DataFrame(columns=columns)
                df.to_csv(TIMING_PATH, index=False)

    def transcribe(self, input_audio: np.ndarray) -> str:
        '''

        :param input_audio:
        :return: transcription
        '''
        raise NotImplementedError("This method should be implemented by the subclass")

    def transcribe_stream(self, audio_queue: Queue, transcription_queue: Queue):
        '''
        :param audio_queue: Queue containing audio chunks from pyaudio stream
        :param transcription_queue: Queue to put transcriptions
        '''
        raise NotImplementedError("This method should be implemented by the subclass")

    def _sim_transcribe_stream(self, input_audio: np.ndarray) -> str:
        """
        Simulates the transcribe stream using a single audio input
        :param input_audio: fp32 numpy array of the audio
        :return: transcription
        """
        audio_queue = Queue()
        transcription_queue = Queue()

        input_buffer = (input_audio * (1 << 15)).astype(np.int16).tobytes()
        audio_queue.put(input_buffer)
        audio_queue.put(None)
        transcription_thread = Thread(target=self.transcribe_stream, args=(audio_queue, transcription_queue))
        transcription_thread.start()
        transcription_thread.join()
        text = ''
        while True:
            _ = transcription_queue.get()
            if _ is None:
                break
            text += _ + ' '
        return text

    def _listen(self) -> str:
        """
        :return: transcription
        records audio using record_user and returns its transcription
        """
        import pysbd
        sentence_finished = False
        first = True
        audio = np.zeros(0, dtype=np.float32)
        while not sentence_finished:
            new_audio = record_user(self.silence_seconds, self.vad,
                                     self.listener, started=not first)
            audio = np.concatenate((audio, new_audio), 0)
            if TIMING and first:
                start_time = monotonic()

                text = self.transcribe(audio)

                stop_time = monotonic()
                time_diff = stop_time - start_time
                new_row_df = pd.DataFrame([{'Model': 'STT', 'Time Taken': time_diff}])
                new_row_df.to_csv(TIMING_PATH, mode='a', header=False, index=False)
            else:
                text = self.transcribe(audio)
            first = False
            seg = pysbd.Segmenter(language="en", clean=False)
            if len(seg.segment(text + ' .')) > 1:
                sentence_finished = True
        return text

    def _listen_stream(self) -> str:
        '''
        :return: transcription
        records audio using record_user and returns its transcription
        '''

        audio_queue = Queue()
        transcription_queue = Queue()

        audio_thread = Thread(target=record_user_stream, args=(self.silence_seconds,
                                                               self.vad, audio_queue, self.listener))
        transcription_thread = Thread(target=self.transcribe_stream, args=(audio_queue, transcription_queue))

        audio_thread.start()
        transcription_thread.start()

        if TIMING:
            audio_thread.join()
            start_time = monotonic()

            transcription_thread.join()
            text = ''
            while True:
                _ = transcription_queue.get()
                if _ is None:
                    break
                text += _ + ' '

            stop_time = monotonic()
            time_diff = stop_time - start_time
            new_row_df = pd.DataFrame([{'Model': 'STT', 'Time Taken': time_diff}])
            new_row_df.to_csv(TIMING_PATH, mode='a', header=False, index=False)
        else:
            text = ''
            while True:
                _ = transcription_queue.get()
                if _ is None:
                    break
                text += _ + ' '
        audio_thread.join()
        transcription_thread.join()
        return text

    def listen(self) -> str:
        '''
        :return: transcription
        records audio using record_user and returns its transcription
        '''
        if self.stream:
            return self._listen_stream()
        else:
            return self._listen()

    def interrupt_listen(self, record_seconds=100) -> str:
        """
        Records audio with interruption. Transcribes audio if
        voice activity detected and returns True if transcription indicates
        interruption.

        :param record_seconds: Max seconds to record for
        :return: boolean indicating the if an interruption occured
        """
        while record_seconds > 0:
            interruption_audio = record_interruption(self.vad, record_seconds, streamer=self.listener)
            # duration of interruption audio
            if interruption_audio is None:
                return ''
            else:
                duration = len(interruption_audio) / 16_000
                if self.stream:
                    text = self._sim_transcribe_stream(interruption_audio)
                else:
                    text = self.transcribe(interruption_audio)
                # remove any punctuation using re
                text = re.sub(r'[^\w\s]', '', text)
                text = text.lower()
                text = text.strip()
                if text in self.not_interrupt_words:
                    record_seconds -= duration
                else:
                    return text
