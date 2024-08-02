import asyncio
import json
from typing import Any

from playwright.async_api import Page

from harambe import SDK, PlaywrightUtils as Pu
from harambe.contrib import playwright_harness


async def scrape(sdk: SDK, current_url: str, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("//h1[@class='product-title h2']")

    features = []
    feature_elements = await Pu.get_texts(page, "div.short-description li")
    for feature_element in feature_elements:
        features.append(feature_element)

    items = json.loads(await (await page.query_selector("script#yoast-schema-graph")).inner_text())["@graph"]

    images = []
    for item in items:
        if item["@type"] == "ImageObject":
            images.append(item["url"])

    global_fitments = []

    async def get_fitment_data(table_element):
        fitments = []
        headers_elements = await table_element.query_selector_all('.MuiTableRow-head th')
        headers = [
            await header.inner_text()
            for header in headers_elements
        ]

        await table_element.wait_for_selector('tbody tr td:nth-child(1)')
        rows = await table_element.query_selector_all('tbody tr')
        for row in rows:
            fitment_row = []
            for i, header in enumerate(headers):
                attribute = await row.query_selector(f'td:nth-child({i + 1})')
                key = header
                value = await attribute.inner_text()
                fitment_row.append(
                    {
                        "key": key,
                        "value": value
                    }
                )
            fitments.append(fitment_row)
        return fitments

    try:
        await page.get_by_role("button", name="This Fits...").first.click()
        await page.wait_for_selector('ag-part-config-fitment-table-container .MuiTableRow-head th')
        global_fitments = await get_fitment_data(await page.query_selector('ag-part-config-fitment-table-container'))

    except TimeoutError:
        pass

    for i, item in enumerate(items):
        if item["@type"] == "Product":

            description = item["description"]

            for offer in item["offers"]:
                try:
                    sku = offer["sku"]
                except TimeoutError:
                    sku = None
                title = offer["name"]
                price = offer["priceSpecification"]["price"]

                local_fitment = []
                try:
                    await(await page.query_selector(f'div.product-variants > section:nth-child({i}) div.variant-fits button')).click()
                    await(await page.query_selector(f'div.product-variants > section:nth-child({i}) div.variant-fits button')).click()
                    await page.wait_for_selector(f'div.product-variants > section:nth-child({i}) div.variant-fits ag-part-config-fitment-table-container')
                    table = await page.query_selector(f'div.product-variants > section:nth-child({i}) div.variant-fits ag-part-config-fitment-table-container')
                    local_fitment = await get_fitment_data(table)

                except (AttributeError, TimeoutError):
                    pass



                await sdk.save_data(
                    {
                        "sku": sku,
                        "type": None,
                        "price": price,
                        "title": title,
                        "images": images,
                        "fitment": global_fitments + local_fitment,
                        "features": features,
                        "attributes": [],
                        "description": description,
                        "interchange": [],
                    }
                )


if __name__ == "__main__":
    asyncio.run(SDK.run(scrape,
                        # "https://awe-tuning.com/collections/exhaust/products/awe-tuning-panamera-s-4s-exhaust",
                        "https://awe-tuning.com/collections/exhaust/products/awe-exhaust-suite-for-the-gr-corolla",
                        schema={}, headless=False, harness=playwright_harness))
