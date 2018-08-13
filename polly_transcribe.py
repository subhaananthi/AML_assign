import boto3
import time
import json

#### Polly to convert text to audio file
S3BucketName = "subhs3aml"
Text_2_Convert = "The sun does arise and make happy the skies. The merry bells ring to welcome the spring."
job_name = "Subha_transcription_job_AML"
transcribe_json = job_name + ".json"

polly_client = boto3.client(service_name='polly', region_name='eu-west-1')

response = polly_client.start_speech_synthesis_task(VoiceId='Mathew',
                OutputS3BucketName=S3BucketName,
                OutputS3KeyPrefix=S3BucketName,
                OutputFormat='mp3', 
                Text=Text_2_Convert)
AudioFile = response['SynthesisTask']['OutputUri']
print('Text to convert: ' + Text_2_Convert)
print('Link to audio file: ' + AudioFile)

time.sleep(30)
#### Transcribe to convert audio to text

transcribe = boto3.client(service_name='transcribe', region_name='eu-west-1')

result = transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': AudioFile},
    OutputBucketName=S3BucketName,
    MediaFormat='mp3',
    LanguageCode='en-US'
)
time.sleep(60)
status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
OutputURI = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
print('Output json file path : ' + OutputURI)
print('Output json file : ' + transcribe_json)

s3 = boto3.resource('s3')

content_object = s3.Object(S3BucketName, transcribe_json)
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)

print('The text converted from audio : ' + json_content['results']['transcripts'][0]['transcript'])
