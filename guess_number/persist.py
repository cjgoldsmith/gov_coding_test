import json
import structlog

log = structlog.get_logger()

DEFAULT_PERSIST_FILE = '/var/data/one_persist.data'
SUM_RETURNS = 'sum_returns'
TOTAL_CALLS = 'total_calls'
AVERAGE = 'average'

_accumulated_results = {
    TOTAL_CALLS: 0,
    SUM_RETURNS: 0,
    AVERAGE: 0.0,
}


def accumulate(func):
    """
    Function decorator which accumulates aggregated
    return results over multiple calls.
    """

    def wrapper(*args, **kwargs):
        rval = func(*args, **kwargs)
        (_, result) = rval
        _accumulated_results[TOTAL_CALLS] += 1
        _accumulated_results[SUM_RETURNS] += result
        _accumulated_results[AVERAGE] = _accumulated_results[SUM_RETURNS] / \
            _accumulated_results[TOTAL_CALLS]
        return rval
    return wrapper


def get_accumulated():
    return _accumulated_results


def persist_results(func):
    """
    Function decorator which stores aggregated
    return results over multiple calls across multiple
    process invokations.
    """
    name = func.__name__

    def wrapper(*args, **kwargs):
        rval = func(*args, **kwargs)
        (_, result) = rval
        with open(DEFAULT_PERSIST_FILE, 'r') as data_file:
            file_content = data_file.read()
        with open(DEFAULT_PERSIST_FILE, 'w') as data_file:
            existing_data = json.loads(file_content) if file_content else {}
            current = existing_data.get(name, {
                SUM_RETURNS: 0,
                TOTAL_CALLS: 0,
                AVERAGE: 0.0,
            })
            current[TOTAL_CALLS] += 1
            current[SUM_RETURNS] += result
            current[AVERAGE] = current[SUM_RETURNS] / current[TOTAL_CALLS]
            existing_data[name] = current
            data_file.write(json.dumps(existing_data))
        log.msg('Persistant data store', data=existing_data)
        return rval
    return wrapper


def persist_clear():
    """
    Clear out the persistant data file.
    """
    with open(DEFAULT_PERSIST_FILE, 'w') as data_file:
        pass


def get_persist():
    """
    Retrieve the entire persistant data file.
    """
    with open(DEFAULT_PERSIST_FILE, 'r') as data_file:
        return json.loads(data_file.read())
