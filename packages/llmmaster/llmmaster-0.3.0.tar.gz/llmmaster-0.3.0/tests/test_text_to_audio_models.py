import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../llmmaster'))

import pytest
import elevenlabs

from llmmaster.config import OPENAI_TTS_VOICE_OPTIONS
from llmmaster.text_to_audio_models import OpenAITextToSpeech
from llmmaster.text_to_audio_models import ElevenLabsTextToSpeech
from llmmaster import LLMMaster

TEST_OUTPUT_PATH = 'test-outputs'
PROMPT = "Do not concentrate on the finger, or you will miss all that heavenly glory."


@pytest.fixture
def run_api(request):
    return request.config.getoption("--run-api")


def test_openai_text_to_speech_basic(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = []

    for voice_pattern in OPENAI_TTS_VOICE_OPTIONS:
        test_case = {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': voice_pattern}
        test_cases.append({'name': f'openai_tts_{voice_pattern}', 'params': test_case})

    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAITextToSpeech):
            judgment = False

    if run_api:
        # add --run-api option for making actual API calls test, paying API credit
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        for name, response in master.results.items():
            if not response:
                judgment = False
            filename = f"{name}.mp3"
            filepath = os.path.join(TEST_OUTPUT_PATH, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            print(f'Saved as {filepath} for {name}')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True


def test_openai_text_to_speech_various_options(run_api):
    judgment = True
    master = LLMMaster()

    test_cases = [
        {'name': 'openai_tts_v1_echo_voice_slow', 'params': {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': 'echo', 'speed': 0.5}},
        {'name': 'openai_tts_v2_fable_voice_fast', 'params': {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': 'fable', 'speed': 1.5, 'response_format': 'opus'}},
        {'name': 'openai_tts_v3_onyx_voice_model_tts_1', 'params': {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': 'onyx', 'model': 'tts-1', 'response_format': 'aac'}},
        {'name': 'openai_tts_v4_nova_voice_model_tts_1_hd', 'params': {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': 'nova', 'model': 'tts-1-hd'}},
        {'name': 'openai_tts_v5_shimmer_voice_response_format', 'params': {'provider': 'openai_tts', 'prompt': PROMPT, 'voice': 'shimmer', 'response_format': 'opus'}},
    ]

    for case in test_cases:
        master.summon({case['name']: master.pack_parameters(**case['params'])})

    for name, instance in master.instances.items():
        print(f'{name} = {instance}, {instance.parameters}')
        if not isinstance(instance, OpenAITextToSpeech):
            judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        for name, response in master.results.items():
            if not response:
                judgment = False

            ext = master.instances[name].parameters.get('response_format', 'mp3')
            filename = f"{name}.{ext}"
            filepath = os.path.join(TEST_OUTPUT_PATH, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
            print(f'Saved as {filepath} for {name}')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True


def test_elevenlabs_text_to_speech(run_api):
    judgment = True
    master = LLMMaster()

    test_case = master.pack_parameters(provider='elevenlabs_tts', prompt=PROMPT)

    master.summon({'elevenlabs_tts': test_case})

    print(f'elevenlabs_tts = {master.instances["elevenlabs_tts"]}, {master.instances["elevenlabs_tts"].parameters}')
    if not isinstance(master.instances["elevenlabs_tts"], ElevenLabsTextToSpeech):
        judgment = False

    if run_api:
        print('Run API')
        try:
            master.run()
        except Exception as e:
            pytest.fail(f"An error occurred during API calls: {str(e)}")

        if not os.path.isdir(TEST_OUTPUT_PATH):
            os.makedirs(TEST_OUTPUT_PATH)

        print('Responses')
        if not master.results['elevenlabs_tts']:
            judgment = False
        else:
            filepath = os.path.join(TEST_OUTPUT_PATH, 'elevenlabs_tts.mp3')
            elevenlabs.save(master.results['elevenlabs_tts'], filepath)
            print(f'Saved as {filepath} for elevenlabs_tts')

    print(f'Elapsed time: {master.elapsed_time} seconds')
    master.dismiss()

    assert judgment is True
