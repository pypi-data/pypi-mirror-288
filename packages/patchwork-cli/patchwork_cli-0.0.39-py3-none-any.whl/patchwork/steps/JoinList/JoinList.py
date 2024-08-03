from patchwork.step import Step
from patchwork.steps.JoinList.typed import JoinListInputs


class JoinList(Step):
    def __init__(self, inputs):
        missing_keys = JoinListInputs.__required_keys__.difference(inputs.keys())
        if len(missing_keys) > 0:
            raise ValueError(f"Missing required data: {missing_keys}")

        self.list = inputs["list"]
        self.delimiter = inputs["delimiter"]

    def run(self):
        items = []
        for item in self.list:
            if isinstance(item, str):
                items.append(item)
            elif isinstance(item, dict):
                if "body" in item.keys() or len(item.keys()) < 1:
                    items.append(item.get("body"))
                elif "text" in item.keys():
                    items.append(item.get("text"))
                else:
                    items.append(str(item))
            else:
                items.append(str(item))

        return dict(text=self.delimiter.join(items))
