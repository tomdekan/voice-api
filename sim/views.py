import os

from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseBadRequest
from elevenlabs.client import ElevenLabs


def index(request):
    voices = [
        {"name": "Bruce", "id": os.environ['VOICE1_ID']},
        {"name": "Mike", "id": os.environ['VOICE2_ID']},
        {"name": "Shaneel", "id": os.environ['VOICE3_ID']},
    ]
    return render(request, 'index.html', context={"voices": voices})


def stream_audio(request):
    # Retrieve text and voice from query parameters
    text = request.GET.get('text')
    voice = request.GET.get('voice')

    if not text or not voice:
        return HttpResponseBadRequest("Text and voice parameters are required.")

    client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
    try:
        audio_stream = client.generate(
            text=text,
            voice=voice,
            stream=True
        )
    except Exception as e:
        return HttpResponseBadRequest(f"Error generating audio: {str(e)}")

    response = StreamingHttpResponse(audio_stream, content_type='audio/mp3')
    return response
