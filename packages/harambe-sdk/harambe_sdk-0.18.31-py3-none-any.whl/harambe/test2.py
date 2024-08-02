import asyncio
from typing import Any

from playwright.async_api import Page, TimeoutError

from harambe import SDK
from harambe.contrib import playwright_harness


async def scrape(
    sdk: SDK, url: str, context: Any, *args: Any, **kwargs: Any
) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("//strong[contains(text(),'Solicitation ID:')]/following-sibling::p")
    post_title = await page.locator('div.esbd-result-title h4').first.inner_text()
    try:
        await page.wait_for_selector("//strong[contains(text(),'Solicitation ID:')]/following-sibling::p", timeout=2000)
        notice_id = await page.locator(
            "//strong[contains(text(),'Solicitation ID:')]/following-sibling::p").inner_text()
    except TimeoutError:
        notice_id = None

    try:
        await page.wait_for_selector("//strong[contains(text(),'Solicitation Description')]/following-sibling::p[2]",
                                     timeout=1000)
        desc = await page.locator(
            "//strong[contains(text(),'Solicitation Description')]/following-sibling::p[2]").inner_text()
        desc = desc.strip()
    except TimeoutError:
        try:
            await page.wait_for_selector(
                "//strong[contains(text(),'Solicitation Description')]/following-sibling::p[1]",
                timeout=1000)
            desc = await page.locator(
                "//strong[contains(text(),'Solicitation Description')]/following-sibling::p[1]").inner_text()
            desc = desc.strip()
        except TimeoutError:
            desc = None

    try:
        await page.wait_for_selector('#body_x_tabc_rfp_ext_prxrfp_ext_x_txtOrgaLabel_label + div',
                                     timeout=2000)
        buyer_agency = await page.locator('#body_x_tabc_rfp_ext_prxrfp_ext_x_txtOrgaLabel_label + div div').inner_text()
        buyer_agency = buyer_agency.strip()
    except TimeoutError:
        buyer_agency = None
    try:
        buyer_name = await page.wait_for_selector("//strong[contains(text(),'Contact Name:')]/following-sibling::p[1]",
                                                  timeout=2000)
        buyer_name = await page.locator(
            "//strong[contains(text(),'Contact Name:')]/following-sibling::p[1]").inner_text()
        buyer_name = buyer_name.strip()
    except TimeoutError:
        buyer_name = None
    try:
        await page.wait_for_selector("//strong[contains(text(),'Contact Email')]/following-sibling::p[1]",
                                     timeout=2000)
        buyer_email = await page.locator(
            "//strong[contains(text(),'Contact Email')]/following-sibling::p[1]").inner_text()
        buyer_email = buyer_email.strip()
    except TimeoutError:
        buyer_email = None
    try:
        await page.wait_for_selector(
            "//strong[contains(text(),'Contact Number:')]/following-sibling::p[1]", timeout=2000)
        buyer_phone = await page.locator(
            "//strong[contains(text(),'Contact Number:')]/following-sibling::p[1]").inner_text()
        buyer_phone = buyer_phone.strip()
    except TimeoutError:
        buyer_phone = None
    try:
        await page.wait_for_selector("//strong[contains(text(),'Solicitation Posting Date')]/following-sibling::p[1]",
                                     timeout=1000)
        publish_date = await page.locator(
            "//strong[contains(text(),'Solicitation Posting Date')]/following-sibling::p[1]").inner_text()
    except TimeoutError:
        publish_date = None
    try:
        await page.wait_for_selector("//strong[contains(text(),'Status')]/following-sibling::p[1]", timeout=1000)
        status = await page.locator("//strong[contains(text(),'Status')]/following-sibling::p[1]").inner_text()
    except TimeoutError:
        status = None
    try:
        await page.wait_for_selector("//strong[contains(text(),'Response Due Date:')]/following-sibling::p[1]",
                                     timeout=1000)
        day = await page.locator("//strong[contains(text(),'Response Due Date:')]/following-sibling::p[1]").inner_text()
        day = day.strip()
        hours = await page.locator(
            "//strong[contains(text(),'Response Due Time')]/following-sibling::p[1]").inner_text()
        due_date = day + ' ' + hours
    except TimeoutError:
        due_date = None
    files = []
    try:
        await page.wait_for_selector("//div[@class='esbd-attachment-row ']//a[@data-action='downloadURL']",
                                     timeout=2000)
        links = await page.query_selector_all("//div[@class='esbd-attachment-row ']//a[@data-action='downloadURL']")
        for link in links:
            title = await link.inner_text()
            href = await link.get_attribute('data-href')
            files.append(
                {'title': title.strip(), 'url': 'https://www.txsmartbuy.com' + href}
            )
    except TimeoutError:
        files = []
    p_items = []
    try:
        await page.wait_for_selector("//strong[contains(text(),'Class/Item Code')]/following-sibling::p[1]",
                                     timeout=1000)
        items_full_text = await page.locator(
            "//strong[contains(text(),'Class/Item Code')]/following-sibling::p[1]").inner_text()
        items_meta = items_full_text.split(';')
        items_meta = [item for item in items_meta if item]
        for item_meta in items_meta:
            if item_meta.count('-') == 0:
                if len(p_items) > 0:
                    p_items[-1]['code_description'] += "; " + item_meta.strip()
                continue

            # Split the item_meta string at the first occurrence of '-'
            parts = item_meta.split('-', 1)
            code = parts[0].strip()

            # Further split the remaining part if another '-' exists
            remaining = parts[1].strip()
            if '-' in remaining:
                code, description = remaining.split('-', 1)
            else:
                description = remaining

            # Strip the extracted parts
            code = code.strip()
            description = description.strip()

            while not description[0].isalpha():
                description = description[1:]

            p_items.append(
                {'code_type': None, 'code': code, 'code_description': description, 'description': None}
            )
    except TimeoutError:
        pass

    await sdk.save_data(
        {
            "id": notice_id,
            "title": post_title,
            "status": status,
            "description": desc,
            "location": None,
            "type": None,
            "category": None,
            "posted_date": publish_date,
            "due_date": due_date,
            "buyer_name": buyer_agency,
            "buyer_contact_name": buyer_name,
            "buyer_contact_number": buyer_phone,
            "buyer_contact_email": buyer_email,
            'attachments': files,
            'procurement_items': p_items,
        }
    )


if __name__ == "__main__":
    asyncio.run(SDK.run(scrape, "https://www.txsmartbuy.com/esbd/24R-035LG", schema=sche, harness=playwright_harness))
