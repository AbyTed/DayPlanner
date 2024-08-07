def day_planner(data: dict):
    """
    {name:diff, break_time, time}
    """
    # Sort activities within each difficulty level
    classified = [(key, *value) for key, value in data.items()]

    items_list = dict(
        [
            (activity[0], (activity[1], activity[2], activity[3]))
            for activity in (
                sorted(
                    ([x for x in classified if x[1] == "h"]),
                    key=lambda x: x[3],
                    reverse=True,
                )
                + sorted(
                    ([x for x in classified if x[1] == "m"]),
                    key=lambda x: x[3],
                    reverse=True,
                )
                + sorted(
                    ([x for x in classified if x[1] == "e"]),
                    key=lambda x: x[3],
                    reverse=True,
                )
            )
        ]
    )

    return items_list
