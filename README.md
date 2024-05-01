---
title: Stream your voice clone 🎼
description: We'll build a Django app that streams your voice (cloned using ElevenLabs) to the user
created_at:
---
We'll quickly create a Django app that:
- streams audios to the user
- turned your voice into an instrument that you can use to create audiobooks with your voice, or anything else 🎉

Our final product will look like this:
<br>

<style>
    /* Make video responsive */
    .video-container video {
       width: 100% !important;
        height: auto !important;
        border-radius: 10px;
    }
  </style>
<div class="video-container">
  <video controls autoplay controls playsinline loop muted>
    <source src="https://pd-site.s3.amazonaws.com/voice-api/final_product.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>


## 0. Install and create your Django app
```bash
pip install --upgrade django elevenlabs python-dotenv

django-admin startproject core .
python manage.py startapp sim
```

- Add our app sim to the `INSTALLED_APPS` in settings.py:

```python
# settings.py
INSTALLED_APPS = [
    'sim',
    ...
]
```

## Add your environment variables
- Create a .env file in your project root and add the following:
```
ELEVENLABS_API_KEY=your-elevenlabs-api-key
VOICE1_ID=your-voice1-id
VOICE2_ID=your-voice2-id
VOICE2_ID=your-voice3-id
```

- To get your ElevenLabs API key, sign up at [ElevenLabs](https://www.eleven-labs.com/).
- Add at least 3 voice ids you want to use from ElevenLabs to the .env file.


## 1. Add your urls
- Add the following to your core/urls.py:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sim.urls')),
]
```

- Create a urls.py file in your sim app and add the following:
```python
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('stream/', views.stream_audio, name='stream-audio'),
]
```

## 2. Add your templates
- Create a templates directory in your sim app and add an index.html file:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stream your voice</title>

</head>
<body>
    <div class="audio-player">
        <h1>Hear your voice</h1>
        <form action="{% url 'stream-audio' %}" method="get" target="audio_frame">
            <label for="text">Enter text:</label>
            <textarea name="text" id="text" required>The Western world is a beacon of happiness</textarea>
            <label for="voice">Choose a voice:</label>
            <select id="voice" name="voice">
                {% for voice in voices %}
                <option value="{{ voice.id }}">{{ voice.name }}</option>
                {% endfor %}
            </select>
            <button type="submit">Create audio</button>
        </form>
        <audio controls>
            <source src="" type="audio/mp3" id="audioSource">
            Your browser does not support the audio element.
        </audio>
    </div>

    <script>
        const form = document.querySelector('form');
        const audioSource = document.getElementById('audioSource');
        const audioPlayer = document.querySelector('audio');

        form.onsubmit = function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const url = `${form.action}?text=${encodeURIComponent(formData.get('text'))}&voice=${encodeURIComponent(formData.get('voice'))}`;
            audioSource.src = url;
            audioPlayer.load();
            audioPlayer.play();
        };
    </script>
</body>
</html>
```


## 3. Create your views
- Add the following to your sim/views.py:
```python
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
```


## Run your app
```bash
python manage.py runserver
```
- Visit the url mentioned in the terminal to see your app in action.


## Add styling using Photon Designer
Currently, the app looks pretty basic.
[]

- We'll use Photon Designer (my product) to style the app in three simple steps:
- 1. Visit [Photon Designer](https://www.photondesigner.com/?ref=blink) and sign up (free currently) 
- 2. paste our template into the editor
- 3. add a prompt "Style to be an elegant audio streaming app like [your favorite audio streaming app]" and press generate
- 4. Paste generated code and replace the content of the index.html file with it.

Here's a video of me doing this:


Here's how our final app looks after doing this:


## Add your voice clone
Finally, let's add your specific voice to the app, so that you can stream your voice clone to the user.
This is very easy to do. We simply need to clone your voice and copy your voice clone id to the .env file.
To do this:
1. Create a voice clone on [ElevenLabs](https://www.elevenlabs.io/)
See my short video below showing exactly how to do this:
2. Paste your voice clone id into the .env file

Video showing how to clone your voice:
<br>
<style>
.embed-container { 
    position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 10px;
} 
.embed-container iframe, .embed-container object, .embed-container embed { 
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
</style>
<div class='embed-container'>
<iframe src='https://www.youtube.com/embed/TjMKTVlMxjE' allow='autoplay' frameborder='0' allowfullscreen></iframe>
</div>
<br>  



## Congrats! ✅
You've successfully built a Django app that:
- streams audios to the user
- turned your voice into an instrument that you can use to create audiobooks with your voice, or anything else 🎉


## P.S Photon Designer
Do you dream of creating Django products so quickly they break the space-time continuum? Yeah, me too.

I'm building: [Photon Designer](https://www.photondesigner.com/?ref=blink). It's a visual editor that puts the 'fast'
in 'very fast.'

When [Photon Designer](https://www.photondesigner.com/?ref=blink) starts up, it slings Django templates at you faster
than light escaping a black hole (In a friendly way).
