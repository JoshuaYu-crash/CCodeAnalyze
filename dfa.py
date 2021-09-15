import copy


class DFA:

    def __init__(self, keyword_list: list):
        self.state_event_dict = self._generate_state_event_dict(keyword_list)

    @staticmethod
    def _generate_state_event_dict(keyword_list: list) -> dict:
        state_event_dict = {}

        for keyword in keyword_list:
            current_dict = state_event_dict
            length = len(keyword)

            for index, char in enumerate(keyword):
                if char not in current_dict:
                    next_dict = {"is_end": False}
                    current_dict[char] = next_dict
                    current_dict = next_dict
                else:
                    next_dict = current_dict[char]
                    current_dict = next_dict

                if index == length - 1:
                    current_dict["is_end"] = True

        return state_event_dict

    def match(self, content: str):
        match_list = []
        state_list = []
        temp_match_list = []
        conlen = len(content)

        for char_pos, char in enumerate(content):
            if char in self.state_event_dict:
                state_list.append(self.state_event_dict)
                temp_match_list.append({
                    "start": char_pos,
                    "match": ""
                })

            for index, state in enumerate(state_list):
                if char in state:
                    state_list[index] = state[char]
                    temp_match_list[index]["match"] += char

                    if state[char]["is_end"]:
                        # and (char_pos + 1 < and content[char_pos + 1] not in state[char])
                        # if next char in state[char], then the match can not finish
                        if not (char_pos + 1 < conlen and content[char_pos + 1] in state[char]):
                            match_list.append(copy.deepcopy(temp_match_list[index]))
                            # print(char_pos+1, content[char_pos + 1], state[char])

                        # if the state[char] have no char, then delete this state
                        if len(state[char].keys()) == 1:
                            state_list[index] = None
                            temp_match_list[index] = None
                            # state_list.pop(index)
                            # temp_match_list.pop(index)
                else:
                    state_list[index] = None
                    temp_match_list[index] = None
                    # state_list.pop(index)
                    # temp_match_list.pop(index)
            state_list = [i for i in state_list if i]
            temp_match_list = [i for i in temp_match_list if i]

        return match_list
