import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import openai
from llm import pipeline
from llm.schema import EnrichInput, EnrichOutput


class FakeResp:
    def __init__(self, content, usage=None):
        self.choices = [mock.Mock()]
        self.choices[0].message.content = content
        self.usage = usage or mock.Mock(model_dump=lambda: {"prompt_tokens": 5, "completion_tokens": 3})


def make_item():
    return EnrichInput(
        title="Test Book",
        description="Some description for a test book.",
        price_gbp=9.99,
    )


class TestRetryPolicy(unittest.TestCase):
    def setUp(self):
        pipeline.MAX_RETRIES = 3
        pipeline.BACKOFF_BASE = 0.0  # no real sleeping in tests
        pipeline.random.uniform = lambda a, b: 0.0
        os.environ["LLM_CACHE"] = "0"  # never let the cache short-circuit a mocked call

    def test_401_authentication_error_is_not_retried(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            raise openai.AuthenticationError("bad key", response=mock.Mock(status_code=401), body=None)
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            with self.assertRaises(openai.AuthenticationError):
                pipeline.complete([{"role": "user", "content": "x"}], "v1", "gemma3:1b")
        self.assertEqual(len(calls), 1, "401 must never be retried")

    def test_400_bad_request_is_not_retried(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            raise openai.BadRequestError("bad", response=mock.Mock(status_code=400), body=None)
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            with self.assertRaises(openai.BadRequestError):
                pipeline.complete([{"role": "user", "content": "x"}], "v1", "gemma3:1b")
        self.assertEqual(len(calls), 1, "400 must never be retried")

    def test_429_rate_limit_is_retried_then_succeeds(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            if len(calls) == 1:
                raise openai.RateLimitError("slow down", response=mock.Mock(status_code=429), body=None)
            return FakeResp('{"category": "fiction", "summary": "ok", "confidence": 0.9, "quality_flags": []}')
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            text, retries, _ = pipeline.complete([{"role": "user", "content": "x"}], "v1", "gemma3:1b")
        self.assertEqual(len(calls), 2)
        self.assertEqual(retries, 1)

    def test_500_is_retried(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            raise openai.InternalServerError("boom", response=mock.Mock(status_code=500), body=None)
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            with self.assertRaises(openai.InternalServerError):
                pipeline.complete([{"role": "user", "content": "x"}], "v1", "gemma3:1b")
        self.assertEqual(len(calls), 4, "5xx retried up to MAX_RETRIES then raises")

    def test_pipeline_repairs_once_then_validates(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            if len(calls) == 1:
                return FakeResp("Sure! Here is the JSON: ```json\n{\"category\": \"fiction\", \"summary\": \"ok\", \"confidence\": 0.9, \"quality_flags\": []}```")
            return FakeResp('{"category": "fiction", "summary": "ok", "confidence": 0.9, "quality_flags": []}')
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            out = pipeline.run_pipeline(make_item(), model="gemma3:1b")
        self.assertIsInstance(out, EnrichOutput)
        self.assertEqual(out.category.value, "fiction")
        self.assertEqual(len(calls), 1, "fence-wrapped JSON parses on first try")

    def test_validation_failure_quarantines_and_raises(self):
        calls = []
        def fake_create(**kwargs):
            calls.append(1)
            return FakeResp('{"category": "not_a_real_category", "summary": "x", "confidence": 1, "quality_flags": []}')
        with mock.patch.object(pipeline, "get_client") as gc:
            gc.return_value = mock.Mock(chat=mock.Mock(completions=mock.Mock(create=fake_create)))
            with self.assertRaises(RuntimeError):
                pipeline.run_pipeline(make_item(), model="gemma3:1b")
        self.assertEqual(len(calls), 2, "exactly one repair attempt")
        q = (Path(__file__).resolve().parent.parent / "logs" / "quarantine.jsonl")
        lines = q.read_text().strip().splitlines()
        self.assertTrue(any("not_a_real_category" in l for l in lines), "quarantine line written")


if __name__ == "__main__":
    unittest.main(verbosity=2)