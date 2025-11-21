# spiders/yolo_format_mapping.py
import scrapy
import json


class YoloFormatMappingSpider(scrapy.Spider):
    name = "yolo_format_mapping"
    start_urls = ["https://docs.ultralytics.com/modes/export/"]

    def parse(self, response):
        data = []

        for row in response.css("table tbody tr"):
            # 1. Human-readable format name (first column)
            format_name = row.css("td:nth-child(1) a::text").get()
            if not format_name:
                format_name = row.css("td:nth-child(1)::text").get(default="").strip()
            if not format_name:
                continue

            # 2. Format argument (second column, inside <code>)
            format_arg = row.css("td:nth-child(2) code::text").get(default="").strip()
            if not format_arg or format_arg == "-":
                continue  # Skip PyTorch (has no format argument)

            # Clean up names (optional, makes it look nicer)
            format_name = format_name.strip()
            format_arg = format_arg.strip()

            # Add to list: {"Human Name": "format_arg"}
            data.append({format_name: format_arg})

        # Write the exact format you want
        with open("yolo_format_mapping.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Also yield for Scrapy log
        yield {"data": data}
