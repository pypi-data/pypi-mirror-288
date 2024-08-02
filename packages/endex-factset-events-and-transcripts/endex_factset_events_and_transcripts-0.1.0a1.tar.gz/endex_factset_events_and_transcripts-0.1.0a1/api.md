# Shared Types

```python
from endex_factset_events_and_transcripts.types import EventsAudioDaily, NrtCalls, Transcripts
```

# CalendarEvents

Types:

```python
from endex_factset_events_and_transcripts.types import CompanyEventResponse
```

Methods:

- <code title="post /calendar/events">client.calendar_events.<a href="./src/endex_factset_events_and_transcripts/resources/calendar_events.py">create</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/calendar_event_create_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/company_event_response.py">CompanyEventResponse</a></code>

# EventsAudio

## History

Types:

```python
from endex_factset_events_and_transcripts.types.events_audio import EventsAudioHistory
```

Methods:

- <code title="get /audio/history">client.events_audio.history.<a href="./src/endex_factset_events_and_transcripts/resources/events_audio/history.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/events_audio/history_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/events_audio/events_audio_history.py">EventsAudioHistory</a></code>

## ByDate

Methods:

- <code title="get /audio/by-date">client.events_audio.by_date.<a href="./src/endex_factset_events_and_transcripts/resources/events_audio/by_date.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/events_audio/by_date_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/events_audio_daily.py">EventsAudioDaily</a></code>

## ByUploadTime

Methods:

- <code title="get /audio/by-upload-time">client.events_audio.by_upload_time.<a href="./src/endex_factset_events_and_transcripts/resources/events_audio/by_upload_time.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/events_audio/by_upload_time_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/events_audio_daily.py">EventsAudioDaily</a></code>

## ByFileName

Types:

```python
from endex_factset_events_and_transcripts.types.events_audio import EventsAudioDailyFileName
```

Methods:

- <code title="get /audio/by-file-name">client.events_audio.by_file_name.<a href="./src/endex_factset_events_and_transcripts/resources/events_audio/by_file_name.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/events_audio/by_file_name_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/events_audio/events_audio_daily_file_name.py">EventsAudioDailyFileName</a></code>

## ByIDs

Types:

```python
from endex_factset_events_and_transcripts.types.events_audio import EventsAudioDailyIDs
```

Methods:

- <code title="get /audio/by-ids">client.events_audio.by_ids.<a href="./src/endex_factset_events_and_transcripts/resources/events_audio/by_ids.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/events_audio/by_id_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/events_audio/events_audio_daily_ids.py">EventsAudioDailyIDs</a></code>

# NearRealTimeTranscripts

## ByTicker

Methods:

- <code title="get /nrt/by-ticker">client.near_real_time_transcripts.by_ticker.<a href="./src/endex_factset_events_and_transcripts/resources/near_real_time_transcripts/by_ticker.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/by_ticker_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/nrt_calls.py">NrtCalls</a></code>

## ByIDs

Methods:

- <code title="get /nrt/by-ids">client.near_real_time_transcripts.by_ids.<a href="./src/endex_factset_events_and_transcripts/resources/near_real_time_transcripts/by_ids.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/by_id_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/nrt_calls.py">NrtCalls</a></code>

## Speakerids

Types:

```python
from endex_factset_events_and_transcripts.types.near_real_time_transcripts import NrtSpeakerIDs
```

Methods:

- <code title="get /nrt/speakerids">client.near_real_time_transcripts.speakerids.<a href="./src/endex_factset_events_and_transcripts/resources/near_real_time_transcripts/speakerids.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/speakerid_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/nrt_speaker_ids.py">NrtSpeakerIDs</a></code>

## Indexed

Types:

```python
from endex_factset_events_and_transcripts.types.near_real_time_transcripts import IndexedNrt
```

Methods:

- <code title="get /nrt/indexed">client.near_real_time_transcripts.indexed.<a href="./src/endex_factset_events_and_transcripts/resources/near_real_time_transcripts/indexed.py">retrieve</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/indexed_retrieve_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/near_real_time_transcripts/indexed_nrt.py">IndexedNrt</a></code>

# Transcripts

## Dates

Methods:

- <code title="get /transcripts/dates">client.transcripts.dates.<a href="./src/endex_factset_events_and_transcripts/resources/transcripts/dates.py">list</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/transcripts/date_list_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/transcripts.py">Transcripts</a></code>

## Times

Types:

```python
from endex_factset_events_and_transcripts.types.transcripts import TranscriptsTimes
```

Methods:

- <code title="get /transcripts/times">client.transcripts.times.<a href="./src/endex_factset_events_and_transcripts/resources/transcripts/times.py">list</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/transcripts/time_list_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/transcripts/transcripts_times.py">TranscriptsTimes</a></code>

## Search

Methods:

- <code title="get /transcripts/search">client.transcripts.search.<a href="./src/endex_factset_events_and_transcripts/resources/transcripts/search.py">list</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/transcripts/search_list_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/transcripts.py">Transcripts</a></code>

## IDs

Types:

```python
from endex_factset_events_and_transcripts.types.transcripts import TranscriptsOne
```

Methods:

- <code title="get /transcripts/ids">client.transcripts.ids.<a href="./src/endex_factset_events_and_transcripts/resources/transcripts/ids.py">list</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/transcripts/id_list_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/transcripts/transcripts_one.py">TranscriptsOne</a></code>

## Events

Methods:

- <code title="get /transcripts/events">client.transcripts.events.<a href="./src/endex_factset_events_and_transcripts/resources/transcripts/events.py">list</a>(\*\*<a href="src/endex_factset_events_and_transcripts/types/transcripts/event_list_params.py">params</a>) -> <a href="./src/endex_factset_events_and_transcripts/types/shared/transcripts.py">Transcripts</a></code>

# Reference

## TimeZones

Types:

```python
from endex_factset_events_and_transcripts.types.reference import ResponseTime
```

Methods:

- <code title="get /reference/time-zones">client.reference.time_zones.<a href="./src/endex_factset_events_and_transcripts/resources/reference/time_zones.py">retrieve</a>() -> <a href="./src/endex_factset_events_and_transcripts/types/reference/response_time.py">ResponseTime</a></code>

## Categories

Types:

```python
from endex_factset_events_and_transcripts.types.reference import ResponseCategories
```

Methods:

- <code title="get /reference/categories">client.reference.categories.<a href="./src/endex_factset_events_and_transcripts/resources/reference/categories.py">list</a>() -> <a href="./src/endex_factset_events_and_transcripts/types/reference/response_categories.py">ResponseCategories</a></code>
