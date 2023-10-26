class AdditionalService:
    def __init__(self, name, price, price_for, price_desc, image, description):
        self.name = name
        self.price = price
        self.price_for = price_for
        self.price_desc = price_desc
        self.image = image
        self.description = description

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_price_for(self):
        return self.price_for

    def get_price_desc(self):
        return self.price_desc

    def get_image(self):
        return self.image

    def get_description(self):
        return self.description

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "unit": self.price_for,
            "price_info": self.price_desc,
            "image_path": self.image,
            "description": self.description
        }

    def __str__(self):
        return f"{self.name} - {self.price}€"


