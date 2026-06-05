"""
Tests for examples from Pipeline Guide.

These tests verify that the code snippets in docs/guide/pipeline.md
actually work as described.
"""

import csv
import json
import os
import tempfile
import unittest

from pali.pipeline import Assembly, Pipeline, Stage
from pali.worker import ThreadPool


class TestPipelineStageExamples(unittest.TestCase):
    """Test individual stage examples from the Pipeline Guide."""

    def test_validate_data_stage_passes_for_valid_data(self):
        class ValidateDataStage(Stage):
            def __init__(self):
                super(ValidateDataStage, self).__init__("Validate")

            def run(self, data):
                if not isinstance(data, dict):
                    raise ValueError("Data must be a dictionary")

                required_keys = ['input', 'config']
                for key in required_keys:
                    if key not in data:
                        raise KeyError(f"Missing required key: {key}")

        stage = ValidateDataStage()
        data = {'input': 1, 'config': {}}
        stage.run(data)
        self.assertEqual(stage.name, 'Validate')

    def test_validate_data_stage_fails_for_missing_keys(self):
        class ValidateDataStage(Stage):
            def __init__(self):
                super(ValidateDataStage, self).__init__("Validate")

            def run(self, data):
                if not isinstance(data, dict):
                    raise ValueError("Data must be a dictionary")

                required_keys = ['input', 'config']
                for key in required_keys:
                    if key not in data:
                        raise KeyError(f"Missing required key: {key}")

        stage = ValidateDataStage()
        with self.assertRaises(KeyError):
            stage.run({'input': 1})

    def test_processing_stage_transforms_numbers(self):
        class ProcessingStage(Stage):
            def __init__(self, multiplier=2):
                super(ProcessingStage, self).__init__("Processing")
                self.multiplier = multiplier

            def run(self, data):
                if 'numbers' in data:
                    data['processed'] = [x * self.multiplier for x in data['numbers']]

        stage = ProcessingStage(multiplier=3)
        data = {'numbers': [1, 2, 3]}
        stage.run(data)
        self.assertEqual(data['processed'], [3, 6, 9])

    def test_output_stage_writes_json_file(self):
        class OutputStage(Stage):
            def __init__(self, output_file):
                super(OutputStage, self).__init__("Output")
                self.output_file = output_file

            def run(self, data):
                with open(self.output_file, 'w') as f:
                    json.dump(data, f, indent=2)

        temp_dir = tempfile.mkdtemp(prefix='pali-pipeline-test-')
        try:
            output_path = os.path.join(temp_dir, 'result.json')
            stage = OutputStage(output_path)
            data = {'numbers': [1, 2, 3], 'processed': [2, 4, 6]}
            stage.run(data)

            with open(output_path, 'r') as f:
                result = json.load(f)

            self.assertEqual(result, data)
        finally:
            try:
                os.remove(output_path)
            except OSError:
                pass
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass


