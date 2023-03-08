import openai



def split_answer(string):
    for i in range(0, len(string), 1000):
        yield string[i:i+1000]

def gpt(self, prompt: str):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response['choices'][0]['message']['content']
    
    answer_length = len(answer)
    print(answer_length)
    print(answer)
    for i in split_answer(answer):
            print(len(i))
    #for i in split_answer(answer):


def whisper(audio_file):
    """
    :endpoint: /transcriptions
    :endpoint: /translations
    Warning: File uploads are currently limited to 25 MB and the following input types are
    supported: mp3,mp4,mpeg,mpeg,mpga,m4a,wav,webm
    """
    #Transcriptions
    with open(audio_file, "rb") as af:
        transcript = openai.Audio.transcribe("whisper-1", af)
        print(transcript)
        return transcript
        # by default, the response type will be json with the raw text included!

    #Translations
    with open(audio_file, "rb") as af:
        translation = openai.Audio.translate("whisper-1", af)
        print(translation)
        return translation

    # Longer inputs
    # you need to break into chunks of 25 MB
    #from pydub import AudioSegment


    

        