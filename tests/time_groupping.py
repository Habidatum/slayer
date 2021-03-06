import pandas as pd
from isodate import parse_duration
from slayer.generation.plugins.point import Generator
from slayer.generation import utils
from slayer import constants


def test_minutes_ratio():
    assert_aggregation_ratio(parse_duration('PT1M'), parse_duration('PT15M'))
    assert_aggregation_ratio(parse_duration('PT5M'), parse_duration('PT15M'))
    assert_aggregation_ratio(parse_duration('PT10M'), parse_duration('PT15M'))


def test_days_ratio():
    assert_aggregation_ratio(parse_duration('P1D'), parse_duration('P7D'))


def test_days_to_week_ratio():
    assert_aggregation_ratio(parse_duration('P1D'), parse_duration('P1W'))


def test_minutes_lost():
    assert_nothing_is_lost(parse_duration('PT1M'), parse_duration('PT15M'))
    assert_nothing_is_lost(parse_duration('PT5M'), parse_duration('PT15M'))
    assert_nothing_is_lost(parse_duration('PT10M'), parse_duration('PT15M'))


def test_days_lost():
    assert_nothing_is_lost(parse_duration('P1D'), parse_duration('P7D'))


def test_days_to_week_lost():
    assert_nothing_is_lost(parse_duration('P1D'), parse_duration('P1W'))


def assert_nothing_is_lost(source_duration, target_duration):
    generator = Generator(**basic_generator_stub())
    month_df = month_df_stub(source_duration)
    time_slices = generator.group_by_time(month_df, target_duration)
    grouped_len = sum([len(group) for ts, group in time_slices])
    assert grouped_len == len(month_df)


def assert_aggregation_ratio(source_duration, target_duration):
    generator = Generator(**basic_generator_stub())
    month_df = month_df_stub(source_duration)
    time_slices = generator.group_by_time(month_df, target_duration)
    assert len(month_df)/len(time_slices) == target_duration/source_duration


def test_minutes_intervals():
    time_intervals = basic_generator_stub()['time_intervals']
    slice_duration = parse_duration('PT30M')
    assert_timeinterval_filtering(time_intervals, slice_duration)


def assert_timeinterval_filtering(time_intervals, slice_duration):
    intervals = utils.convert_time_intervals(time_intervals)
    month_df = month_df_stub(slice_duration)
    data = utils.index_datetime(month_df)
    data = utils.filter_df_time_intervals(data, intervals)


def test_intervals_clap():
    time_intervals = basic_generator_stub()['time_intervals']
    clapped_intervals = utils.clap_time_intervals(time_intervals, 'P1D')
    assert clapped_intervals[0][0] == '2012-08-07T00:00:00Z'
    assert clapped_intervals[1][1] == '2013-09-07T00:00:00Z'


def basic_generator_stub():
    return {'bbox': {'bottom_right_lat': 39.54462, 'top_left_lat': 39.98894,
                     'top_left_lon': -105.26372, 'bottom_right_lon': -104.63632},
            'cell_size': 100,
            'time_intervals': [['2012-08-07T14:10:30Z', '2012-09-07T14:10:30Z'],
                               ['2013-08-07T14:10:30Z', '2013-09-07T14:10:30Z']]}


def month_df_stub(duration):
    if duration < parse_duration('P1D'):
        time_range = pd.date_range('1/1/2012', periods=60 * 24 * 30,
                                   freq=duration)
    else:
        time_range = pd.date_range('1/1/2012', periods=7 * 50,
                                   freq=duration)
    return pd.DataFrame({constants.start_date_column: time_range})
