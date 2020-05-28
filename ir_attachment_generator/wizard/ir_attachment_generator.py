# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import base64
import io
import logging
from PIL import Image
import random

from odoo import _, fields, models


logger = logging.getLogger(__name__)


class IrAttachmentGenerator(models.TransientModel):

    _name = "ir.attachment.generator"
    _description = "Random ir.attachment generator"

    number = fields.Integer(default=100)
    width = fields.Integer(default=100)
    height = fields.Integer(default=100)

    def _generate_image(self):
        image = Image.new("RGB", size=(self.width, self.height))
        pixels = image.load()
        for x in range(self.width):
            for y in range(self.height):
                pixels[x, y] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
        return image

    def generate_attachments(self):
        self.ensure_one()
        logger.info(
            "Generating %s images of width %s px and height %s px" % (
                self.number, self.width, self.height
            )
        )
        created_ids = list()
        for i in range(1, self.number + 1):
            logger.info(
                "Generating image %s / %s" % (i, self.number)
            )
            file_object = io.BytesIO()
            image_data = self._generate_image()
            image_data.save(file_object, format="PNG")
            attachment = self.env["ir.attachment"].create(
                {
                    "res_model": self._name,
                    "res_id": self.id,
                    "name": "Random generated image %s" % i,
                    "datas": base64.b64encode(file_object.getvalue()),
                    "datas_fname": "random_generated_image_%s.png" % i,
                }
            )
            created_ids.append(attachment.id)
        return {
            "name": _("Generated attachments"),
            "type": "ir.actions.act_window",
            "res_model": "ir.attachment",
            "view_mode": 'tree,form',
            "domain": [('id', 'in', created_ids)]
        }
