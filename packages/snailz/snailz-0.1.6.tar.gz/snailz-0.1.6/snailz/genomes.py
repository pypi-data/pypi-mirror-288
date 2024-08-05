'''Generate genomes with random mutations.'''

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import random

from .params import GenomeParams, load_params


# Bases.
DNA = 'ACGT'


@dataclass
class GenePool:
    '''Keep track of generated genomes.'''

    length: int
    reference: str
    individuals: list[str]
    locations: list[int]
    susceptible_loc: int = 0
    susceptible_base: str = ''


def genomes(options):
    '''Main driver.'''
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(GenomeParams, options.params)
    random.seed(options.params.seed)
    data = _random_genomes(options.params)
    _add_susceptibility(data)
    _save(options.outfile, data)


def _add_susceptibility(data):
    '''Add indication of genetic susceptibility.'''
    if not data.locations:
        return
    loc = _choose_one(data.locations)
    choices = {ind[loc] for ind in data.individuals} - {data.reference[loc]}
    data.susceptible_loc = loc
    data.susceptible_base = _choose_one(list(sorted(choices)))


def _random_bases(length):
    '''Generate a random sequence of bases of the specified length.'''
    assert 0 < length
    return ''.join(random.choices(DNA, k=length))


def _random_genomes(params):
    '''Generate a set of genomes with specified number of point mutations.'''
    assert 0 <= params.num_snp <= params.length

    # Reference genomes and specific genomes to modify.
    reference = _random_bases(params.length)
    individuals = [reference] * params.num_genomes

    # Locations for SNPs.
    locations = random.sample(list(range(params.length)), params.num_snp)

    # Introduce significant mutations.
    for loc in locations:
        candidates = _other_bases(reference, loc)
        bases = [reference[loc]] + random.sample(candidates, k=len(candidates))
        individuals = [_mutate_snps(params, reference, ind, loc, bases) for ind in individuals]

    # Introduce other random mutations.
    other_locations = list(set(range(params.length)) - set(locations))
    individuals = [
        _mutate_other(ind, params.prob_other, other_locations) for ind in individuals
    ]

    # Return structure.
    individuals.sort()
    locations.sort()
    return GenePool(
        length=params.length, reference=reference, individuals=individuals, locations=locations
    )


def _save(outfile, data):
    '''Save or show generated data.'''
    as_text = json.dumps(asdict(data), indent=4)
    if outfile:
        Path(outfile).write_text(as_text)
    else:
        print(as_text)


def _mutate_snps(params, reference, genome, loc, bases):
    '''Introduce single nucleotide polymorphisms at the specified location.'''
    choice = _choose_one(bases, params.snp_probs)
    return genome[:loc] + choice + genome[loc + 1 :]


def _mutate_other(genome, prob, locations):
    '''Introduce other mutations at specified locations.'''
    if random.random() > prob:
        return genome
    loc = random.sample(locations, k=1)[0]
    base = random.choice(_other_bases(genome, loc))
    genome = genome[:loc] + base + genome[loc + 1 :]
    return genome


def _choose_one(values, weights=None):
    '''Convenience wrapper to choose a single items with weighted probabilities.'''
    return random.choices(values, weights=weights, k=1)[0]


def _other_bases(seq, loc):
    '''Create a list of bases minus the one in the sequence at that location.

    We return a list instead of a set because the result is used in random.choices(),
    which requires an indexable sequence. We sort for reproducibility.
    '''
    return list(sorted(set(DNA) - {seq[loc]}))
