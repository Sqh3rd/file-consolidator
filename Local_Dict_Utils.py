class Local_Dict_Utils:
    def _modify_counter(self, dict_to_modify: dict, key_to_modify: object, modifier: int) -> dict[object, object]:
        if key_to_modify in dict_to_modify:
            dict_to_modify[key_to_modify] += modifier
        else:
            dict_to_modify[key_to_modify] = modifier
        return dict_to_modify
    
    def increase_counter(self, dict_to_modify: dict, key_to_modify: object) -> dict[object, object]:
        return self._modify_counter(dict_to_modify, key_to_modify, 1)
    
    def decrease_counter(self, dict_to_modify: dict, key_to_modify: object) -> dict[object, object]:
        return self._modify_counter(dict_to_modify, key_to_modify, -1)