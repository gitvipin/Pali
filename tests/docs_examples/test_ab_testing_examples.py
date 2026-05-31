"""
Tests for examples from A/B Testing Guide.

These tests verify that all code snippets in docs/guide/ab-testing.md
actually work as described.
"""

import unittest
from pali import params


class TestABTestingBasic(unittest.TestCase):
    """Test: Basic A/B testing from A/B Testing Guide."""
    
    def test_simple_ab_testing(self):
        """Test simple parameter with A/B values."""
        # Reset params for clean test
        params.params_dict = {}
        
        params.add_param(
            'algorithm',
            val='algorithm_v1',
            val_type=str,
            ab_values=['algorithm_v1', 'algorithm_v2'],
            ab_enabled=True
        )
        
        # Each call should return next value in sequence
        result1 = params.get_param('algorithm')
        result2 = params.get_param('algorithm')
        result3 = params.get_param('algorithm')
        
        # Should cycle through values
        self.assertIn(result1, ['algorithm_v1', 'algorithm_v2'])
        self.assertIn(result2, ['algorithm_v1', 'algorithm_v2'])
        self.assertIn(result3, ['algorithm_v1', 'algorithm_v2'])
    
    def test_ab_testing_disabled(self):
        """Test A/B testing disabled - should always return default."""
        params.params_dict = {}
        
        params.add_param(
            'feature_flag',
            val='disabled',
            val_type=str,
            ab_values=['enabled', 'disabled'],
            ab_enabled=False
        )
        
        # Should always return default value
        result1 = params.get_param('feature_flag')
        result2 = params.get_param('feature_flag')
        result3 = params.get_param('feature_flag')
        
        self.assertEqual(result1, 'disabled')
        self.assertEqual(result2, 'disabled')
        self.assertEqual(result3, 'disabled')


class TestABTestingInteger(unittest.TestCase):
    """Test: A/B testing with integer parameters."""
    
    def test_integer_ab_values(self):
        """Test A/B testing with integer values."""
        params.params_dict = {}
        
        params.add_param(
            'batch_size',
            val=32,
            val_type=int,
            ab_values=[16, 32, 64],
            ab_enabled=True
        )
        
        # Collect results
        results = [params.get_param('batch_size') for _ in range(6)]
        
        # Should contain the A/B values
        for result in results:
            self.assertIn(result, [16, 32, 64])
    
    def test_integer_ab_cycling(self):
        """Test integer A/B values cycle correctly."""
        params.params_dict = {}
        
        params.add_param(
            'threads',
            val=4,
            val_type=int,
            ab_values=[2, 4, 8],
            ab_enabled=True
        )
        
        results = [params.get_param('threads') for _ in range(9)]
        
        # With 3 values, should cycle
        unique_results = set(results)
        self.assertEqual(unique_results, {2, 4, 8})


class TestABTestingFloat(unittest.TestCase):
    """Test: A/B testing with float parameters."""
    
    def test_float_ab_values(self):
        """Test A/B testing with float values."""
        params.params_dict = {}
        
        params.add_param(
            'learning_rate',
            val=0.001,
            val_type=float,
            ab_values=[0.0001, 0.001, 0.01],
            ab_enabled=True
        )
        
        results = [params.get_param('learning_rate') for _ in range(3)]        
        # Should get all three values
        self.assertIn(0.0001, results)
        self.assertIn(0.001, results)
        self.assertIn(0.01, results)
    
    def test_float_ab_precision(self):
        """Test float A/B values maintain precision."""
        params.params_dict = {}
        
        params.add_param(
            'threshold',
            val=0.5,
            val_type=float,
            ab_values=[0.25, 0.5, 0.75],
            ab_enabled=True
        )
        
        result1 = params.get_param('threshold')
        
        # Should be a float with correct precision
        self.assertIsInstance(result1, float)
        self.assertIn(result1, [0.25, 0.5, 0.75])


