import fastedit
import filecmp
import itertools
import os
import tempfile
import unittest


class FasteditTests(unittest.TestCase):
    def test_get(self):
        test_fasta = "test/test.fasta"
        expected = "test/get_output.csv"
        tempfile_path = tempfile.mkstemp()[1]
        try:
            fastedit.get_headers(test_fasta, out=tempfile_path)
            with open(expected) as exp, open(tempfile_path) as tmp:
                for a, b in itertools.izip(exp, tmp):
                    assert a.strip() == b.strip()
        finally:
            os.remove(tempfile_path)

    def test_get_gzip(self):
        test_fasta = "test/test.fasta.gz"
        expected = "test/get_output.csv"
        tempfile_path = tempfile.mkstemp()[1]
        try:
            fastedit.get_headers(test_fasta, out=tempfile_path)
            with open(expected) as exp, open(tempfile_path) as tmp:
                for a, b in itertools.izip(exp, tmp):
                    assert a.strip() == b.strip()
        finally:
            os.remove(tempfile_path)

    def test_put(self):
        test_fasta = "test/test.fasta"
        expected = "test/put_output.fasta"
        put_input = "test/put_input.csv"
        tempfile_path = tempfile.mkstemp()[1]
        try:
            fastedit.put_headers(test_fasta, put_input, out=tempfile_path)
            with open(expected) as exp, open(tempfile_path) as tmp:
                for a, b in itertools.izip(exp, tmp):
                    assert a.strip() == b.strip()
        finally:
            os.remove(tempfile_path)


if __name__ == '__main__':
    unittest.main()
