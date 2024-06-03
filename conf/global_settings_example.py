"""
Default settings example. Copy this file as 'global_settings.py' in this repository.
"""

DFS_CYCLE = {
    "max_depth": 5,
    "edge_removal": None,  # Possible values: None, "current_node", "failed_cycle_nodes"
}

ITEMS = {"min_value": 50, "max_value": 500, "value_step": 50}

TESTS = {
    "users_file_name": "users.json",
    "items_file_name": "items.json",
    "cycles_file_name": "output.json",
    "users_to_generate": 100,
    "items_per_user": 30,
    "items_wished_per_user": 30,
}