class TestPipelineExamples(unittest.TestCase):
    """Test pipeline execution examples from the Pipeline Guide."""

    def test_pipeline_runs_stages_and_shares_data(self):
        class ReadStage(Stage):
            def __init__(self):
                super(ReadStage, self).__init__("Read")

            def run(self, data):
                data['value'] = data.get('value', 0)

        class WriteStage(Stage):
            def __init__(self):
                super(WriteStage, self).__init__("Write")

            def run(self, data):
                data['value'] = 42

        class ModifyStage(Stage):
            def __init__(self):
                super(ModifyStage, self).__init__("Modify")

            def run(self, data):
                data['value'] *= 2

        pipeline = Pipeline(
            name='DataPipeline',
            stages=[ReadStage(), WriteStage(), ModifyStage()],
            data={'value': None}
        )

        pipeline._run()
        self.assertEqual(pipeline.data['value'], 84)

    def test_pipeline_with_threadpool_runs_in_parallel(self):
        class ValidateDataStage(Stage):
            def __init__(self):
                super(ValidateDataStage, self).__init__("Validate")

            def run(self, data):
                data['validated'] = True

        class ProcessingStage(Stage):
            def __init__(self, multiplier=2):
                super(ProcessingStage, self).__init__("Processing")
                self.multiplier = multiplier

            def run(self, data):
                data['processed'] = [x * self.multiplier for x in data['numbers']]

        class OutputStage(Stage):
            def __init__(self, output_file):
                super(OutputStage, self).__init__("Output")
                self.output_file = output_file

            def run(self, data):
                with open(self.output_file, 'w') as f:
                    json.dump(data, f)

        temp_dir = tempfile.mkdtemp(prefix='pali-pipeline-test-')
        pipelines = []
        try:
            stages = [ValidateDataStage(), ProcessingStage(multiplier=3)]
            outputs = []
            for i in range(3):
                output_file = os.path.join(temp_dir, f'pipeline_{i}.json')
                pipeline = Pipeline(
                    name=f'Pipeline_{i}',
                    stages=stages + [OutputStage(output_file)],
                    data={'numbers': list(range(i * 2, i * 2 + 3))}
                )
                pipelines.append((pipeline, output_file))

            with ThreadPool(3) as tpool:
                for pipeline, _ in pipelines:
                    tpool.append_task(pipeline)

            for pipeline, output_file in pipelines:
                self.assertTrue(pipeline.data.get('validated'))
                self.assertIn('processed', pipeline.data)
                self.assertTrue(os.path.exists(output_file))
                with open(output_file, 'r') as f:
                    loaded = json.load(f)
                self.assertEqual(loaded, pipeline.data)
        finally:
            for _, output_file in pipelines:
                try:
                    os.remove(output_file)
                except OSError:
                    pass
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass

    def test_assembly_runs_multiple_pipelines(self):
        class StageA(Stage):
            def __init__(self):
                super(StageA, self).__init__("StageA")

            def run(self, data):
                data['a'] = True

        class StageB(Stage):
            def __init__(self):
                super(StageB, self).__init__("StageB")

            def run(self, data):
                data['b'] = True

        pipelines = []
        for index in range(3):
            pipeline = Pipeline(
                name=f'Pipeline_{index}',
                stages=[StageA(), StageB()],
                data={'index': index}
            )
            pipelines.append(pipeline)

        assembly = Assembly(name='TestAssembly', pipelines=pipelines, max_concurrent_pipelines=2)
        assembly._run()

        for pipeline in pipelines:
            self.assertTrue(pipeline.data.get('a'))
            self.assertTrue(pipeline.data.get('b'))

    def test_pipeline_error_handling_stops_on_failure(self):
        class FailingStage(Stage):
            def __init__(self):
                super(FailingStage, self).__init__("Failing")

            def run(self, data):
                raise ValueError('Intentional failure')

        class NextStage(Stage):
            def __init__(self):
                super(NextStage, self).__init__("Next")

            def run(self, data):
                data['next_ran'] = True

        pipeline = Pipeline(
            name='ErrorPipeline',
            stages=[FailingStage(), NextStage()],
            data={}
        )

        pipeline._run()
        self.assertNotIn('next_ran', pipeline.data)

    def test_real_world_etl_pipeline_writes_json_output(self):
        class ExtractStage(Stage):
            def __init__(self, csv_file):
                super(ExtractStage, self).__init__("Extract")
                self.csv_file = csv_file

            def run(self, data):
                rows = []
                with open(self.csv_file) as f:
                    for row in csv.DictReader(f):
                        rows.append(row)
                data['raw'] = rows

        class TransformStage(Stage):
            def __init__(self):
                super(TransformStage, self).__init__("Transform")

            def run(self, data):
                transformed = []
                for row in data['raw']:
                    transformed.append({
                        'name': row['Name'].upper(),
                        'age': int(row['Age'])
                    })
                data['transformed'] = transformed

        class LoadStage(Stage):
            def __init__(self, output_file):
                super(LoadStage, self).__init__("Load")
                self.output_file = output_file

            def run(self, data):
                with open(self.output_file, 'w') as f:
                    json.dump(data['transformed'], f)

        temp_dir = tempfile.mkdtemp(prefix='pali-etl-test-')
        try:
            csv_path = os.path.join(temp_dir, 'input.csv')
            output_path = os.path.join(temp_dir, 'output.json')

            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['Name', 'Age'])
                writer.writeheader()
                writer.writerow({'Name': 'Alice', 'Age': '30'})
                writer.writerow({'Name': 'Bob', 'Age': '25'})

            pipeline = Pipeline(
                name='ETLPipeline',
                stages=[ExtractStage(csv_path), TransformStage(), LoadStage(output_path)],
                data={}
            )
            pipeline._run()

            with open(output_path, 'r') as f:
                result = json.load(f)

            self.assertEqual(result, [
                {'name': 'ALICE', 'age': 30},
                {'name': 'BOB', 'age': 25}
            ])
        finally:
            for path in [csv_path, output_path]:
                try:
                    os.remove(path)
                except OSError:
                    pass
            try:
                os.rmdir(temp_dir)
            except OSError:
                pass


if __name__ == '__main__':
    unittest.main()
