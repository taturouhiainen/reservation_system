class JetSki:
    def __init__(self, id, label, color, availability=True, additional_info=None):
        self.id = id
        self.label = label
        self.color = color
        self.availability = availability
        self.additional_info = additional_info

    def get_label(self):
        return self.label

    def get_color(self):
        return self.color

    def get_id(self):
        return self.id

    def __str__(self):
        return f"Jet Ski {self.id}: {self.label}, color: {self.color}, available: {self.availability}"
