from hestia_earth.schema import TermTermType, AnimalReferencePeriod
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import debugValues
from hestia_earth.models.utils.input import get_feed_inputs
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.property import get_node_property, get_node_property_value, node_property_lookup_value
from .utils import get_milkYield_practice
from . import MODEL

MODEL_KEY = 'pastureGrass'
KEY_TERM_TYPES = [
    TermTermType.LANDCOVER.value
]


def practice_input_id(practice: dict):
    return get_lookup_value(practice.get('key', {}), 'grazedPastureGrassInputId', model=MODEL, model_key=MODEL_KEY)


def _get_grouping(animal: dict) -> str:
    term = animal.get('term', {})
    return get_lookup_value(term, 'ipcc2019AnimalTypeGrouping', model=MODEL, model_key=MODEL_KEY)


def _get_activityCoefficient(cycle: dict, animal: dict, system: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')
    system_id = system.get('term', {}).get('@id')
    lookup = download_lookup('system-liveAnimal-activityCoefficient-ipcc2019.csv')
    activityCoefficient = safe_parse_float(get_table_value(lookup, 'termid', system_id, column_name(term_id)), 0)

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                activityCoefficient=activityCoefficient)

    return activityCoefficient


def _calculate_NEm(cycle: dict, animal: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    mjDayKgCfiNetEnergyMaintenance = safe_parse_float(
        get_lookup_value(term, 'mjDayKgCfiNetEnergyMaintenanceIpcc2019', model=MODEL, model_key=MODEL_KEY), 0
    )
    liveweightPerHead = get_node_property(animal, 'liveweightPerHead', False).get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEm = mjDayKgCfiNetEnergyMaintenance * pow(liveweightPerHead, 0.75) * animal_value * cycleDuration

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                mjDayKgCfiNetEnergyMaintenance=mjDayKgCfiNetEnergyMaintenance,
                liveweightPerHead=liveweightPerHead,
                NEm=NEm)

    return NEm


def _calculate_NEa_cattleAndBuffalo(cycle: dict, animal: dict, system: dict, NEm: float, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    activityCoefficient = _get_activityCoefficient(cycle, animal, system, log_node)

    NEa = activityCoefficient * NEm

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                NEa=NEa)

    return NEa


def _calculate_NEa_sheepAndGoat(cycle: dict, animal: dict, system: dict, _NEm: float, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    activityCoefficient = _get_activityCoefficient(cycle, animal, system, log_node)

    liveweightPerHead = get_node_property(animal, 'liveweightPerHead', False).get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEa = activityCoefficient * liveweightPerHead * animal_value * cycleDuration

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                liveweightPerHead=liveweightPerHead,
                NEa=NEa)

    return NEa


_NEa_BY_GROUPING = {
    'cattleAndBuffalo': _calculate_NEa_cattleAndBuffalo,
    'sheepAndGoat': _calculate_NEa_sheepAndGoat
}


def _calculate_NEa(cycle: dict, animal: dict, system: dict, NEm: float, log_node: dict) -> float:
    grouping = _get_grouping(animal)
    return _NEa_BY_GROUPING.get(grouping, lambda *args: 0)(cycle, animal, system, NEm, log_node)


def _calculate_NEl_cattleAndBuffalo(cycle: dict, animal: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    milkYieldPractice = get_milkYield_practice(animal)
    milkYield = list_sum(milkYieldPractice.get('value', []))
    fatContent = get_node_property(milkYieldPractice, 'fatContent').get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEl = milkYield * (1.47 + (0.4 * fatContent)) * animal_value * cycleDuration

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                milkYield=milkYield,
                fatContent=fatContent,
                NEl=NEl)

    return NEl


def _calculate_NEl_sheepAndGoat(cycle: dict, animal: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    milkYieldPractice = get_milkYield_practice(animal)
    milkYield = list_sum(milkYieldPractice.get('value', []))
    EV_milk = safe_parse_float(
        get_lookup_value(milkYieldPractice.get('term', {}), 'mjKgEvMilkIpcc2019', model=MODEL, model_key=MODEL_KEY),
        0
    )
    default_fatContent = safe_parse_float(
        get_lookup_value(milkYieldPractice.get('term', {}),
                         'defaultFatContentEvMilkIpcc2019', model=MODEL, model_key=MODEL_KEY),
        7
    )
    fatContent = get_node_property(milkYieldPractice, 'fatContent').get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEl = milkYield * (EV_milk * fatContent/default_fatContent) * animal_value * cycleDuration

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                milkYield=milkYield,
                EV_milk=EV_milk,
                NEl=NEl)

    return NEl


_NEl_BY_GROUPING = {
    'cattleAndBuffalo': _calculate_NEl_cattleAndBuffalo,
    'sheepAndGoat': _calculate_NEl_sheepAndGoat
}


def _calculate_NEl(cycle: dict, animal: dict, log_node: dict) -> float:
    grouping = _get_grouping(animal)
    return _NEl_BY_GROUPING.get(grouping, lambda *args: 0)(cycle, animal, log_node)


