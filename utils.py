"""Utils module of kytos/pathfinder Kytos Network Application."""


def lazy_filter(filter_type, filter_func):
    """Lazy typed filter on top of the built-in function, it's meant
    to be used when the values to be filtered for are only defined later on
    dynamically at runtime."""

    def filter_closure(value, items):
        if not isinstance(value, filter_type):
            raise TypeError(f"Expected type: {filter_type}")
        return filter(filter_func(value), items)

    return filter_closure


def nx_edge_data_weight(u, v, edge_data):
    """Helper function callback meant to be used with nx shortest path methods
    that take a weight callback, providing a fallback default value"""

    if edge_data.get("hop"):
        return edge_data["hop"]
    return 1


def nx_edge_data_delay(u, v, edge_data):
    """Helper function callback meant to be used with nx shortest path methods
    that take a weight callback, providing a fallback default value"""

    if edge_data.get("delay"):
        return edge_data["delay"]
    return 1


def nx_edge_data_priority(u, v, edge_data):
    """Helper function callback meant to be used with nx shortest path methods
    that take a weight callback, providing a fallback default value"""

    if edge_data.get("priority"):
        return edge_data["priority"]
    return 1


def filter_le(metric):
    return lambda x: (lambda nx_edge_tup: nx_edge_tup[2].get(metric, x) <= x)


def filter_ge(metric):
    return lambda x: (lambda nx_edge_tup: nx_edge_tup[2].get(metric, x) >= x)


def filter_in(metric):
    return lambda x: (lambda nx_edge_tup: x in nx_edge_tup[2].get(metric, {x}))
