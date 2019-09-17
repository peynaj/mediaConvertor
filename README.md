Python script for change `playback speed rate` of audio and video media files or extract duration time of them.


### Requirements
- Python3
- ffmpeg
- `requirements.txt` python packages


### Change speed rate
```python
import mconv

media_path = '/path/to/media/files'
speed_rate = 2
mconv.change_audio_rate(media_path, speed_rate)
```


### Convert video files to audio & change speed rate
```python
import mconv

videos_path = '/path/to/media/files'
speed_rate = 2
mconv.video_to_audio_and_change_rate(videos_path, speed_rate)
```


### Extract medias duration seconds
```python
import mconv

media_path = '/path/to/media/files'
durations = mconv.get_audio_details(media_path)
```



