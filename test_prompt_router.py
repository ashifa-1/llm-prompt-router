import sys
import os
import json
import unittest
from unittest.mock import MagicMock, patch

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock third-party libraries if not installed in current environment
if "dotenv" not in sys.modules:
    sys.modules["dotenv"] = MagicMock()
if "groq" not in sys.modules:
    sys.modules["groq"] = MagicMock()

import classifier
import router
import logger
import prompts


class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        classifier.client = self.mock_client

    def test_classifier_prompt_contains_clarifications(self):
        """Verify prompt explicitly separates SQL/code from writing, and details data."""
        self.assertIn("SQL queries", classifier.CLASSIFIER_PROMPT)
        self.assertIn("Note: requests asking to explain, analyze, or debug code/SQL belong in 'code', not 'writing'", classifier.CLASSIFIER_PROMPT)
        self.assertIn("human language/prose feedback", classifier.CLASSIFIER_PROMPT)
        self.assertIn("data:", classifier.CLASSIFIER_PROMPT)

    def test_classify_intent_json_mode_and_raw_json(self):
        """Verify response_format={'type': 'json_object'} is used and raw JSON parsed."""
        mock_choice = MagicMock()
        mock_choice.message.content = '{"intent": "code", "confidence": 0.95}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response

        res = classifier.classify_intent("How do I sort a list?")
        self.assertEqual(res, {"intent": "code", "confidence": 0.95})

        # Verify response_format was passed as json_object
        call_kwargs = self.mock_client.chat.completions.create.call_args.kwargs
        self.assertEqual(call_kwargs.get("response_format"), {"type": "json_object"})

    def test_classify_intent_markdown_stripping_json(self):
        """Verify markdown fences with ```json ... ``` are stripped properly."""
        mock_choice = MagicMock()
        mock_choice.message.content = '```json\n{\n  "intent": "code",\n  "confidence": 0.98\n}\n```'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response

        res = classifier.classify_intent("explain this sql query")
        self.assertEqual(res, {"intent": "code", "confidence": 0.98})

    def test_classify_intent_markdown_stripping_plain_fence(self):
        """Verify markdown fences with ``` ... ``` are stripped properly."""
        mock_choice = MagicMock()
        mock_choice.message.content = '```\n{"intent": "data", "confidence": 0.91}\n```'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response

        res = classifier.classify_intent("what is the standard deviation")
        self.assertEqual(res, {"intent": "data", "confidence": 0.91})

    def test_classify_intent_invalid_intent_fallback(self):
        """Verify unrecognized intents fall back to 'unclear'."""
        mock_choice = MagicMock()
        mock_choice.message.content = '{"intent": "random_unknown_intent", "confidence": 0.99}'
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response

        res = classifier.classify_intent("foo bar")
        self.assertEqual(res, {"intent": "unclear", "confidence": 0.99})


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        router.client = self.mock_client

    def test_route_low_confidence_fallback(self):
        res = router.route_and_respond("help", {"intent": "code", "confidence": 0.5})
        self.assertIn("I'm not sure what you need", res)

    def test_route_unclear_intent(self):
        res = router.route_and_respond("hello", {"intent": "unclear", "confidence": 0.95})
        self.assertIn("I'm not sure what you need", res)

    def test_route_high_confidence_known_intent(self):
        mock_choice = MagicMock()
        mock_choice.message.content = "Here is the code to sort a list..."
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        self.mock_client.chat.completions.create.return_value = mock_response

        res = router.route_and_respond("sort list", {"intent": "code", "confidence": 0.95})
        self.assertEqual(res, "Here is the code to sort a list...")


class TestAppCLI(unittest.TestCase):
    @patch("builtins.input", side_effect=["", "   ", "exit"])
    @patch("classifier.classify_intent")
    def test_app_empty_input_and_graceful_exit(self, mock_classify, mock_input):
        import app
        # Should skip empty inputs and exit gracefully on "exit" without calling classifier
        app.main()
        mock_classify.assert_not_called()

    @patch("builtins.input", side_effect=["quit"])
    @patch("classifier.classify_intent")
    def test_app_quit_command(self, mock_classify, mock_input):
        import app
        app.main()
        mock_classify.assert_not_called()

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_app_keyboard_interrupt(self, mock_input):
        import app
        # Should catch KeyboardInterrupt and exit without raising exception
        app.main()


if __name__ == "__main__":
    unittest.main()