def _calculate_NEwork(cycle: dict, animal: dict, NEm: float, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    hoursWorkedPerDay = get_node_property(animal, 'hoursWorkedPerDay').get('value', 0)
    NEwork = 0.1 * NEm * hoursWorkedPerDay

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                hoursWorkedPerDay=hoursWorkedPerDay,
                NEwork=NEwork)

    return NEwork


def _get_pregnancy_ratio_per_birth(animal: dict, value: str) -> float:
    animalsPerBirth = get_node_property(animal, 'animalsPerBirth').get('value', 3)
    single = safe_parse_float(extract_grouped_data(value, 'singleBirth'), 0)
    double = safe_parse_float(extract_grouped_data(value, 'doubleBirth'), 0)
    tripple = safe_parse_float(extract_grouped_data(value, 'tripleBirthOrMore'))
    return (
        single if animalsPerBirth <= 1 else
        ((animalsPerBirth-1)/2)*single * (1-((animalsPerBirth-1)/2)*double) if 1 < animalsPerBirth < 2 else
        double if animalsPerBirth == 2 else
        ((animalsPerBirth-2)/3)*double * (1-((animalsPerBirth-2)/3)*tripple) if 2 < animalsPerBirth < 3 else
        tripple
    )


def _get_pregnancy_ratio(animal: dict) -> float:
    term = animal.get('term', {})
    value = get_lookup_value(term, 'ratioCPregnancyNetEnergyPregnancyIpcc2019', model=MODEL, model_key=MODEL_KEY)
    return _get_pregnancy_ratio_per_birth(animal, value) if ';' in value else safe_parse_float(value, 0)


def _calculate_NEp(cycle: dict, animal: dict, NEm: float, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    ratioCPregnancyNetEnergyPregnancy = _get_pregnancy_ratio(animal)
    pregnancyRateTotal = get_node_property(animal, 'pregnancyRateTotal').get('value', 0)
    NEp = ratioCPregnancyNetEnergyPregnancy * pregnancyRateTotal/100 * NEm

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                ratioCPregnancyNetEnergyPregnancy=ratioCPregnancyNetEnergyPregnancy,
                pregnancyRateTotal=pregnancyRateTotal,
                NEp=NEp)

    return NEp


def _calculate_NEg_cattleAndBuffalo(cycle: dict, animal: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    ratioCNetEnergyGrowthCattleBuffalo = safe_parse_float(
        get_lookup_value(term, 'ratioCNetEnergyGrowthCattleBuffaloIpcc2019', model=MODEL, model_key=MODEL_KEY), 0
    )
    liveweightPerHead = get_node_property(animal, 'liveweightPerHead').get('value', 0)
    weightAtMaturity = get_node_property(animal, 'weightAtMaturity').get('value', 0)
    liveweightGain = get_node_property(animal, 'liveweightGain').get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEg = 22.02 * \
        pow(liveweightPerHead / (ratioCNetEnergyGrowthCattleBuffalo * weightAtMaturity), 0.75) * \
        pow(liveweightGain, 1.097) * \
        animal_value * cycleDuration if all([
            ratioCNetEnergyGrowthCattleBuffalo * weightAtMaturity > 0
        ]) else 0

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                ratioCNetEnergyGrowthCattleBuffalo=ratioCNetEnergyGrowthCattleBuffalo,
                liveweightPerHead=liveweightPerHead,
                weightAtMaturity=weightAtMaturity,
                liveweightGain=liveweightGain,
                NEg=NEg)

    return NEg


def _calculate_NEg_sheepAndGoat(cycle: dict, animal: dict, log_node: dict) -> float:
    term = animal.get('term', {})
    term_id = term.get('@id')

    MjKgABNetEnergyGrowthSheepGoats = get_lookup_value(
        term, 'MjKgABNetEnergyGrowthSheepGoatsIpcc2019', model=MODEL, model_key=MODEL_KEY)
    MjKg_a = safe_parse_float(extract_grouped_data(MjKgABNetEnergyGrowthSheepGoats, 'a'), 0)
    MjKg_b = safe_parse_float(extract_grouped_data(MjKgABNetEnergyGrowthSheepGoats, 'b'), 0)
    BWi = get_node_property(animal, 'weightAtWeaning').get('value', 0)
    BWf = get_node_property(animal, 'weightAtOneYear').get('value', 0) or \
        get_node_property(animal, 'weightAtSlaughter').get('value', 0)
    animal_value = animal.get('value', 0)
    cycleDuration = cycle.get('cycleDuration', 365)
    NEg = (BWf - BWi) * (MjKg_a + 0.5 * MjKg_b * (BWi + BWf)) / 365 * animal_value * cycleDuration

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                MjKg_a=MjKg_a,
                MjKg_b=MjKg_b,
                BWi=BWi,
                BWf=BWf,
                NEg=NEg)

    return NEg


_NEg_BY_GROUPING = {
    'cattleAndBuffalo': _calculate_NEg_cattleAndBuffalo,
    'sheepAndGoat': _calculate_NEg_sheepAndGoat
}


def _calculate_NEg(cycle: dict, animal: dict, log_node: dict) -> float:
    grouping = _get_grouping(animal)
    return _NEg_BY_GROUPING.get(grouping, lambda *args: 0)(cycle, animal, log_node)


