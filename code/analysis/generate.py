import os

from src.effort.activity_generator import ActivityGenerator
from src.effort.spectra import Spectra
from src.effort.util import to_str

current_dir = os.path.dirname(__file__)
directory = os.path.normpath(os.path.join(current_dir, 'output/spectra'))


def generate_matrices(rounds, cardinality, goodness):
    for filename in os.listdir(directory):
        # print(filename)
        spectra = Spectra('output/spectra/%s' % filename)
        activity_generator = ActivityGenerator(spectra, cardinality)

        # IF-statement only necessary to control for failures and passes.
        if len(activity_generator.candidates_with_error) >= 20:
            output = 'output/matrices/%s' % filename
            if not os.path.exists(output):
                os.makedirs(output)

            fault_sets = []

            while len(fault_sets) < rounds:
                activity_matrix, faulty_set = activity_generator.generate(goodness, True)
                faulty_set.sort()
                h = hash(frozenset(faulty_set))
                if h not in fault_sets:
                    # print(faulty_set)
                    fault_sets.append(h)
                    name = '_'.join(to_str(faulty_set))
                    with open('output/matrices/%s/%s.txt' % (filename, name), 'w') as f:
                        for column in activity_matrix:
                            f.write(' '.join(to_str(column)))
                            f.write('\n')


if __name__ == "__main__":
    generate_matrices(20, 2, 0)
