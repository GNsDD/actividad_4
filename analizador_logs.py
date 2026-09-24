# -*- coding: utf-8 -*-
from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w']+")
STOP_WORDS = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'en', 'y', 'o',
    'que', 'es', 'son', 'para', 'por', 'con', 'su', 'sus', 'al', 'se', 'lo', 'como',
    'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'by', 'is', 'it'
}

class MRAnalizadorLogs(MRJob):
    def mapper(self, _, line):
        line_lower = line.lower()
        
        if "error" in line_lower:
            yield "LOG_ERROR_TOTAL", 1
        elif "critical" in line_lower:
            yield "LOG_CRITICAL_TOTAL", 1
            
        codigos_http = re.findall(r'\b(4\d{2}|5\d{2})\b', line)
        for codigo in codigos_http:
            yield f"HTTP_STATUS_{codigo}", 1

        palabras = WORD_RE.findall(line_lower)
        for palabra in palabras:
            if palabra not in STOP_WORDS and not palabra.isdigit() and len(palabra) > 2:
                yield f"PALABRA_{palabra}", 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRAnalizadorLogs.run()