def _pastureGrass_key_property_value(practice: dict, column: dict):
    term_id = practice_input_id(practice)
    term = download_hestia(term_id)
    term_type = term.get('termType')
    value = list_sum(practice.get('value', [0]))
    lookup_value = node_property_lookup_value(MODEL, {'@id': term_id, 'termType': term_type}, column, default=0)
    return (lookup_value, value)


def calculate_REM(energy: float = 0) -> float:
    return 1.123 - (4.092/1000 * energy) + (1.126/100000 * pow(energy, 2)) - (25.4/energy) if energy > 0 else 0


def calculate_REG(energy: float = 0) -> float:
    return 1.164 - (5.16/1000 * energy) + (1.308/100000 * pow(energy, 2)) - (37.4/energy) if energy > 0 else 0


def _calculate_feed_meanDE(log_node: dict, input: dict) -> float:
    term_id = input.get('term', {}).get('@id')

    energyContent = get_node_property_value(MODEL, input, 'energyContentHigherHeatingValue')
    energyDigestibility = get_node_property_value(MODEL, input, 'energyDigestibilityRuminants')
    meanDE = energyContent * energyDigestibility if all([energyContent, energyDigestibility]) else 0

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                energyContent=energyContent,
                energyDigestibility=energyDigestibility,
                meanDE=meanDE)

    return meanDE


def _calculate_NEfeed_m(log_node: dict, input: dict, meanDE: float) -> float:
    term_id = input.get('term', {}).get('@id')

    energyDigestibility = get_node_property_value(MODEL, input, 'energyDigestibilityRuminants', default=0)
    REm = calculate_REM(energyDigestibility * 100)

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                REm=REm)

    input_value = list_sum(input.get('value'))
    return meanDE * REm * input_value


def _calculate_NEfeed_g(log_node: dict, input: dict, meanDE: float) -> float:
    term_id = input.get('term', {}).get('@id')

    energyDigestibility = get_node_property_value(MODEL, input, 'energyDigestibilityRuminants', default=0)
    REg = calculate_REG(energyDigestibility * 100)

    debugValues(log_node, model=MODEL, term=term_id, model_key=MODEL_KEY,
                REg=REg)

    input_value = list_sum(input.get('value'))
    return meanDE * REg * input_value


def calculate_NEfeed(node: dict) -> tuple:
    inputs = get_feed_inputs(node)
    # calculate meanDE for each input first
    inputs = [(input, _calculate_feed_meanDE(node, input)) for input in inputs]
    NEfeed_m = sum([
        _calculate_NEfeed_m(node, input, meanDE) for (input, meanDE) in inputs
    ]) if len(inputs) > 0 else 0
    NEfeed_g = sum([
        _calculate_NEfeed_g(node, input, meanDE) for (input, meanDE) in inputs
    ]) if len(inputs) > 0 else 0

    return (NEfeed_m, NEfeed_g)


def get_animal_values(cycle: dict, animal: dict, system: dict, log_node: dict):
    NEm = _calculate_NEm(cycle, animal, log_node=log_node)
    NEa = _calculate_NEa(cycle, animal, system, NEm, log_node=log_node)
    NEl = _calculate_NEl(cycle, animal, log_node=log_node)
    NEwork = _calculate_NEwork(cycle, animal, NEm, log_node=log_node)
    NEp = _calculate_NEp(cycle, animal, NEm, log_node=log_node)
    NEg = _calculate_NEg(cycle, animal, log_node=log_node)

    return (NEm, NEa, NEl, NEwork, NEp, NEg)


def calculate_meanECHHV(practices: list) -> float:
    values = list(map(lambda p: _pastureGrass_key_property_value(p, 'energyContentHigherHeatingValue'), practices))
    total_weight = sum([weight/100 for _value, weight in values])
    return sum([
        (value * weight/100 if all([value, weight]) else 0) for value, weight in values
    ]) / total_weight if total_weight > 0 else 0


def calculate_meanDE(practices: list) -> float:
    values = list(map(lambda p: _pastureGrass_key_property_value(p, 'energyDigestibilityRuminants'), practices))
    total_weight = sum([weight/100 for _value, weight in values])
    meanDE = sum([
        (value * weight/100 if all([value, weight]) else 0) for value, weight in values
    ]) / total_weight if total_weight > 0 else 0

    return meanDE


def product_wool_energy(product: dict):
    return safe_parse_float(get_lookup_value(product.get('term', {}), 'mjKgEvWoolNetEnergyWoolIpcc2019'), 24)


def should_run_practice(cycle: dict):
    def should_run(practice: dict):
        term_id = practice.get('term', {}).get('@id')
        key_term_type = practice.get('key', {}).get('termType')
        value = practice.get('value', [])
        return all([len(value) > 0, term_id == MODEL_KEY, key_term_type in KEY_TERM_TYPES])

    return should_run


def get_animals(cycle: dict):
    return [
        a for a in cycle.get('animals', []) if all([
            a.get('value'),
            a.get('referencePeriod') == AnimalReferencePeriod.AVERAGE.value
        ])
    ]