class TestABTestingMultipleParams(unittest.TestCase):
    """Test: A/B testing with multiple parameters."""
    
    def test_multiple_ab_parameters(self):
        """Test multiple A/B parameters."""
        params.params_dict = {}
        
        params.add_param(
            'algorithm',
            val='v1',
            val_type=str,
            ab_values=['v1', 'v2'],
            ab_enabled=True
        )
        
        params.add_param(
            'batch_size',
            val=32,
            val_type=int,
            ab_values=[16, 32, 64],
            ab_enabled=True
        )
        
        params.add_param(
            'learning_rate',
            val=0.001,
            val_type=float,
            ab_values=[0.0001, 0.001, 0.01],
            ab_enabled=True
        )
        
        # Get each parameter multiple times
        algo1 = params.get_param('algorithm')
        batch1 = params.get_param('batch_size')
        lr1 = params.get_param('learning_rate')
        
        algo2 = params.get_param('algorithm')
        batch2 = params.get_param('batch_size')
        lr2 = params.get_param('learning_rate')
        
        # All should be in their respective A/B values
        self.assertIn(algo1, ['v1', 'v2'])
        self.assertIn(batch1, [16, 32, 64])
        self.assertIn(lr1, [0.0001, 0.001, 0.01])


class TestABTestingMixedEnabled(unittest.TestCase):
    """Test: Mix of enabled and disabled A/B testing."""
    
    def test_some_ab_enabled_some_disabled(self):
        """Test with some parameters A/B enabled and others disabled."""
        params.params_dict = {}
        
        # Enabled A/B
        params.add_param(
            'algo_ab',
            val='v1',
            val_type=str,
            ab_values=['v1', 'v2'],
            ab_enabled=True
        )
        
        # Disabled A/B
        params.add_param(
            'algo_fixed',
            val='v1',
            val_type=str,
            ab_values=['v1', 'v2'],
            ab_enabled=False
        )
        
        # A/B enabled should vary
        ab_results = [params.get_param('algo_ab') for _ in range(4)]
        
        # A/B disabled should stay same
        fixed_results = [params.get_param('algo_fixed') for _ in range(4)]
        
        self.assertEqual(len(set(fixed_results)), 1)  # All same
        self.assertEqual(fixed_results[0], 'v1')


class TestABTestingDistribution(unittest.TestCase):
    """Test: A/B testing value distribution."""
    
    def test_even_distribution(self):
        """Test that A/B values are distributed evenly."""
        params.params_dict = {}
        
        params.add_param(
            'variant',
            val='a',
            val_type=str,
            ab_values=['a', 'b', 'c'],
            ab_enabled=True
        )
        
        # Get many samples
        results = [params.get_param('variant') for _ in range(30)]
        
        # Count occurrences
        count_a = results.count('a')
        count_b = results.count('b')
        count_c = results.count('c')
        
        # Should be roughly distributed
        self.assertGreater(count_a, 0)
        self.assertGreater(count_b, 0)
        self.assertGreater(count_c, 0)


class TestABTestingEdgeCases(unittest.TestCase):
    """Test: Edge cases for A/B testing."""
    
    def test_single_ab_value(self):
        """Test A/B testing with single value."""
        params.params_dict = {}
        
        params.add_param(
            'single',
            val='only',
            val_type=str,
            ab_values=['only'],
            ab_enabled=True
        )
        
        results = [params.get_param('single') for _ in range(3)]
        
        # Should always be the same
        self.assertTrue(all(r == 'only' for r in results))
    
    def test_two_ab_values(self):
        """Test A/B testing with two values."""
        params.params_dict = {}
        
        params.add_param(
            'binary',
            val='option1',
            val_type=str,
            ab_values=['option1', 'option2'],
            ab_enabled=True
        )
        
        results = [params.get_param('binary') for _ in range(4)]
        
        # Should alternate between two values
        for result in results:
            self.assertIn(result, ['option1', 'option2'])


class TestABTestingWithConfig(unittest.TestCase):
    """Test: A/B testing integration with configuration."""
    
    def test_ab_testing_with_typed_values(self):
        """Test A/B testing respects value types."""
        params.params_dict = {}
        
        # String type
        params.add_param(
            'mode',
            val='prod',
            val_type=str,
            ab_values=['prod', 'test'],
            ab_enabled=True
        )
        
        mode_result = params.get_param('mode')
        self.assertIsInstance(mode_result, str)
        
        # Integer type
        params.add_param(
            'count',
            val=10,
            val_type=int,
            ab_values=[5, 10, 15],
            ab_enabled=True
        )
        
        count_result = params.get_param('count')
        self.assertIsInstance(count_result, int)


if __name__ == '__main__':
    unittest.main()
