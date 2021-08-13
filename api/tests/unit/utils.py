import pytest
from pydantic import ValidationError


def parent_setup(self):
    if self.parent:
        print("Parent:", self.parent.example_data)
        self.correct_data = map(lambda x: {**self.parent.example_data, **x}, self.correct_data)
        self.wrong_data = map(lambda x: {**self.parent.example_data, **x}, self.wrong_data)
        self.irregular_data = map(lambda x: {**self.parent.example_data, **x}, self.irregular_data)


class BaseModelTest:
    schema = None
    parent = None
    example_data = {}
    correct_data = []
    wrong_data = []
    irregular_data = []

    def test_validate(self):
        parent_setup(self)

        for correct in [*self.correct_data, self.example_data]:
            print("Correct:", correct)
            print("Parsed:", self.schema(**correct))
            assert self.schema(**correct) == correct

        for wrong in self.wrong_data:
            with pytest.raises(ValidationError):
                print("Wrong:", wrong)
                print("Parsed:", self.schema(**wrong))

    def test_parsing(self):
        parent_setup(self)

        for irregular in self.irregular_data:
            print("Irregular:", irregular)
            print("Parsed:", self.schema(**irregular))
            assert self.schema(**irregular) == self.example_data
