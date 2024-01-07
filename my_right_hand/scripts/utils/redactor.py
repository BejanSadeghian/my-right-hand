from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from icecream import ic

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def redactor(text):
    results = analyzer.analyze(text=text, language="en")
    results = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )
    ic(results)
    return results.text
