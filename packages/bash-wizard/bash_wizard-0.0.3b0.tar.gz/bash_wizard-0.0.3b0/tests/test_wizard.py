import unittest
from unittest.mock import patch
import json
from bash_wizard import wizard


class TestWizard(unittest.TestCase):
    @patch('bash_wizard.wizard.ollama.generate')
    def test_generate(self, mock_generate):
        # Mock the response from ollama.generate
        mock_response = {
            'response': json.dumps({
                'bash_command': 'ls -la',
                'command_explanation': 'List all files in long format'
            })
        }
        mock_generate.return_value = mock_response

        description = "List all files"
        expected_output = {
            'bash_command': 'ls -la',
            'command_explanation': 'List all files in long format'
        }

        result = wizard.generate(description)
        self.assertEqual(result, expected_output)

    @patch('bash_wizard.wizard.input', return_value='y')
    @patch('bash_wizard.wizard.generate')
    @patch('bash_wizard.wizard.check_model')
    @patch('bash_wizard.wizard.args_description', return_value="List all files")
    @patch('bash_wizard.wizard.messages.thinking')
    @patch('bash_wizard.wizard.messages.output')
    def test_run(
        self,
        mock_output,
        mock_thinking,
        mock_args_description,
        mock_check_model,
        mock_generate,
        mock_input
    ):
        # Mock the generate function
        mock_generate.return_value = {
            'bash_command': 'ls -la',
            'command_explanation': 'List all files in long format'
        }

        # Mock the messages
        mock_thinking.return_value = "Thinking..."
        mock_output.return_value = "Output message"

        # Run the function
        wizard.run()

        # Assertions
        mock_check_model.assert_called_once()
        mock_args_description.assert_called_once()
        mock_thinking.assert_called_once_with("List all files")
        mock_generate.assert_called_once_with("List all files")
        mock_output.assert_called_once_with(
            bash_command='ls -la',
            command_explanation='List all files in long format'
        )
        mock_input.assert_called_once()


if __name__ == '__main__':
    unittest.main()
